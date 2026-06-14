#!/usr/bin/env python3
import json
import os
import shutil

BASE_DIR = "/home/trim/oh-bench-final"
ARKTS_FILE = os.path.join(BASE_DIR, "data/arkts_dataset_final.json")
CPP_FILE = os.path.join(BASE_DIR, "data/cpp_dataset_final.json")
SRC_REPO_DIR = os.path.join(BASE_DIR, "repositories")
DST_REPO_DIR = os.path.join(BASE_DIR, "repositories_slim")

def load_projects(filepath):
    projects = set()
    if not os.path.exists(filepath):
        print(f"  跳过 (不存在): {filepath}")
        return projects
    with open(filepath, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    for task in tasks:
        projects.add(task['project'])
    print(f"  {filepath}: {len(tasks)} 个任务, {len(projects)} 个项目")
    return projects

def main():
    print("=== 提取数据集中用到的项目 ===")
    
    projects = set()
    projects |= load_projects(ARKTS_FILE)
    projects |= load_projects(CPP_FILE)
    
    print(f"\n共需要 {len(projects)} 个项目:")
    for p in sorted(projects):
        print(f"  - {p}")
    
    missing = []
    existing = []
    for p in sorted(projects):
        src = os.path.join(SRC_REPO_DIR, p)
        if os.path.exists(src):
            existing.append(p)
        else:
            missing.append(p)
    
    if missing:
        print(f"\n  缺失 {len(missing)} 个项目:")
        for p in missing:
            print(f"  {p}")
    
    if os.path.exists(DST_REPO_DIR):
        print(f"\n清理已有目录 {DST_REPO_DIR}...")
        shutil.rmtree(DST_REPO_DIR)
    
    os.makedirs(DST_REPO_DIR)
    
    print(f"\n开始复制 {len(existing)} 个项目到 {DST_REPO_DIR}...")
    for i, p in enumerate(existing, 1):
        src = os.path.join(SRC_REPO_DIR, p)
        dst = os.path.join(DST_REPO_DIR, p)
        
        print(f"  [{i}/{len(existing)}] {p}...", end=" ", flush=True)
        shutil.copytree(src, dst, symlinks=True)
        
        size_mb = sum(
            os.path.getsize(os.path.join(dp, f))
            for dp, dn, filenames in os.walk(dst)
            for f in filenames
        ) / (1024 * 1024)
        print(f"{size_mb:.1f} MB")
    
    total_mb = sum(
        os.path.getsize(os.path.join(dp, f))
        for dp, dn, filenames in os.walk(DST_REPO_DIR)
        for f in filenames
    ) / (1024 * 1024)
    print(f"\n完成! 精简仓库总大小: {total_mb:.1f} MB")
    print(f"   路径: {DST_REPO_DIR}")
    print(f"\n下一步: 修改 Dockerfile 中 COPY repositories → COPY repositories_slim")

if __name__ == "__main__":
    main()