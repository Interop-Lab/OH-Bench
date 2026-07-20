#!/usr/bin/env python3
"""
OH-Bench Dataset Construction Tool (C/C++)
Scans repositories using Cppcheck to collect static analysis violations.
"""

import os
import sys
import subprocess
import argparse
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
import pandas as pd
from tqdm import tqdm


def run_cppcheck_single_repo(workspace: str, repo_name: str) -> List[Dict[str, Any]]:
    """Runs Cppcheck on a single repository and parses the generated XML report."""
    repo_path = os.path.join(workspace, repo_name)
    if not os.path.exists(repo_path):
        return []
    
    xml_out = os.path.join(repo_path, "cppcheck_out.xml")
    cmd = [
        "cppcheck",
        "--enable=all", 
        "--inconclusive",
        "--force", 
        "--xml", 
        f"--output-file={xml_out}",
        repo_path
    ]
    
    try:
        # 1200 seconds execution ceiling to prevent hangs
        subprocess.run(
            cmd, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL, 
            timeout=1200
        )
    except subprocess.SubprocessError:
        pass
    
    violations = []
    if os.path.exists(xml_out):
        try:
            tree = ET.parse(xml_out)
            root = tree.getroot()
            for error in root.findall(".//error"):
                location = error.find("location")
                if location is None: 
                    continue
                
                file_path = location.get("file")
                line_no = location.get("line")
                msg = error.get("msg")
                rule_id = error.get("id")
                severity = error.get("severity")
                
                # Exclude noisy, generated, or third-party scopes
                if any(x in file_path for x in ["third_party", "node_modules", "test", "mock"]):
                    continue

                # Relativize path for benchmark standard
                rel_path = os.path.relpath(file_path, repo_path) if file_path.startswith(repo_path) else file_path

                violations.append({
                    "Repository": repo_name,
                    "Rule_ID": f"cppcheck/{rule_id}",
                    "Message": msg,
                    "Severity": severity,
                    "File_Path": rel_path,
                    "Line_No": line_no
                })
            os.remove(xml_out)
        except (ET.ParseError, IOError):
            if os.path.exists(xml_out):
                os.remove(xml_out)
        
    return violations


def main():
    parser = argparse.ArgumentParser(description="Collect C/C++ static violations using Cppcheck.")
    parser.add_argument("--workspace", required=True, help="Path to directory containing C++ repos")
    parser.add_argument("--output", required=True, help="Path to save output CSV file")
    args = parser.parse_args()

    if not os.path.exists(args.workspace):
        print(f"[Error] Workspace directory not found: {args.workspace}")
        sys.exit(1)

    repos = [d for d in os.listdir(args.workspace) if os.path.isdir(os.path.join(args.workspace, d))]
    print(f"Discovered {len(repos)} repositories. Starting static mining with Cppcheck...")
    
    all_violations: List[Dict[str, Any]] = []
    for repo in tqdm(repos, desc="Cppcheck Scan"):
        repo_violations = run_cppcheck_single_repo(args.workspace, repo)
        all_violations.extend(repo_violations)
        
    if all_violations:
        df = pd.DataFrame(all_violations)
        df.to_csv(args.output, index=False, encoding='utf-8-sig')
        print(f"\n[Success] Collected {len(df)} unique C/C++ violations.")
        print(f"Results saved to: {args.output}")
    else:
        print("\n[Warning] No violations found or cppcheck failed to execute.")


if __name__ == "__main__":
    main()
