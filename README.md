# OH-Bench: Competence-Aware Program Repair in OpenHarmony

This repository contains the replication package for **OH-Bench**, a comprehensive program repair benchmark designed specifically for the OpenHarmony ecosystem. It evaluates state-of-the-art LLMs and autonomous coding agents under a rigorous **Three-Level Competence Framework** (Format, Semantic, and Holistic competence).

---

## Prerequisites & Environmental Setup

Before executing the evaluation runners, ensure your host environment meets the following requirements:

### Host Requirements
*   **Operating System**: Linux (Ubuntu 20.04 LTS or later recommended)
*   **Python**: Version 3.8 or later
*   **Docker**: Installed and running (ensure the current user has permissions to run docker commands without `sudo`).

### Sandbox Image Assets (Omitted from Git via .gitignore)
The local Docker image `oh-bench-evaluator:latest` relies on a few heavy assets. Before triggering `docker build`, ensure you have retrieved the open-source repositories and verified compiler archives:
1.  **Compiler & Linter SDKs**: Placed at `evaluator/docker/tools_archive/codelinter` and `evaluator/docker/tools_archive/ohos-sdk`.
2.  **Benchmark Targets**: Placed at `repositories_slim/` (can be fully automated via Step 1 below).

---

## Directory Structure

```text
OH-Bench/
├── dataset/                     # Standardized evaluation JSON records (ArkTS, C++, Runtime)
├── evaluator/                   # Containerized sandbox evaluator engines
│   ├── docker/                  # Dockerfiles to build static/runtime sandboxes
│   ├── container_scripts/       # Custom test/analysis oracles inside containers
│   ├── run_eval_static.py       # Static analysis host-side orchestrator
│   └── run_eval_runtime.py      # Runtime test host-side orchestrator
├── tools/                       # Developer utility, data mining, and setup scripts
└── results/                     # Baseline execution outputs (.json) and reports (.report)
```

---

## Quick Start Setup

To preserve scientific transparency and keep the repository lightweight, we do not bundle third-party code. Instead, we provide an automatic recovery engine.

### Step 1: Restore the Benchmark Repositories

Run the following script to automatically clone the exact versions of the 39 target OpenHarmony repositories from GitCode and checkout to their historical commits:

```bash
python3 tools/download_repos.py
```

*This will safely populate the `repositories_slim/` directory on your host. 

### Step 2: Build the Static Evaluation Sandbox

Build the isolated Docker execution sandbox locally:

```bash
docker build -t oh-bench-evaluator:latest -f evaluator/docker/Dockerfile.static .
```

---

## Running Evaluations

OH-Bench supports two distinct evaluation runners to certify program repair candidates:

### 1. Static Analysis Evaluator (`run_eval_static.py`)
This engine mounts the target repository into an isolated sandbox, applies the generated patch, and triggers a full project rescan using Codelinter/Cppcheck. It verifies whether the patch eliminates target violations without introducing new ones.

To evaluate any static predictions (e.g., Gemini 2.5 Flash on C++):
```bash
python3 evaluator/run_eval_static.py \
  --dataset cpp \
  --results results/cpp/plan2_gemini-2.5-flash_dependency_only.json
```

**Key Command-Line Arguments:**
*   `--dataset`: Either `arkts` or `cpp`.
*   `--results`: Path to your agent-generated JSON output.
*   `--start` / `--end`: Slice specific instance evaluation ranges (e.g., `--start OH_0001 --end OH_0050`).
*   `--isolated`: Runs a fresh container for each instance (safer but slower).
*   `--verbose`: Print container stderr outputs in real-time.

### 2. Runtime Defect Evaluator (`run_eval_runtime.py`)
This engine evaluates runtime program behavior. It compiles the patched codebase and executes dynamic test suites to verify that the runtime defect or functional crash has been successfully resolved.

To evaluate runtime predictions:
```bash
python3 evaluator/run_eval_runtime.py \
  --results results/arkts/runtime_predictions.json
```

---

## Output Interpretations & Reports

### Evaluation Signals (Instance-Level)
For each evaluated task, the engine prints a normalized signal:
*   `PASS`: The target violation/defect is resolved, and no regressions are introduced.
*   `LINTER_FAIL`: The target static warning still persists after patch application.
*   `TEST_FAIL`: The dynamic test suite failed to execute successfully.
*   `SECONDARY_DEFECT`: The target warning is eliminated, but new warnings are introduced elsewhere.
*   `SYNTAX_FAIL`: The patch introduced compilation or syntax errors.
*   `APPLY_ERROR`: The patch format is corrupted and cannot be applied cleanly.
*   `TIMEOUT`: The evaluation process exceeded the execution limit (600s).

### Evaluation Reports
Upon completion, the runners automatically generate a comprehensive, publication-aligned summary report.
*   **Directory**: Saved automatically under the `logs/` directory.
*   **Format**: `logs/report_<predictions_filename>_<timestamp>.txt`.
*   **Contents**: Includes global statistics ($\mathrm{PAR}$, $\mathrm{WER}$, $\mathrm{SDR}$, $\mathrm{SPR}$), conversion method distribution, difficulty analysis, and per-rule breakdown tables.

---

## License & Double-Blind Compliance

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

In compliance with the **Double-Blind Review Policy**, all author identities, email addresses, and organizational affiliations have been strictly omitted from this repository, datasets, and scripts. All toolchains and baseline records have been fully anonymized.