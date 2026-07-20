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
| SWE-agent | 87.2 | 48.2 | 86.6 | 37.3 |
| OpenCode | 85.3 | 43.7 | 88.6 | 35.1 |
| Claude Code | 98.4 | 45.8 | 92.2 | 32.9 |
| ***LLMs (native input)*** | | | | |
| Gemini 2.5 | 78.0 | **51.1** | 96.9 | **39.3** |
| Claude Opus 4.5 | 90.1 | 46.6 | 99.2 | 33.2 |
| Claude Sonnet 4.5 | 92.7 | 45.3 | 97.2 | 36.8 |
| Kimi K2.5 | 80.9 | 41.9 | 97.8 | 36.8 |
| MiniMax M2.5 | 50.3 | 29.6 | 84.1 | 24.2 |

**Key takeaway:** No system exceeds 60% SPR on ArkTS or 45% on C/C++ — substantial headroom remains, and the dominant failure mode shifts between the two languages.

*(Note: We provide bootstrap resampling scripts in `tools/significance_testing/` to verify the statistical significance of these performance gaps).*

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


## Extensible Architecture

OH-Bench is designed as a continuously evolving infrastructure rather than a static dataset. It ensures future defect types can be integrated seamlessly via three non-breaking mechanisms: **Slot-Based Branches** (reusing Docker infrastructure), **Composable Annotations** (for dynamic metadata filtering), and **Semantic Versioning**.

**Empirical Validation:** We successfully added a 145-instance **Runtime Bug Prototype** to validate this architecture. Switching the evaluation engine from static-warning to runtime-bug repair required **zero changes** to the core Docker sandboxes—it merely took a **92-line adapter** (`run_eval_runtime.py`) to swap static rescans for native `hvigor` dynamic test execution.

---

## Directory Structure

```text
OH-Bench/
├── dataset/                     # Standardized JSON records
│   ├── main_benchmark/          # 741 verified static warnings (ArkTS & C/C++)
│   ├── extensibility/           # 145 Runtime Extensibility prototypes
│   └── generalization/          # HapRepair comparative subsets
├── evaluator/                   # Containerized evaluator engines
│   ├── container_scripts/       # Custom test/analysis oracles inside containers
│   ├── docker/                  # Dockerfiles for GN/Ninja & Hvigor sandboxes
│   ├── run_eval_static.py       # Core orchestrator for Static Warnings
│   └── run_eval_runtime.py      # 92-line adapter for Runtime Errors
├── tools/                       # Auxiliary scripts & rigorous validation
│   ├── data_cleaning/           # Scripts for noise filtering and curation
│   ├── manual_audit/            # Audit records (κ=0.96) & evasion defense logs
│   └── significance_testing/    # Bootstrap resampling scripts for model comparisons
└── results/                     # Baseline outputs and comprehensive reports
```

---

## Rigorous Validation (Manual Audit)

To ensure maximum reliability and counter the conservative nature of strict metrics like SPR, the OH-Bench dataset underwent rigorous manual verification, fully transparent in this repository (`tools/audit_and_stats/`):

1. **Instance-Quality Audit**: 100 instances (50 per language) were independently verified to confirm they describe genuine, repairable defects. (2 disagreements were successfully resolved by consensus).
2. **Oracle-Verdict Audit**: 200 instances (100 oracle-FAIL and 100 oracle-PASS) were manually re-judged by two authors. The inter-rater agreement achieved a **Cohen's $\kappa = 0.96$**.
3. **Statistical Confidence & Evasion Defense**: In the oracle-FAIL stratum, the observed false-negative rate was 1/100 (Clopper-Pearson 95% upper bound of 5.4%). In the oracle-PASS stratum, **zero false positives** were found (95% upper bound of 3.6%). 
   * *Note on strictness:* Fixes employing "evasions" (e.g., inline suppression directives or wholesale deletion of the flagged construct) were strictly counted as false positives. Zero such evasions appeared, as our project-wide rebuild oracle effectively breaks compilation upon blind deletions.

---

## Contributing & Community

As OpenHarmony rapidly expands into consumer and IoT devices, a single research group cannot capture all defect typologies. **We welcome contributions from the community to expand OH-Bench.**

Here are a few ways you can get involved:
* **Evaluate Your Models**: Benchmark your custom LLMs or agents using our rigorous environment.
* **Submit Runtime Bugs**: Use our extensible JSON schema to contribute new dynamic bugs and native tests.
* **Expand the Taxonomy**: Leverage our slot-based architecture to add entirely new branches (e.g., *Security Vulnerabilities*, *Build Failures*), reusing our existing toolchain sandboxes.

---

## Citation

```bibtex
@inproceedings{ohbench2027icse,
  title     = {OH-Bench: A Cross-Language, Repository-Level Benchmark for Warning Repair on OpenHarmony},
  author    = {Anonymous},
  booktitle = {Proceedings of ICSE 2027},
  year      = {2027},
}
```

## License & Double-Blind Compliance

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

In compliance with the **Double-Blind Review Policy**, all author identities, email addresses, and organizational affiliations have been strictly omitted from this repository, datasets, and scripts. All toolchains and baseline records have been fully anonymized.
