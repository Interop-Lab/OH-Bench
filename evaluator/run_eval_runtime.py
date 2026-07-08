#!/usr/bin/env python3
import json
import subprocess
import os
import sys
import re
import argparse
from typing import Dict, List, Tuple, Optional, Any

# ============================================================================
# Configuration
# ============================================================================

DOCKER_IMAGE = "oh-bench-runtime:latest"
DATASET_PATH = "dataset/extensibility/runtime_extensibility_145.json"
REPO_ROOT = "repos"

SIGNAL_PASS = "PASS"
SIGNAL_TEST_FAIL = "TEST_FAIL"
SIGNAL_SYNTAX_FAIL = "SYNTAX_FAIL"
SIGNAL_APPLY_ERROR = "APPLY_ERROR"
SIGNAL_TIMEOUT = "TIMEOUT"
SIGNAL_SYSTEM_ERROR = "SYSTEM_ERROR"

# ============================================================================
# Helper Utilities
# ============================================================================

def extract_files_from_diff(diff_text: str) -> List[str]:
    files = set()
    for line in diff_text.splitlines():
        if line.startswith("--- a/"):
            files.add(line[6:].strip())
    return list(files)


def get_file_at_commit(repo_dir: str, commit: str, filepath: str) -> str:
    cmd = ["git", "show", f"{commit}:{filepath}"]
    res = subprocess.run(cmd, cwd=repo_dir, capture_output=True, text=True)
    return res.stdout if res.returncode == 0 else ""


def parse_diff_hunks(diff_text: str) -> List[Tuple[List[str], List[str]]]:
    hunks = []
    current_old, current_new = [], []
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


def apply_diff(original: str, diff_text: str) -> Optional[str]:
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
            continue

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

    return result if result != original else None


def clean_model_output(content: str) -> str:
    if not content:
        return ""
    cleaned = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
    blocks = re.findall(r'```[a-zA-Z]*\n(.*?)```', cleaned, flags=re.DOTALL)
    if blocks:
        diff_blocks = [b for b in blocks if b.strip().startswith('---') or 
                                            b.strip().startswith('diff ') or 
                                            b.strip().startswith('@@')]
        cleaned = diff_blocks[-1] if diff_blocks else blocks[-1]
    cleaned = cleaned.strip()
    return cleaned + '\n' if cleaned else ""


def prepare_payload(repo_dir: str, commit: str, diff_text: str) -> Tuple[str, str]:
    cleaned_diff = clean_model_output(diff_text)
    target_files = extract_files_from_diff(cleaned_diff)
    if not target_files:
        return cleaned_diff, "raw_diff"

    result_files = {}
    for path in target_files:
        orig = get_file_at_commit(repo_dir, commit, path)
        if not orig:
            return cleaned_diff, "raw_diff"
        patched = apply_diff(orig, cleaned_diff)
        if patched:
            result_files[path] = patched
        else:
            return cleaned_diff, "raw_diff"

    return json.dumps(result_files), "json_full_file"

def evaluate_runtime_instance(task: Dict[str, Any], raw_patch: str) -> Tuple[str, str, str]:
    repo_name = task['repo_name']
    buggy_commit = task['buggy_commit']
    test_cmd = task.get('test_command', './hvigorw test --no-daemon')
    repo_dir = os.path.join(REPO_ROOT, repo_name)

    payload, method = prepare_payload(repo_dir, buggy_commit, raw_patch)

    cmd = [
        "docker", "run", "--rm", "-i", DOCKER_IMAGE,
        "python3", "/workspace/evaluate_runtime_in_docker.py",
        repo_name, buggy_commit, test_cmd
    ]
    try:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = proc.communicate(input=payload, timeout=600)
        lines = stdout.strip().split('\n')
        signal = lines[-1] if lines else SIGNAL_SYSTEM_ERROR
        return signal, method, stderr.strip()[:100]
    except subprocess.TimeoutExpired:
        proc.kill()
        return SIGNAL_TIMEOUT, method, ""
    except Exception as e:
        return SIGNAL_SYSTEM_ERROR, method, str(e)


def main():
    parser = argparse.ArgumentParser(description="OH-Bench Academic Runtime Evaluator")
    parser.add_argument("--results", required=True, help="Path to predictions JSON")
    args = parser.parse_args()

    benchmark_size = 145

    if not os.path.exists(DATASET_PATH):
        print(f"[Error] Dataset missing: {DATASET_PATH}")
        sys.exit(1)

    with open(DATASET_PATH, 'r', encoding='utf-8') as f:
        dataset = {bug['bug_id']: bug for bug in json.load(f)}

    with open(args.results, 'r', encoding='utf-8') as f:
        predictions = json.load(f)

    print(f"\nEvaluating Runtime Extensibility Benchmark ({benchmark_size} instances)")
    print("-" * 65)

    records = []
    for pred in predictions:
        iid = pred.get('instance_id', '')
        task = dataset.get(iid)
        if not task:
            continue

        patch = pred.get('model_patch', '')
        signal, method, _ = evaluate_runtime_instance(task, patch)
        
        print(f"{iid:<35} | {signal:<15} | {method}")
        records.append({"instance_id": iid, "signal": signal})

    n_applied = sum(1 for r in records if r['signal'] in [SIGNAL_PASS, SIGNAL_TEST_FAIL])
    n_passed = sum(1 for r in records if r['signal'] == SIGNAL_PASS)

    par = n_applied / benchmark_size
    wer = n_passed / n_applied if n_applied > 0 else 0.0
    spr = par * wer

    print("\n" + "=" * 65)
    print("                  OH-BENCH RUNTIME EVALUATION SUMMARY")
    print("=" * 65)
    print(f"Total Benchmark Size:  {benchmark_size}")
    print("-" * 65)
    print(f"Format Competence (PAR):      {par:.4f}  ({n_applied}/{benchmark_size})")
    print(f"Semantic Competence (WER):    {wer:.4f}  ({n_passed}/{n_applied})")
    print(f"Success/Resolve Rate (SPR):   {spr:.4f}  ({n_passed}/{benchmark_size})")
    print("=" * 65)


if __name__ == "__main__":
    main()