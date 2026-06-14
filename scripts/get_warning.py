import os
import subprocess
import json
import pandas as pd
from tqdm import tqdm

WORKSPACE = "/home/trim/oh-bench-final/rep"
RESULT_FILE = "/home/trim/oh-bench-final/data/oh_hardcore_results.csv"
LINTER_CMD = "codelinter"

MIN_FILES_ABS = 1      
MUTATION_RATIO = 0.0   

def create_strict_config(work_dir):
    """创建全量规则配置文件"""
    config_path = os.path.join(work_dir, "strict_rules.json5")
    config_content = {
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
            # === B类 & D类 ===
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
    with open(config_path, 'w') as f:
        json.dump(config_content, f, indent=2)
    return config_path

def count_project_files(repo_path):
    try:
        res = subprocess.run('git ls-files', cwd=repo_path, shell=True, capture_output=True)
        return len(res.stdout.split(b'\n'))
    except:
        return 1000 

def get_smart_commits(repo_path):
    total_files = count_project_files(repo_path)
    if total_files == 0: total_files = 1
    
    dynamic_threshold = max(MIN_FILES_ABS, int(total_files * MUTATION_RATIO))
    # tqdm.write(f"  [Smart Filter] {os.path.basename(repo_path)}: files={total_files}, threshold={dynamic_threshold}")

    valid_commits = []
    
    cmd = 'git log --reverse --format="%H" --shortstat'
    try:
        res = subprocess.run(cmd, cwd=repo_path, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        current_hash = None
        lines = res.stdout.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line: continue
            if len(line) == 40 and ' ' not in line:
                current_hash = line
            elif 'files changed' in line and current_hash:
                try:
                    num = int(line.split(' ')[0])
                    if num >= dynamic_threshold:
                        valid_commits.append(current_hash)
                except: pass
                current_hash = None
    except: pass
    
    try:
        head_res = subprocess.run('git rev-parse HEAD', cwd=repo_path, shell=True, capture_output=True, text=True)
        head_hash = head_res.stdout.strip()
        if head_hash and (not valid_commits or valid_commits[-1] != head_hash):
            valid_commits.append(head_hash)
    except: pass

    seen = set()
    unique_commits = []
    for c in valid_commits:
        if c not in seen:
            unique_commits.append(c)
            seen.add(c)
            
    return unique_commits

def run_linter(repo_path, repo_name, commit_hash, config_path):
    abs_out = os.path.join(repo_path, "linter_out.json")
    
    cmd = [LINTER_CMD, "--config", config_path, "-f", "json", "-o", abs_out, "."]
    
    try:
        subprocess.run(cmd, cwd=repo_path, timeout=600, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except: pass

    warnings = []
    if os.path.exists(abs_out):
        try:
            with open(abs_out, 'r', encoding='utf-8') as f:
                content = f.read()
                if content:
                    data = json.loads(content)
                    items = data if isinstance(data, list) else data.get("defects", [])
                    for item in items:
                        msgs = item.get("messages", [])
                        if not msgs and "rule" in item: msgs = [item]
                        
                        for m in msgs:
                            full_path = item.get('filePath', '')
                            rel_path = os.path.relpath(full_path, repo_path) if full_path else ''
                            
                            warnings.append({
                                "Repository": repo_name,
                                "Commit_Hash": commit_hash,
                                "Rule_ID": m.get('rule') or m.get('ruleId'),
                                "Message": m.get('message'),
                                "Severity": m.get('severity'),
                                "File_Path": rel_path, # 存相对路径
                                "Line_No": m.get('line')
                            })
            os.remove(abs_out)
        except: pass
    return warnings

def main():
    if not os.path.exists(WORKSPACE):
        print(f"找不到 Workspace: {WORKSPACE}")
        return
        
    repos = [d for d in os.listdir(WORKSPACE) if os.path.isdir(os.path.join(WORKSPACE, d))]
    
    print(f"初始化结果文件: {RESULT_FILE}")
    pd.DataFrame(columns=["Repository", "Commit_Hash", "Rule_ID", "Message", "Severity", "File_Path", "Line_No"]).to_csv(RESULT_FILE, index=False, encoding='utf-8-sig')

    config_path = create_strict_config(os.path.expanduser("~"))
    print(f"使用规则配置: {config_path}")

    for repo in tqdm(repos, desc="Repos"):
        path = os.path.join(WORKSPACE, repo)
        if not os.path.exists(os.path.join(path, ".git")): continue
        
        commits = get_smart_commits(path)
        
        for commit in tqdm(commits, desc=f"Scanning {repo}", leave=False):
            subprocess.run(f"git checkout -f {commit}", cwd=path, shell=True, stderr=subprocess.DEVNULL)
            res = run_linter(path, repo, commit, config_path)
            
            if res:
                df = pd.DataFrame(res)
                df.to_csv(RESULT_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')
        subprocess.run("git checkout -f master", cwd=path, shell=True, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    main()