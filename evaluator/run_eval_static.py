#!/usr/bin/env python3
import json
import subprocess
import os
import sys
import re
import argparse
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any

# ============================================================================
# Configuration
# ============================================================================

DOCKER_IMAGE = "oh-bench-evaluator:latest"

DATASET_PATHS = {
    "arkts": "dataset/main_benchmark/ohbench_arkts_v1.0.json",
    "cpp": "dataset/main_benchmark/ohbench_cpp_v1.0.json",
}

# Standardized Evaluation Signals
SIGNAL_PASS = "PASS"
SIGNAL_LINTER_FAIL = "LINTER_FAIL"
SIGNAL_SYNTAX_FAIL = "SYNTAX_FAIL"
SIGNAL_SECONDARY_DEFECT = "SECONDARY_DEFECT"
SIGNAL_APPLY_ERROR = "APPLY_ERROR"
SIGNAL_TIMEOUT = "TIMEOUT"
SIGNAL_SYSTEM_ERROR = "SYSTEM_ERROR"

# ============================================================================
# Core Diff & Text Processing
# ============================================================================

def parse_diff_hunks(diff_text: str) -> List[Tuple[List[str], List[str]]]:
    """Parse unified diff into (old_lines, new_lines) hunks."""
    hunks = []
    current_old = []
    current_new = []
    in_hunk = False

    for line in diff_text.splitlines():
        if line.startswith('@@'):
            if in_hunk and (current_old or current_new):
                hunks.append((current_old[:], current_new[:]))
            current_old, current_new = [], []
            in_hunk = True
            continue

        if not in_hunk:
            continue
        if line.startswith('---') or line.startswith('+++'):
            continue

        if line.startswith('-'):
            current_old.append(line[1:])
        elif line.startswith('+'):
            current_new.append(line[1:])
        elif line.startswith(' '):
            current_old.append(line[1:])
            current_new.append(line[1:])
        else:
            current_old.append(line)
            current_new.append(line)

    if in_hunk and (current_old or current_new):
        hunks.append((current_old[:], current_new[:]))
    return hunks


def apply_diff_by_text_match(original: str, diff_text: str) -> Optional[str]:
    """Apply diff via direct text matching (Fallback)."""
    hunks = parse_diff_hunks(diff_text)
    if not hunks:
        return None

    result = original
    for old_lines, new_lines in hunks:
        if not old_lines:
            continue
        old_text = '\n'.join(old_lines)
        new_text = '\n'.join(new_lines)

        if old_text in result:
            result = result.replace(old_text, new_text, 1)
        else:
            old_stripped = '\n'.join(l.rstrip() for l in old_lines)
            result_lines = result.splitlines()
            found = False
            for i in range(len(result_lines)):
                window = '\n'.join(l.rstrip() for l in result_lines[i:i + len(old_lines)])
                if window == old_stripped:
                    before = '\n'.join(result_lines[:i])
                    after = '\n'.join(result_lines[i + len(old_lines):])
                    result = before + ('\n' if before else '') + new_text + ('\n' if after else '') + after
                    found = True
                    break
            if not found:
                return None

    return None if result == original else result


