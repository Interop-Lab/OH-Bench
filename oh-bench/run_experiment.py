#!/usr/bin/env python3

import json
import subprocess
import os
import sys
import re
import argparse
import tempfile
from collections import defaultdict
from datetime import datetime

DOCKER_IMAGE = "oh-bench-env"
DATASET_MAP = {
    "arkts": "data/arkts_dataset_final.json",
    "cpp": "data/cpp_dataset_final.json",
}


def parse_diff_hunks(diff_text):
    hunks = []
    current_old = []
    current_new = []
    in_hunk = False

    for line in diff_text.splitlines():
        if line.startswith('@@'):
            if in_hunk and (current_old or current_new):
                hunks.append((current_old[:], current_new[:]))
            current_old = []
            current_new = []
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


def apply_diff_by_text_match(original_content, diff_text):
    hunks = parse_diff_hunks(diff_text)
    if not hunks:
        return None

    result = original_content

    for old_lines, new_lines in hunks:
        if not old_lines:
            continue

        old_text = '\n'.join(old_lines)
        new_text = '\n'.join(new_lines)

        if old_text in result:
            result = result.replace(old_text, new_text, 1)
        else:
            old_stripped = '\n'.join(l.rstrip() for l in old_lines)
            result_stripped_lines = result.splitlines()

            found = False
            for i in range(len(result_stripped_lines)):
                window = '\n'.join(l.rstrip() for l in result_stripped_lines[i:i + len(old_lines)])
                if window == old_stripped:
                    before = '\n'.join(result_stripped_lines[:i])
                    after = '\n'.join(result_stripped_lines[i + len(old_lines):])
                    result = before + ('\n' if before else '') + new_text + ('\n' if after else '') + after
                    found = True
                    break

            if not found:
                return None

    if result == original_content:
        return None

    return result


def apply_diff_with_patch(original_content, diff_text):
    if not diff_text.endswith('\n'):
        diff_text += '\n'

    with tempfile.TemporaryDirectory() as tmpdir:
        orig_file = os.path.join(tmpdir, "original.txt")
        with open(orig_file, 'w', encoding='utf-8') as f:
            f.write(original_content)

        patch_file = os.path.join(tmpdir, "fix.patch")
        with open(patch_file, 'w', encoding='utf-8') as f:
            f.write(diff_text)

        for strip in [0, 1, 2]:
            work_file = os.path.join(tmpdir, "work.txt")
            with open(work_file, 'w', encoding='utf-8') as f:
                f.write(original_content)

            result = subprocess.run(
                ["patch", f"-p{strip}", "--no-backup-if-mismatch",
                 "--fuzz=3", "--silent", work_file, patch_file],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                with open(work_file, 'r', encoding='utf-8') as f:
                    return f.read()

    return None


def prepare_payload(model_patch, buggy_files):
    if isinstance(model_patch, str):
        return model_patch, "raw_diff"

    if not isinstance(model_patch, dict):
        return json.dumps(model_patch), "unknown"

    result_files = {}
    all_ok = True
    method_used = "full_content"

    for file_path, content in model_patch.items():
        if not isinstance(content, str):
            result_files[file_path] = str(content)
            continue

        stripped = content.strip()
        is_diff = (stripped.startswith("---") or
                   stripped.startswith("diff ") or
                   stripped.startswith("@@"))

        if not is_diff:
            result_files[file_path] = content
            continue

        method_used = "diff_converted"
        original = buggy_files.get(file_path, "")
        if not original:
            all_ok = False
            continue

        fixed = apply_diff_by_text_match(original, content)
        if fixed is not None:
            result_files[file_path] = fixed
            continue

        fixed = apply_diff_with_patch(original, content)
        if fixed is not None:
            result_files[file_path] = fixed
            method_used = "diff_patched"
            continue

        all_ok = False

    if not all_ok or not result_files:
        diffs = [v for v in model_patch.values() if isinstance(v, str)]
        return '\n'.join(diffs), "raw_diff_fallback"

    return json.dumps(result_files), method_used


def evaluate_one(task, model_patch):
    rule_id = task['rule_id']
    project = task['project']
    target_file = task['target_file']
    commit_hash = task.get('commit_hash', '')
    buggy_files = task.get('buggy_files', {})

    payload, method = prepare_payload(model_patch, buggy_files)

    cmd = [
        "docker", "run", "--rm", "-i",
        DOCKER_IMAGE, "evaluate",
        rule_id, project, target_file,
    ]
    if commit_hash:
        cmd.append(commit_hash)

    try:
        proc = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True
        )
        stdout, stderr = proc.communicate(input=payload, timeout=600)
        return stdout.strip(), method, stderr.strip()[:300]
    except subprocess.TimeoutExpired:
        proc.kill()
        return "TIMEOUT", method, ""
    except Exception as e:
        return f"SYSTEM_ERR: {e}", method, ""


