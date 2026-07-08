# OH-Bench Datasets

This directory contains the datasets used in our evaluation. The data is organized into three subdirectories based on their experimental scope.

## 1. Main Benchmark (`/main_benchmark`)
The core OH-Bench dataset containing 741 high-quality static analysis warnings.
* `ohbench_arkts_v1.0.json` (382 ArkTS instances)
* `ohbench_cpp_v1.0.json` (359 C/C++ instances)

**Schema (Static Analysis Format):**
* `instance_id`: Unique identifier (e.g., `OH_0001`, `CPP_0001`).
* `rule_id`: The targeted CodeLinter/Cppcheck rule.
* `commit_hash`: The specific Git commit snapshot required for reproduction.
* `buggy_files`: A dictionary mapping file paths to their complete buggy source code.
* `input_snippet`: The precise code context for LLM prompting.

## 2. Comparative Subset (`/comparative_subset`)
* `haprepair_like_subset.json`: A curated subset of ArkTS instances extracted from the main OH-Bench dataset.

**Usage:** 
This subset is specifically filtered to mirror the rule distribution and scope evaluated in the prior HapRepair system. Sharing the identical schema with the Main Benchmark, it is provided for comparative studies—allowing researchers to observe the performance gap between a narrower, rule-constrained scenario and the full, rigorous OH-Bench evaluation.

## 3. Extensibility Prototype (`/extensibility`)
* `runtime_extensibility_145.json`: A prototype dataset containing 145 verified OpenHarmony runtime bugs.

**Schema (Runtime Test Format):**
This dataset extends the core schema to support dynamic execution and test-driven repair:
* `bug_id`: Unique identifier (e.g., `openharmony-sig-ohos_axios-143`).
* `repo_url`: The remote Git repository URL.
* `buggy_commit` & `fixed_commit`: Hashes for establishing the buggy state and referencing the oracle patch.
* `test_command`: The native build/test command required to trigger the bug (e.g., `./hvigorw test --mode localTest --no-daemon`).

**Usage:**
Provided to demonstrate the framework's extensibility. It empirically validates that the underlying containerized evaluation engine can be effortlessly adapted from static-warning repair to runtime-bug repair by simply substituting a lightweight native test execution adapter.