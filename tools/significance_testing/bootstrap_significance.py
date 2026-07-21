#!/usr/bin/env python3
"""
Bootstrap Significance Testing for OH-Bench
Calculates 95% Confidence Intervals (CI) and P-values for model performance comparisons.
Automatically detects whether to use Paired or Independent statistical testing.
"""

import numpy as np
import re
from pathlib import Path

# ==============================================================================
# Configuration
# ==============================================================================
RESULTS_DIR = Path("../results")
NUM_ITERATIONS = 10000

TASKS = [
    (
        "arkts_moatless_no_examples.report",
        "arkts_plan2_gemini-2.5-flash_hybrid_small.report",
        "ArkTS: Moatless vs Gemini"
    ),
]

# ==============================================================================
# Core Parsing & Statistical Engine
# ==============================================================================

def parse_eval_log(file_path: Path) -> dict:
    """
    Parses the standard OH-Bench evaluation report text.
    Extracts instance IDs (e.g., OH_0001, CPP_0001) and sets 1 for PASS, 0 otherwise.
    """
    if not file_path.exists():
        print(f"[Error] Log file not found: {file_path}")
        return {}

    data = {}
    pattern = re.compile(r'^(OH_\d+|CPP_\d+)\s+\|\s+([A-Z_]+)\s+\|')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = pattern.match(line.strip())
            if match:
                iid = match.group(1).strip()
                signal = match.group(2).strip()
                data[iid] = 1 if signal == "PASS" else 0
                
    return data

def run_bootstrap_smart(file_a: str, file_b: str, label: str):
    path_a = RESULTS_DIR / file_a
    path_b = RESULTS_DIR / file_b
    
    res_a = parse_eval_log(path_a)
    res_b = parse_eval_log(path_b)
    
    if not res_a or not res_b:
        return

    common_ids = set(res_a.keys()) & set(res_b.keys())
    
    if len(common_ids) > 0:
        # --- Paired Test ---
        all_ids = sorted(list(set(res_a.keys()) | set(res_b.keys())))
        mode = "Paired (Same Problems)"
        n_samples = len(all_ids)
        
        a_outcomes = np.array([res_a.get(i, 0) for i in all_ids])
        b_outcomes = np.array([res_b.get(i, 0) for i in all_ids])
        
        spr_a = np.mean(a_outcomes) * 100
        spr_b = np.mean(b_outcomes) * 100
        
        boot_diffs = np.zeros(NUM_ITERATIONS)
        for i in range(NUM_ITERATIONS):
            idx = np.random.choice(n_samples, size=n_samples, replace=True)
            boot_diffs[i] = (np.mean(b_outcomes[idx]) - np.mean(a_outcomes[idx])) * 100

    else:
        # --- Independent Test ---
        mode = "Independent (Different Problems)"
        a_outcomes = np.array(list(res_a.values()))
        b_outcomes = np.array(list(res_b.values()))
        n_a, n_b = len(a_outcomes), len(b_outcomes)
        n_samples = f"A={n_a}, B={n_b}"
        
        spr_a = np.mean(a_outcomes) * 100
        spr_b = np.mean(b_outcomes) * 100
        
        boot_diffs = np.zeros(NUM_ITERATIONS)
        for i in range(NUM_ITERATIONS):
            boot_a = np.random.choice(a_outcomes, size=n_a, replace=True)
            boot_b = np.random.choice(b_outcomes, size=n_b, replace=True)
            boot_diffs[i] = (np.mean(boot_b) - np.mean(boot_a)) * 100

    observed_diff = spr_b - spr_a
    ci_lower = np.percentile(boot_diffs, 2.5)
    ci_upper = np.percentile(boot_diffs, 97.5)
    
    if observed_diff > 0:
        p_val = np.mean(boot_diffs <= 0)
    else:
        p_val = np.mean(boot_diffs >= 0)
        
    is_significant = ci_lower > 0 or ci_upper < 0

    print(f"\n[{label}]")
    print(f"  Mode           : {mode}")
    print(f"  Sample Size    : {n_samples}")
    print(f"  System A       : {spr_a:.1f}%")
    print(f"  System B       : {spr_b:.1f}%")
    print(f"  Observed Diff  : {observed_diff:+.2f} pp")
    print(f"  95% CI         : [{ci_lower:+.2f}, {ci_upper:+.2f}] pp")
    print(f"  P-value        : {p_val:.4f}")
    
    if is_significant:
        print("  Result         : 【Significant】")
    else:
        print("  Result         : 【Not Significant】")

if __name__ == "__main__":
    print(f"Executing {NUM_ITERATIONS:,} Bootstrap Iterations (Pure Random Mode)...")
    for fa, fb, lab in TASKS:
        run_bootstrap_smart(fa, fb, lab)
