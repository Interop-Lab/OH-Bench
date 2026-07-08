#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import argparse
from typing import Dict, List, Any, Set
import pandas as pd
from tqdm import tqdm

# Standardized ArkTS performance and stylistic rules configuration
STRICT_RULES = {
    "rules": {
        "@performance/hp-arkui-use-reusable-component": "warning",
        "@performance/hp-arkui-set-cache-count-for-lazyforeach-grid": "warning",
        "@performance/hp-arkui-no-state-var-access-in-loop": "warning",
        "@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator": "warning",
        "@performance/hp-arkui-use-local-var-to-replace-state-var": "warning",
        "@performance/hp-arkui-use-object-link-to-replace-prop": "warning",
        "@performance/hp-arkui-use-grid-layout-options": "warning",
        "@performance/hp-arkui-use-transition-to-replace-animateto": "warning",
        "@performance/hp-arkui-suggest-use-effectkit-blur": "warning",
        "@performance/hp-arkui-no-func-as-arg-for-reusable-component": "warning",
        "@performance/hp-arkui-use-onAnimationStart-for-swiper-preload": "warning",
        "@performance/hp-arkui-load-on-demand": "warning",
        "@previewer/mandatory-default-value-for-local-initialization": "warning",
        "@performance/foreach-args-check": "warning",
        "@performance/high-frequency-log-check": "warning",
        "@performance/hp-arkts-no-use-any-export-other": "warning",
        "@performance/hp-arkts-no-use-any-export-current": "warning",
        "@hw-stylistic/quotes": "warning",
        "@hw-stylistic/no-tabs": "warning",
        "@hw-stylistic/operator-linebreak": "warning",
        "@hw-stylistic/space-before-blocks": "warning",
        "@hw-stylistic/max-len": "warning",
        "@hw-stylistic/no-multi-spaces": "warning",
        "@hw-stylistic/space-infix-ops": "warning"
    },
    "ignore": ["build/**/*", "oh_modules/**/*", "node_modules/**/*"]
}


def create_strict_config(work_dir: str) -> str:
    """Creates a temporary full-rule configuration file for the linter."""
    config_path = os.path.join(work_dir, "strict_rules.json5")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(STRICT_RULES, f, indent=2)
    return config_path


def count_project_files(repo_path: str) -> int:
    """Counts tracking files in the git repository to determine size."""
    try:
        res = subprocess.run(
            ['git', 'ls-files'], 
            cwd=repo_path, 
            capture_output=True, 
            check=True
        )
        return len(res.stdout.splitlines())
    except subprocess.SubprocessError:
        return 1000  # Default fallback size


def get_smart_commits(repo_path: str, min_files_abs: int, mutation_ratio: float) -> List[str]:
    """Extracts valid historical commits using an size-adaptive mutation threshold."""
    total_files = count_project_files(repo_path)
    if total_files == 0:
        total_files = 1
    
    dynamic_threshold = max(min_files_abs, int(total_files * mutation_ratio))
    valid_commits: List[str] = []
    
    cmd = ["git", "log", "--reverse", "--format=%H", "--shortstat"]
    try:
        res = subprocess.run(
            cmd, 
            cwd=repo_path, 
            capture_output=True, 
            text=True, 
            encoding='utf-8', 
            errors='ignore',
            check=True
        )
        current_hash = None
        
        for line in res.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            if len(line) == 40 and ' ' not in line:
                current_hash = line
            elif 'files changed' in line and current_hash:
                try:
                    num_changed = int(line.split()[0])
                    if num_changed >= dynamic_threshold:
                        valid_commits.append(current_hash)
                except (ValueError, IndexError):
                    pass
                current_hash = None
    except subprocess.SubprocessError:
        pass
    
    # Always append HEAD as the baseline boundary
    try:
        head_res = subprocess.run(
            ['git', 'rev-parse', 'HEAD'], 
            cwd=repo_path, 
            capture_output=True, 
            text=True,
            check=True
        )
        head_hash = head_res.stdout.strip()
        if head_hash and (not valid_commits or valid_commits[-1] != head_hash):
            valid_commits.append(head_hash)
    except subprocess.SubprocessError:
        pass

    # Deduplicate keeping order
    seen: Set[str] = set()
    return [c for c in valid_commits if not (c in seen or seen.add(c))]


