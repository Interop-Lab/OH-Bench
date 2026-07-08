#!/usr/bin/env python3
import sys
import os
import subprocess
import json

REPO_ROOT = "/app/repositories"

def git_checkout_commit(project_dir, commit_hash):
    subprocess.run(["git", "checkout", "-f", "."], cwd=project_dir, capture_output=True)
    subprocess.run(["git", "clean", "-fdx"], cwd=project_dir, capture_output=True)
    result = subprocess.run(["git", "checkout", "-f", commit_hash], cwd=project_dir, capture_output=True, text=True)
    if result.returncode != 0:
        return False, f"Checkout failed: {result.stderr}"
    return True, "OK"

def apply_patch(project_dir, input_data):
    if input_data.strip().startswith("{"):
        try:
            files_dict = json.loads(input_data)
            for rel_path, content in files_dict.items():
                full_path = os.path.join(project_dir, rel_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w", encoding='utf-8') as f:
                    f.write(content)
            return True, "json_full_file_success"
        except Exception as e:
            return False, f"json parse error: {e}"

    patch_file = "/tmp/agent_fix.patch"
    with open(patch_file, "w", encoding='utf-8') as f:
        f.write(input_data)
    
    last_error = ""
    for extra in [[], ["-p1"], ["-p0"]]:
        cmd = ["git", "apply", "--ignore-space-change", "--ignore-whitespace"] + extra + [patch_file]
        res = subprocess.run(cmd, cwd=project_dir, capture_output=True, text=True)
        if res.returncode == 0:
            return True, "git_apply_success"
        last_error = res.stderr

    for extra in ["-p1", "-p0"]:
        cmd = ["patch", extra, "--no-backup-if-mismatch", "--fuzz=3", "--force", "-i", patch_file]
        res = subprocess.run(cmd, cwd=project_dir, capture_output=True, text=True)
        if res.returncode == 0:
            return True, "gnu_patch_success"
        last_error += f"\nPatch fallback failed: {res.stderr}"

    return False, last_error[:300]

def main():
    if len(sys.argv) < 4:
        print("ERROR: Usage: evaluate_runtime <repo_name> <buggy_commit> <test_command>")
        sys.exit(1)

    repo_name = sys.argv[1]
    buggy_commit = sys.argv[2]
    test_cmd = sys.argv[3]

    project_dir = os.path.join(REPO_ROOT, repo_name)
    if not os.path.exists(project_dir):
        print(f"ERROR: Repo not found at {project_dir}")
        sys.exit(0)

    try:
        ok, msg = git_checkout_commit(project_dir, buggy_commit)
        if not ok:
            print(f"ERROR: {msg}")
            sys.exit(0)

        input_data = sys.stdin.read().strip()
        if not input_data:
            print("ERROR: No patch provided via stdin")
            sys.exit(0)

        success, msg = apply_patch(project_dir, input_data)
        if not success:
            print(f"APPLY_ERROR: {msg}") 
            sys.exit(0)

        local_prop = os.path.join(project_dir, "local.properties")
        with open(local_prop, "w") as f:
            f.write("sdk.dir=/opt/ohos-sdk\n")
        
        hvigorw = os.path.join(project_dir, "hvigorw")
        if os.path.exists(hvigorw):
            os.chmod(hvigorw, 0o755)

        if os.path.exists(os.path.join(project_dir, "oh-package.json5")):
            subprocess.run("ohpm install --all", shell=True, cwd=project_dir, capture_output=True, timeout=120)

        result = subprocess.run(
            test_cmd, shell=True, cwd=project_dir, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=300
        )

        out_text = (result.stdout + result.stderr).lower()
        
        if result.returncode == 0 and "fail" not in out_text and "error" not in out_text:
            print("PASS")
        elif "syntaxerror" in out_text or "compile error" in out_text:
            print("SYNTAX_FAIL")
        else:
            print("TEST_FAIL")

    except subprocess.TimeoutExpired:
        print("TIMEOUT")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        subprocess.run(["git", "checkout", "-f", "."], cwd=project_dir, capture_output=True)

if __name__ == "__main__":
    main()