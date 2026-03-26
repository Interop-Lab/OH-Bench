#!/usr/bin/env python3
import sys
import os
import subprocess
import shutil
import json
import re
import xml.etree.ElementTree as ET

REPO_ROOT = "/app/repositories"

def git_checkout_commit(project_dir, commit_hash):
    subprocess.run(["git", "checkout", "."], cwd=project_dir,
                   capture_output=True, timeout=30)
    subprocess.run(["git", "clean", "-fd"], cwd=project_dir,
                   capture_output=True, timeout=30)
    result = subprocess.run(
        ["git", "checkout", commit_hash],
        cwd=project_dir, capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        result2 = subprocess.run(
            ["git", "checkout", "--detach", commit_hash],
            cwd=project_dir, capture_output=True, text=True, timeout=30
        )
        if result2.returncode != 0:
            return False, f"checkout failed: {result.stderr[:200]}"
    return True, "OK"


def git_restore(project_dir):
    subprocess.run(["git", "checkout", "."], cwd=project_dir,
                   capture_output=True, timeout=30)
    subprocess.run(["git", "clean", "-fd"], cwd=project_dir,
                   capture_output=True, timeout=30)
    for branch in ["master", "main"]:
        r = subprocess.run(["git", "checkout", branch], cwd=project_dir,
                           capture_output=True, timeout=30)
        if r.returncode == 0:
            break

def apply_agent_patch(project_dir, input_data):
    if input_data.strip().startswith("{"):
        try:
            files_dict = json.loads(input_data)
            backups = {}
            for rel_path, content in files_dict.items():
                full_path = os.path.join(project_dir, rel_path)
                if os.path.exists(full_path):
                    backup_path = full_path + ".eval_bak"
                    shutil.copy2(full_path, backup_path)
                    backups[full_path] = backup_path
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w", encoding='utf-8') as f:
                    f.write(content)
            return True, backups, "json"
        except Exception as e:
            return False, None, str(e)
    else:
        patch_file = "/tmp/agent_fix.patch"
        with open(patch_file, "w", encoding='utf-8') as f:
            f.write(input_data)
        for extra in [[], ["-p1"], ["-p0"]]:
            cmd = ["git", "apply", "--ignore-space-change", "--ignore-whitespace"] + extra + [patch_file]
            result = subprocess.run(cmd, cwd=project_dir, capture_output=True, text=True)
            if result.returncode == 0:
                return True, None, "git_diff"
        return False, None, f"git apply failed: {result.stderr[:300]}"


def restore_backups(backups):
    if backups:
        for original, backup in backups.items():
            if os.path.exists(backup):
                shutil.move(backup, original)

def parse_codelinter_output(output, project_dir):
    warnings = set()
    current_file = None

    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        file_match = re.match(r'^(/[^\s]+\.(ets|ts|js))\s*\(\d+\)', line)
        if file_match:
            abs_path = file_match.group(1)
            try:
                current_file = os.path.relpath(abs_path, project_dir)
            except ValueError:
                current_file = abs_path
            continue
        warn_match = re.match(
            r'^(\d+):(\d+)\s+(warn|error|suggestion)\s+(.+?)\s{2,}(@\S+|@[\w/-]+)$',
            line
        )
        if warn_match and current_file:
            line_no = warn_match.group(1)
            severity = warn_match.group(3)
            message = warn_match.group(4).strip()
            rule_id = warn_match.group(5)
            warnings.add((current_file, line_no, rule_id))
            continue
        warn_match2 = re.match(
            r'^(\d+):(\d+)\s+(warn|error)\s+(.+?)\s+(@\S+)$',
            line
        )
        if warn_match2 and current_file:
            line_no = warn_match2.group(1)
            rule_id = warn_match2.group(5)
            warnings.add((current_file, line_no, rule_id))

    return warnings


def run_codelinter(project_dir, target_file_rel):
    cmd = f"codelinter {project_dir}"
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=300, executable='/bin/bash'
        )
    except subprocess.TimeoutExpired:
        return set(), "TIMEOUT"

    output = result.stdout + "\n" + result.stderr
    warnings = parse_codelinter_output(output, project_dir)
    return warnings, output