def run_linter(
    repo_path: str, 
    repo_name: str, 
    commit_hash: str, 
    config_path: str,
    linter_cmd: str
) -> List[Dict[str, Any]]:
    """Executes code linter and parses violations."""
    abs_out = os.path.join(repo_path, "linter_out.json")
    cmd = [linter_cmd, "--config", config_path, "-f", "json", "-o", abs_out, "."]
    
    try:
        subprocess.run(
            cmd, 
            cwd=repo_path, 
            timeout=600, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
    except subprocess.TimeoutExpired:
        pass

    violations = []
    if os.path.exists(abs_out):
        try:
            with open(abs_out, 'r', encoding='utf-8') as f:
                content = f.read()
                if content:
                    data = json.loads(content)
                    items = data if isinstance(data, list) else data.get("defects", [])
                    for item in items:
                        msgs = item.get("messages", [])
                        if not msgs and "rule" in item:
                            msgs = [item]
                        
                        for m in msgs:
                            full_path = item.get('filePath', '')
                            rel_path = os.path.relpath(full_path, repo_path) if full_path else ''
                            
                            violations.append({
                                "Repository": repo_name,
                                "Commit_Hash": commit_hash,
                                "Rule_ID": m.get('rule') or m.get('ruleId'),
                                "Message": m.get('message'),
                                "Severity": m.get('severity'),
                                "File_Path": rel_path,
                                "Line_No": m.get('line')
                            })
            os.remove(abs_out)
        except (json.JSONDecodeError, IOError):
            pass
    return violations


def main():
    parser = argparse.ArgumentParser(description="Collect ArkTS violations across historical commits.")
    parser.add_argument("--workspace", required=True, help="Path to directories containing git repos")
    parser.add_argument("--output", required=True, help="Path to save output CSV file")
    parser.add_argument("--linter", default="codelinter", help="Command to run the ArkTS codelinter")
    args = parser.parse_args()

    if os.path.exists(args.linter):
        args.linter = os.path.abspath(args.linter)

    if not os.path.exists(args.workspace):
        print(f"[Error] Workspace directory not found: {args.workspace}")
        sys.exit(1)
        
    repos = [d for d in os.listdir(args.workspace) if os.path.isdir(os.path.join(args.workspace, d))]
    
    headers = ["Repository", "Commit_Hash", "Rule_ID", "Message", "Severity", "File_Path", "Line_No"]
    pd.DataFrame(columns=headers).to_csv(args.output, index=False, encoding='utf-8-sig')

    config_path = create_strict_config(os.path.expanduser("~"))
    print(f"Initialized global configuration: {config_path}")
    print(f"Scanning {len(repos)} repositories...")

    for repo in tqdm(repos, desc="Repositories"):
        path = os.path.join(args.workspace, repo)
        if not os.path.exists(os.path.join(path, ".git")):
            continue
        
        commits = get_smart_commits(path, min_files_abs=1, mutation_ratio=0.0)
        
        for commit in tqdm(commits, desc=f"Scanning {repo}", leave=False):
            subprocess.run(
                ["git", "checkout", "-f", commit], 
                cwd=path, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
            
            violations = run_linter(path, repo, commit, config_path, args.linter)
            if violations:
                df = pd.DataFrame(violations)
                df.to_csv(args.output, mode='a', header=False, index=False, encoding='utf-8-sig')
                
        subprocess.run(
            ["git", "checkout", "-f", "master"], 
            cwd=path, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )

    if os.path.exists(config_path):
        os.remove(config_path)
    print(f"\n[Success] Dataset mining complete. Saved to: {args.output}")


if __name__ == "__main__":
    main()