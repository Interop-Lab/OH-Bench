# OH-Bench: A Cross-Language, Repository-Level Benchmark for Warning Repair on OpenHarmony

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Version](https://img.shields.io/badge/Version-1.0-green.svg)
![OpenHarmony](https://img.shields.io/badge/Ecosystem-OpenHarmony-000000.svg)

**OH-Bench** is the first repository-level, cross-language, containerized benchmark designed specifically for Automated Program Repair (APR) within the **OpenHarmony** ecosystem. 

Beyond a standard dataset, OH-Bench serves as an **extensible evaluation framework** to rigorously test the capabilities of Large Language Models (LLMs) and Autonomous Agents in resolving real-world, cross-file defects under complex industrial build systems (GN/Ninja, Hvigor).

---

## Why OH-Bench? (The Ecosystem Gap)

The OpenHarmony ecosystem presents unique challenges that mainstream benchmarks like SWE-bench (Python) or Defects4J (Java) cannot address:
- **C1: Multi-language codebase.** OpenHarmony combines C/C++ kernel and system-service code with ArkTS framework and application code. These language families have different toolchains, APIs, and debugging workflows.

- **C2: Cross-file and cross-component dependencies.** Repairs frequently require coordinated changes across files and components: **35.1%** of OH-Bench ArkTS instances (134/382) require edits to at least two files.

- **C3: Specialized build infrastructure.** OpenHarmony uses **GN/Ninja** for C/C++ and **Hvigor** for ArkTS, rather than conventional package-manager workflows. Reproducible evaluation therefore requires the exact project toolchain and build configuration.

- **C4: Platform-specific framework semantics.** ArkUI lifecycle callbacks, reactive state decorators such as `@State` and `@Link`, and NAPI bindings introduce OpenHarmony-specific constraints that are uncommon in general-purpose training data.

### Comparison with Existing Benchmarks

| Feature | OH-Bench | SWE-bench | Defects4J | HapRepair |
| :--- | :---: | :---: | :---: | :---: |
| Instances | **741** | 2,294 | 835 | 1,952 |
| Repositories | **39** | 12 | 17 | 13 |
| Languages | **3** (ArkTS, C, C++) | 1 (Python) | 1 (Java) | 1 (ArkTS) |
| Cross-file repair | ✓ | ✓ | ✓ | ✗ |
| Docker environment | ✓ | ✓ | ✓ | ✗ |
| Extensible taxonomy | ✓ | ✗ | ✗ | ✗ |

## Leaderboard & Discriminability

OH-Bench employs a **Three-Level Competence Framework** (Format, Semantic, and Holistic competence), operationalized through four complementary metrics:

| Metric | Definition |
| :--- | :--- |
| **PAR** (Patch Apply Rate) | The generated patch is syntactically well-formed and applies cleanly to the codebase. |
| **WER** (Warning Elimination Rate) | The target static warning is eliminated after applying the patch. |
| **SDR** (Secondary Defect Rate, ↓) | The patch introduces *new* warnings elsewhere in the project (lower is better). |
| **SPR** (Strict Pass Rate) | All three conditions hold simultaneously: patch applies, warning eliminated, no secondary defects. |

The benchmark is deliberately calibrated to expose the capability ceilings of frontier models. As shown below, even state-of-the-art LLMs and iterative agents struggle to achieve a high SPR across both languages.

### Main Results (Selected)
*LLM rows use the **native input** configuration (raw warning context only, without retrieval augmentation); see the paper and `results/` for RAG-augmented configurations and full WER/SDR breakdowns.*

| System | ArkTS PAR | ArkTS SPR | C/C++ PAR | C/C++ SPR |
| :--- | :---: | :---: | :---: | :---: |
| ***Agents (backend: Claude Sonnet 4.5)*** | | | | |
| Moatless | 98.4 | **58.4** | 93.3 | **42.1** |
| Agentless | 96.1 | 55.2 | 96.9 | 31.2 |
| Claude Code | 98.4 | 45.8 | 92.2 | 32.9 |
| SWE-agent | 87.2 | 48.2 | 86.6 | 37.3 |
| ***LLMs (native input)*** | | | | |
| Gemini 2.5 | 78.0 | **51.1** | 96.9 | **39.3** |
| Opus 4.5 | 90.1 | 46.6 | 99.2 | 33.2 |
| Sonnet 4.5 | 92.7 | 45.3 | 97.2 | 36.8 |
| Kimi K2.5 | 80.9 | 41.9 | 97.8 | 36.8 |
| DeepSeek-R1 | 79.8 | 50.5 | 90.3 | 34.5 |
| Qwen2.5-32B | 45.8 | 22.3 | 68.3 | 24.0 |

**Key takeaway:** No system exceeds 60% SPR on ArkTS or 45% on C/C++ — substantial headroom remains, and the dominant failure mode shifts between the two languages.

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
