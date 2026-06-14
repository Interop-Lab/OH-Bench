import os
import subprocess
import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm
import multiprocessing

# ================= 配置 =================
WORKSPACE = "/home/trim/oh-bench-final/repositories"
RESULT_FILE = "/home/trim/oh-bench-final/data/cpp_results.csv"

def run_cppcheck_single_repo(repo_name):
    """
    单个仓库的扫描逻辑
    """
    repo_path = os.path.join(WORKSPACE, repo_name)
    if not os.path.exists(repo_path): return []
    
    xml_out = os.path.join(repo_path, "cppcheck_out.xml")
    cmd = [
        "cppcheck",
        "--enable=all", 
        "--inconclusive",
        "--force", 
        "--xml", 
        "--output-file=" + xml_out,
        repo_path
    ]
    
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1200)
    except Exception as e:
        pass
    
    warnings = []
    if os.path.exists(xml_out):
        try:
            tree = ET.parse(xml_out)
            root = tree.getroot()
            for error in root.findall(".//error"):
                location = error.find("location")
                if location is None: continue
                
                file_path = location.get("file")
                line_no = location.get("line")
                msg = error.get("msg")
                rule_id = error.get("id")
                severity = error.get("severity")
                
                if any(x in file_path for x in ["third_party", "node_modules", "test", "mock"]):
                    continue

                rel_path = os.path.relpath(file_path, repo_path) if file_path.startswith(repo_path) else file_path

                warnings.append({
                    "Repository": repo_name,
                    "Rule_ID": f"cppcheck/{rule_id}",
                    "Message": msg,
                    "Severity": severity,
                    "File_Path": rel_path,
                    "Line_No": line_no
                })
            os.remove(xml_out)
        except: pass
        
    return warnings

def main():
    if not os.path.exists(WORKSPACE):
        print(f"找不到目录: {WORKSPACE}")
        return

    repos = [d for d in os.listdir(WORKSPACE) if os.path.isdir(os.path.join(WORKSPACE, d))]
    print(f"发现 {len(repos)} 个仓库，准备开始全量 C++ 扫描...")
    
    all_warnings = []
    for repo in tqdm(repos):
        ws = run_cppcheck_single_repo(repo)
        all_warnings.extend(ws)
        
    df = pd.DataFrame(all_warnings)
    # 去重：完全相同的报错只留一个
    # df.drop_duplicates(inplace=True)
    
    df.to_csv(RESULT_FILE, index=False, encoding='utf-8-sig')
    print(f"扫描完成！共生成 {len(df)} 条 C++ 告警。")
    print(f"结果已保存至: {RESULT_FILE}")

if __name__ == "__main__":
    main()