def load_datasets(dataset_type):
    truth_map = {}
    targets = [dataset_type] if dataset_type != "both" else ["arkts", "cpp"]
    for ds in targets:
        path = DATASET_MAP.get(ds)
        if path and os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                for t in json.load(f):
                    truth_map[t['instance_id']] = t
    print(f"  加载数据集: {len(truth_map)} 任务")
    return truth_map


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=["arkts", "cpp", "both"], default="both")
    parser.add_argument("--results", required=True)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--report", default=None, help="报告输出路径")
    args = parser.parse_args()

    if args.report is None:
        os.makedirs("logs", exist_ok=True)
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        base = os.path.splitext(os.path.basename(args.results))[0]
        args.report = f"logs/report_{base}_{ts}.txt"

    print("=" * 60)
    print(f"OH-Bench 实验 - 数据集: {args.dataset}")
    print("=" * 60)

    truth_map = load_datasets(args.dataset)
    if not truth_map:
        sys.exit(1)

    with open(args.results, 'r', encoding='utf-8') as f:
        predictions = json.load(f)
    print(f"  Agent 结果: {len(predictions)} 条\n")

    stats = {
        "total": 0, "matched": 0,
        "applied": 0, "strict_pass": 0,
        "eliminated": 0, "new_defect": 0,
        "linter_fail": 0, "syntax_fail": 0,
        "apply_error": 0, "timeout": 0, "error": 0,
    }
    method_stats = {}
    rule_results = defaultdict(lambda: {"total": 0, "pass": 0, "fail": 0, "error": 0, "secondary": 0})
    baseline_issues = []
    all_records = []

    print(f"{'ID':<15} | {'Result':<30} | {'Method':<18} | {'Rule'}")
    print("-" * 95)

    for pred in predictions:
        iid = pred.get('instance_id', '')
        task = truth_map.get(iid)
        stats["total"] += 1

        if not task:
            continue

        stats["matched"] += 1
        patch = pred.get('model_patch', pred.get('patch', ''))
        result, method, stderr = evaluate_one(task, patch)
        method_stats[method] = method_stats.get(method, 0) + 1

        rule = task['rule_id']
        rule_results[rule]['total'] += 1

        short_rule = rule.split('/')[-1][:28]
        print(f"{iid:<15} | {result:<30} | {method:<18} | {short_rule}")

        if args.verbose and stderr:
            print(f"{'':>15}   STDERR: {stderr[:150]}")

        if "target rule not found" in stderr:
            baseline_issues.append((iid, rule, stderr[:120]))

        all_records.append({"id": iid, "result": result, "method": method, "rule": rule})

        if "TIMEOUT" in result:
            stats["timeout"] += 1
            rule_results[rule]['error'] += 1
        elif "APPLY_ERROR" in result:
            stats["apply_error"] += 1
            rule_results[rule]['error'] += 1
        elif result.startswith("ERROR") or "SYSTEM_ERR" in result:
            stats["error"] += 1
            rule_results[rule]['error'] += 1
        else:
            stats["applied"] += 1
            if result.strip() == "PASS":
                stats["strict_pass"] += 1
                stats["eliminated"] += 1
                rule_results[rule]['pass'] += 1
            elif "SECONDARY_DEFECT" in result:
                stats["eliminated"] += 1
                stats["new_defect"] += 1
                rule_results[rule]['secondary'] += 1
            elif "LINTER_FAIL" in result:
                stats["linter_fail"] += 1
                rule_results[rule]['fail'] += 1
            elif "SYNTAX_FAIL" in result:
                stats["syntax_fail"] += 1
                rule_results[rule]['error'] += 1

    m = stats["matched"]
    report_lines = []

    def p(line=""):
        print(line)
        report_lines.append(line)

    p(f"\n{'='*80}")
    p(f"OH-Bench 评估报告")
    p(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    p(f"数据集: {args.dataset} | Agent: {os.path.basename(args.results)}")
    p(f"{'='*80}")

    if m > 0:
        p(f"\n## 1. 总体统计 ({m} 任务)")
        p(f"  补丁成功应用:   {stats['applied']}/{m} ({stats['applied']/m*100:.1f}%)")
        p(f"  告警消除:       {stats['eliminated']}/{m} ({stats['eliminated']/m*100:.1f}%)")
        p(f"  严格通过:     {stats['strict_pass']}/{m} ({stats['strict_pass']/m*100:.1f}%)")
        p(f"  ---")
        p(f"  仍有告警:       {stats['linter_fail']}/{m} ({stats['linter_fail']/m*100:.1f}%)")
        p(f"  二次缺陷:       {stats['new_defect']}/{m}")
        p(f"  语法错误:       {stats['syntax_fail']}/{m}")
        p(f"  补丁应用失败:   {stats['apply_error']}/{m} ({stats['apply_error']/m*100:.1f}%)")
        p(f"  超时:           {stats['timeout']}/{m}")
        p(f"  系统错误:       {stats['error']}/{m}")

        p(f"\n## 按规则统计")
        p(f"{'规则':<45} | {'总':>3} | {'PASS':>4} | {'FAIL':>4} | {'ERR':>3} | {'SEC':>3} | {'通过率':>6}")
        p("-" * 85)
        for rule in sorted(rule_results.keys()):
            rs = rule_results[rule]
            t = rs['total']
            pp = rs['pass']
            rate = f"{pp/t*100:.0f}%" if t > 0 else "N/A"
            short = rule.split('/')[-1][:43]
            p(f"{short:<45} | {t:>3} | {pp:>4} | {rs['fail']:>4} | {rs['error']:>3} | {rs['secondary']:>3} | {rate:>6}")

        easy = [r for r, s in rule_results.items() if s['total'] >= 3 and s['pass'] / s['total'] > 0.7]
        hard = [r for r, s in rule_results.items() if s['total'] >= 3 and s['pass'] / s['total'] < 0.2]
        medium = [r for r, s in rule_results.items() if s['total'] >= 3 and 0.2 <= s['pass'] / s['total'] <= 0.7]

        p(f"\n## 难度分析")
        p(f"  简单 (>70%通过): {len(easy)} 个规则")
        for r in easy:
            s = rule_results[r]
            p(f"    {r.split('/')[-1]}: {s['pass']}/{s['total']}")
        p(f"  中等 (20-70%通过): {len(medium)} 个规则")
        for r in medium:
            s = rule_results[r]
            p(f"    {r.split('/')[-1]}: {s['pass']}/{s['total']}")
        p(f"  困难 (<20%通过): {len(hard)} 个规则")
        for r in hard:
            s = rule_results[r]
            p(f"    {r.split('/')[-1]}: {s['pass']}/{s['total']}")

        p(f"\n## 区分度评价")
        if easy and hard:
            p(f"  数据集具有良好区分度: 简单{len(easy)} / 中等{len(medium)} / 困难{len(hard)}")
        elif len(set([len(easy) > 0, len(medium) > 0, len(hard) > 0])) >= 2:
            p(f"  数据集有一定区分度")
        else:
            p(f"  区分度可能不足")

        if baseline_issues:
            p(f"\n## Baseline 问题 ({len(baseline_issues)} 个)")
            p(f"以下任务基线扫描未找到目标规则，可能是数据集问题:")
            for iid, rule, msg in baseline_issues[:15]:
                p(f"  {iid}: {rule.split('/')[-1]}")

        ae_records = [r for r in all_records if 'APPLY_ERROR' in r['result']]
        if ae_records:
            p(f"\n## APPLY_ERROR 详情 ({len(ae_records)} 个)")
            ae_by_rule = defaultdict(int)
            for r in ae_records:
                ae_by_rule[r['rule']] += 1
            for rule, cnt in sorted(ae_by_rule.items(), key=lambda x: -x[1]):
                p(f"  {rule.split('/')[-1]:<40}: {cnt}")

        p(f"\n{'='*80}")

    # with open(args.report, 'w', encoding='utf-8') as f:
    #     f.write('\n'.join(report_lines))
    # print(f"\n 报告已保存: {args.report}")


if __name__ == "__main__":
    main()