def run_cppcheck(project_dir, target_file_rel):
    warnings = set()
    
    cmd = [
        "cppcheck", "--enable=all",
        "--suppress=missingIncludeSystem",
        "--suppress=missingInclude",
        "--xml", "--xml-version=2",
        project_dir
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return warnings, "TIMEOUT"

    output = result.stderr

    try:
        root = ET.fromstring(output)
        for error in root.iter('error'):
            err_id = error.get('id', '')
            if err_id in ('checkersReport', 'unmatchedSuppression'):
                continue
            for location in error.iter('location'):
                file_path = location.get('file', '')
                line_no = location.get('line', '0')
                try:
                    rel_path = os.path.relpath(file_path, project_dir)
                except ValueError:
                    rel_path = file_path
                warnings.add((rel_path, line_no, f"cppcheck/{err_id}"))
    except ET.ParseError:
        for m in re.finditer(r'id="([^"]+)".*?file="([^"]+)".*?line="(\d+)"', output):
            err_id, err_file, err_line = m.groups()
            try:
                rel_path = os.path.relpath(err_file, project_dir)
            except ValueError:
                rel_path = err_file
            warnings.add((rel_path, err_line, f"cppcheck/{err_id}"))

    return warnings, output

def run_linter(project_dir, rule_id, target_file_rel):
    if rule_id.startswith("cppcheck/"):
        return run_cppcheck(project_dir, target_file_rel)
    else:
        return run_codelinter(project_dir, target_file_rel)


def check_target_warning(warnings, rule_id, target_file_rel):
    for (file_path, line_no, w_rule) in warnings:
        if target_file_rel in file_path or file_path in target_file_rel:
            if w_rule == rule_id:
                return True
    return False


def count_new_warnings(base_warnings, new_warnings):
    added = new_warnings - base_warnings
    return len(added), added

def main():
    if len(sys.argv) < 4:
        print("Usage: evaluate <rule_id> <project_name> <target_file> [commit_hash]")
        sys.exit(1)

    rule_id = sys.argv[1]
    project_name = sys.argv[2]
    target_file_rel = sys.argv[3]
    commit_hash = sys.argv[4] if len(sys.argv) > 4 else None

    project_dir = os.path.join(REPO_ROOT, project_name)
    if not os.path.exists(project_dir):
        print(f"ERROR: Project not found: {project_dir}")
        sys.exit(2)

    try:
        if commit_hash:
            ok, msg = git_checkout_commit(project_dir, commit_hash)
            if not ok:
                print(f"ERROR: {msg}")
                sys.exit(0)
        base_warnings, base_output = run_linter(project_dir, rule_id, target_file_rel)
        has_target = check_target_warning(base_warnings, rule_id, target_file_rel)
        if not has_target:
            sys.stderr.write(f"WARN: Baseline has {len(base_warnings)} warnings but target rule not found\n")
            sys.stderr.write(f"Looking for: file={target_file_rel}, rule={rule_id}\n")
            if base_warnings:
                sys.stderr.write(f"Sample warnings:\n")
                for w in list(base_warnings)[:5]:
                    sys.stderr.write(f"  {w}\n")
        input_data = sys.stdin.read()
        if not input_data.strip():
            print("ERROR: No input via stdin")
            sys.exit(0)
        success, backups, patch_type = apply_agent_patch(project_dir, input_data)
        if not success:
            print(f"APPLY_ERROR: {patch_type}")
            sys.exit(0)
        new_warnings, new_output = run_linter(project_dir, rule_id, target_file_rel)
        syntax_markers = ["SyntaxError", "Build failed", "Compile error", "Parse error"]
        if any(m in new_output for m in syntax_markers):
            print("SYNTAX_FAIL")
            sys.exit(0)

        target_still_exists = check_target_warning(new_warnings, rule_id, target_file_rel)

        if target_still_exists:
            print("LINTER_FAIL")
        else:
            num_added, added_set = count_new_warnings(base_warnings, new_warnings)
            if num_added > 0:
                print(f"SECONDARY_DEFECT: {num_added}")
            else:
                print("PASS")

    except subprocess.TimeoutExpired:
        print("TIMEOUT")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        if commit_hash:
            git_restore(project_dir)
        else:
            subprocess.run(["git", "checkout", "."], cwd=project_dir,
                           capture_output=True, timeout=30)
            subprocess.run(["git", "clean", "-fd"], cwd=project_dir,
                           capture_output=True, timeout=30)


if __name__ == "__main__":
    main()