def apply_diff_with_patch(original_content: str, diff_text: str) -> Optional[str]:
    """Apply diff using system patch utility."""
    if not diff_text.endswith('\n'):
        diff_text += '\n'

    with tempfile.TemporaryDirectory() as tmpdir:
        orig_file = os.path.join(tmpdir, "original.txt")
        with open(orig_file, 'w', encoding='utf-8') as f:
            f.write(original_content)

        patch_file = os.path.join(tmpdir, "fix.patch")
        with open(patch_file, 'w', encoding='utf-8') as f:
            f.write(diff_text)

        for strip_level in [0, 1, 2]:
            work_file = os.path.join(tmpdir, "work.txt")
            with open(work_file, 'w', encoding='utf-8') as f:
                f.write(original_content)

            result = subprocess.run(
                ["patch", f"-p{strip_level}", "--no-backup-if-mismatch",
                 "--fuzz=3", "--silent", work_file, patch_file],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                with open(work_file, 'r', encoding='utf-8') as f:
                    return f.read()
    return None


def clean_model_output(content: str) -> str:
    """Clean markdown code blocks and reasoning/think tags."""
    if not content:
        return ""
    cleaned = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
    blocks = re.findall(r'```[a-zA-Z]*\n(.*?)```', cleaned, flags=re.DOTALL)
    if blocks:
        diff_blocks = [b for b in blocks if b.strip().startswith('---') or 
                                            b.strip().startswith('diff ') or 
                                            b.strip().startswith('@@')]
        cleaned = diff_blocks[-1] if diff_blocks else blocks[-1]
    else:
        lines = cleaned.splitlines()
        for i, line in enumerate(lines):
            if line.startswith('--- a/') or line.startswith('diff --git') or line.startswith('@@'):
                cleaned = '\n'.join(lines[i:])
                break
    cleaned = cleaned.strip()
    return cleaned + '\n' if cleaned else ""


def normalize_diff_header(diff_text: str) -> str:
    """Ensure proper git-style diff headers."""
    stripped = diff_text.strip()
    if stripped.startswith("diff --git"):
        return diff_text

    if stripped.startswith("--- a/"):
        lines = stripped.split('\n')
        old_path = lines[0][len("--- "):].strip()
        new_path = old_path.replace("a/", "b/", 1)
        header = f"diff --git {old_path} {new_path}"
        result = header + '\n' + stripped
        if not result.endswith('\n'):
            result += '\n'
        return result
    return diff_text


def prepare_payload(model_patch: Any, buggy_files: Dict[str, str]) -> Tuple[str, str]:
    """Prepares the exact file content or diff payload for the container linter."""
    if isinstance(model_patch, str):
        return clean_model_output(model_patch), "raw_diff"

    if not isinstance(model_patch, dict):
        return json.dumps(model_patch), "unknown"

    result_files = {}
    all_success = True
    conversion_method = "full_content"

    for file_path, content in model_patch.items():
        if not isinstance(content, str):
            result_files[file_path] = str(content)
            continue

        content = clean_model_output(content)
        is_diff = content.strip().startswith("---") or content.strip().startswith("diff ") or content.strip().startswith("@@")
        
        if not is_diff:
            result_files[file_path] = content
            continue

        conversion_method = "diff_applied"
        content = normalize_diff_header(content)
        original = buggy_files.get(file_path, "")
        if not original:
            all_success = False
            continue

        patched = apply_diff_by_text_match(original, content)
        if patched is not None:
            result_files[file_path] = patched
            continue

        import tempfile
        patched = apply_diff_with_patch(original, content)
        if patched is not None:
            result_files[file_path] = patched
            conversion_method = "diff_patched"
            continue

        all_success = False

    if not all_success or not result_files:
        diffs = []
        for v in model_patch.values():
            if isinstance(v, str):
                cleaned = clean_model_output(v)
                cleaned = normalize_diff_header(cleaned)
                diffs.append(cleaned)
        combined = '\n'.join(diffs)
        combined = re.sub(r'^```.*$', '', combined, flags=re.MULTILINE).strip() + '\n'
        return combined, "raw_diff_fallback"

    return json.dumps(result_files), conversion_method


# ============================================================================
# Docker Execution Engine
# ============================================================================

class PersistentDockerContainer:
    """Manages persistent Docker execution for high-throughput evaluation."""
    def __init__(self, image: str):
        self.image = image
        self.name = f"oh-bench-eval-{os.getpid()}"
        self.active = False

    def start(self) -> bool:
        subprocess.run(["docker", "rm", "-f", self.name], capture_output=True, timeout=10)
        
        host_scripts_dir = os.path.abspath("evaluator/container_scripts")
        
        proc = subprocess.run(
            ["docker", "run", "-d", "--name", self.name, 
             "-v", f"{host_scripts_dir}:/workspace",
             self.image, "sleep", "infinity"],
            capture_output=True, text=True, timeout=30
        )
        if proc.returncode == 0:
            self.active = True
            return True
        return False

    def execute(self, args: List[str], stdin_data: str, timeout: int = 600) -> Tuple[str, str]:
        if not self.active:
            return SIGNAL_SYSTEM_ERROR, "Container not running"
        cmd = ["docker", "exec", "-i", self.name] + args
        try:
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = proc.communicate(input=stdin_data, timeout=timeout)
            return stdout.strip(), stderr.strip()[:300]
        except subprocess.TimeoutExpired:
            proc.kill()
            return SIGNAL_TIMEOUT, "Execution timeout"
        except Exception as e:
            return SIGNAL_SYSTEM_ERROR, str(e)

    def stop(self):
        if self.active:
            subprocess.run(["docker", "rm", "-f", self.name], capture_output=True, timeout=15)
            self.active = False


def evaluate_with_persistent_container(
    container: PersistentDockerContainer,
    task: Dict[str, Any],
    model_patch: Any
) -> Tuple[str, str, str]:
    rule_id = task['rule_id']
    project = task['project']
    target_file = task['target_file']
    commit_hash = task.get('commit_hash', '')
    buggy_files = task.get('buggy_files', {})

    payload, method = prepare_payload(model_patch, buggy_files)

    cmd_args = ["eval_static", rule_id, project, target_file]
    if commit_hash:
        cmd_args.append(commit_hash)

    stdout, stderr = container.execute(cmd_args, payload)
    return stdout, method, stderr


def evaluate_with_docker_run(
    task: Dict[str, Any],
    model_patch: Any
) -> Tuple[str, str, str]:
    rule_id = task['rule_id']
    project = task['project']
    target_file = task['target_file']
    commit_hash = task.get('commit_hash', '')
    buggy_files = task.get('buggy_files', {})

    payload, method = prepare_payload(model_patch, buggy_files)

    cmd = [
        "docker", "run", "--rm", "-i", 
        DOCKER_IMAGE,
        "eval_static", rule_id, project, target_file
    ]
    if commit_hash:
        cmd.append(commit_hash)

    try:
        proc = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        stdout, stderr = proc.communicate(input=payload, timeout=600)
        return stdout.strip(), method, stderr.strip()[:300]
    except subprocess.TimeoutExpired:
        proc.kill()
        return SIGNAL_TIMEOUT, method, ""
    except Exception as e:
        return f"{SIGNAL_SYSTEM_ERROR}: {e}", method, ""


# ============================================================================
# Academic Metrics Calculator
# ============================================================================

def calculate_metrics(results: List[Dict[str, Any]], total_benchmark_size: int) -> Dict[str, float]:
    """
    Computes rigorous metrics according to paper Definition 1:
        N_total = Fixed benchmark size (ArkTS: 382, C++: 359)
        PAR = N_applied / N_total
        WER = N_eliminated / N_applied
        SDR = N_secondary / N_eliminated
        SPR = PAR * WER * (1 - SDR)
    """
    n_total = total_benchmark_size
    n_applied = 0
    n_eliminated = 0
    n_secondary = 0

    for r in results:
        sig = r['signal']
        if sig in [SIGNAL_PASS, SIGNAL_SECONDARY_DEFECT, SIGNAL_LINTER_FAIL, SIGNAL_SYNTAX_FAIL]:
            n_applied += 1
        if sig in [SIGNAL_PASS, SIGNAL_SECONDARY_DEFECT]:
            n_eliminated += 1
        if sig == SIGNAL_SECONDARY_DEFECT:
            n_secondary += 1

    par = n_applied / n_total if n_total > 0 else 0.0
    wer = n_eliminated / n_applied if n_applied > 0 else 0.0
    sdr = n_secondary / n_eliminated if n_eliminated > 0 else 0.0
    spr = par * wer * (1.0 - sdr)

    return {
        "n_total": n_total,
        "n_applied": n_applied,
        "n_eliminated": n_eliminated,
        "n_secondary": n_secondary,
        "PAR": par,
        "WER": wer,
        "SDR": sdr,
        "SPR": spr
    }


# ============================================================================
# Main Execution Loop
# ============================================================================

def run_evaluation(args):
    benchmark_size = 382 if args.dataset == "arkts" else 359

    dataset_path = DATASET_PATHS[args.dataset]
    if not os.path.exists(dataset_path):
        print(f"[Error] Dataset file missing: {dataset_path}")
        sys.exit(1)

    with open(dataset_path, 'r', encoding='utf-8') as f:
        ground_truth = {task['instance_id']: task for task in json.load(f)}

    with open(args.results, 'r', encoding='utf-8') as f:
        predictions = json.load(f)

    started = (args.start is None)
    filtered_predictions = []
    for pred in predictions:
        iid = pred.get('instance_id', '')
        if not started:
            if iid == args.start:
                started = True
            else:
                continue
        filtered_predictions.append(pred)
        if args.end and iid == args.end:
            break

    print(f"\nEvaluating {args.dataset.upper()} Benchmark ({benchmark_size} instances)")
    print(f"Executing {len(filtered_predictions)} tasks...")
    print(f"{'Instance ID':<20} | {'Signal':<22} | {'Rule'}")
    print("-" * 70)

    container = None
    if not args.isolated:
        container = PersistentDockerContainer(DOCKER_IMAGE)
        if not container.start():
            print("  [Warning] Failed to start persistent container. Falling back to isolated run.")
            container = None

    evaluated_records = []
    rule_results = defaultdict(list)

    try:
        for pred in filtered_predictions:
            iid = pred.get('instance_id', '')
            task = ground_truth.get(iid)
            if not task:
                continue

            patch = pred.get('model_patch', pred.get('patch', ''))
            
            if container:
                stdout, method, stderr = evaluate_with_persistent_container(container, task, patch)
            else:
                stdout, method, stderr = evaluate_with_docker_run(task, patch)

            # Normalize output signal
            signal = SIGNAL_SYSTEM_ERROR
            if "PASS" in stdout:
                signal = SIGNAL_PASS
            elif "SECONDARY_DEFECT" in stdout:
                signal = SIGNAL_SECONDARY_DEFECT
            elif "LINTER_FAIL" in stdout:
                signal = SIGNAL_LINTER_FAIL
            elif "SYNTAX_FAIL" in stdout:
                signal = SIGNAL_SYNTAX_FAIL
            elif "APPLY_ERROR" in stdout:
                signal = SIGNAL_APPLY_ERROR
            elif "TIMEOUT" in stdout:
                signal = SIGNAL_TIMEOUT

            short_rule = task['rule_id'].split('/')[-1][:25]
            print(f"{iid:<20} | {signal:<22} | {short_rule}")

            if args.verbose and stderr:
                print(f"{'':>20}   [stderr] {stderr[:150]}")

            record = {"instance_id": iid, "signal": signal, "rule_id": task['rule_id']}
            evaluated_records.append(record)
            rule_results[task['rule_id']].append(record)

    finally:
        if container:
            container.stop()

    # Calculate global metrics
    m = calculate_metrics(evaluated_records, benchmark_size)

    # Output Academic Report
    print("\n" + "=" * 65)
    print("                      OH-BENCH EVALUATION REPORT")
    print("=" * 65)
    print(f"Dataset Target:        {args.dataset.upper()}")
    print(f"Total Benchmark Size:  {m['n_total']}")
    print("-" * 65)
    print(f"Format Competence    (PAR):  {m['PAR']:.4f}  ({m['n_applied']}/{m['n_total']})")
    print(f"Semantic Competence  (WER):  {m['WER']:.4f}  ({m['n_eliminated']}/{m['n_applied']})")
    print(f"Holistic Competence  (SDR):  {m['SDR']:.4f}  ({m['n_secondary']}/{m['n_eliminated']})")
    print(f"Success/Resolve Rate (SPR):  {m['SPR']:.4f}")
    print("=" * 65)


# ============================================================================
# CLI Entry Point
# ============================================================================

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="OH-Bench Static Analysis Evaluator"
    )
    parser.add_argument(
        "--dataset",
        choices=["arkts", "cpp"],
        required=True,
        help="Dataset to evaluate on"
    )
    parser.add_argument(
        "--results",
        required=True,
        help="Path to model predictions JSON file"
    )
    parser.add_argument(
        "--start",
        default=None,
        help="Start evaluation from this instance_id"
    )
    parser.add_argument(
        "--end",
        default=None,
        help="End evaluation at this instance_id"
    )
    parser.add_argument(
        "--isolated",
        action="store_true",
        help="Use isolated docker run mode (slower but safer, equivalent to --slow)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print stderr output for debugging"
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    run_evaluation(args)

if __name__ == "__main__":
    main()