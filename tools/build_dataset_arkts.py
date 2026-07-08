#!/usr/bin/env python3
import csv
import json
import os
import re
import sys
import hashlib
import argparse
import subprocess
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Any, Set

# ============================================================================
# Configuration & Domain Rules
# ============================================================================

TARGET_RULES = {
    "@performance/hp-arkui-use-reusable-component": 1800,
    "@performance/hp-arkui-set-cache-count-for-lazyforeach-grid": 1800,
    "@performance/hp-arkui-no-state-var-access-in-loop": 1800,
    "@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator": 1800,
    "@performance/hp-arkui-use-local-var-to-replace-state-var": 1800,
    "@performance/hp-arkui-use-object-link-to-replace-prop": 1800,
    "@performance/hp-arkui-use-grid-layout-options": 1800,
    "@performance/hp-arkui-use-transition-to-replace-animateto": 1800,
    "@performance/hp-arkui-suggest-use-effectkit-blur": 1800,
    "@performance/hp-arkui-no-func-as-arg-for-reusable-component": 1800,
    "@performance/hp-arkui-use-onAnimationStart-for-swiper-preload": 1800,
    "@performance/hp-arkui-load-on-demand": 1800,
    "@previewer/mandatory-default-value-for-local-initialization": 1800,
    "@performance/foreach-args-check": 1800,
    "@performance/high-frequency-log-check": 1800,
    "@performance/hp-arkts-no-use-any-export-other": 1800,
    "@performance/hp-arkts-no-use-any-export-current": 1800,
    "@hw-stylistic/quotes": 1800,
    "@hw-stylistic/no-tabs": 1800,
    "@hw-stylistic/operator-linebreak": 1800,
    "@hw-stylistic/space-before-blocks": 1800,
    "@hw-stylistic/max-len": 1800,
    "@hw-stylistic/no-multi-spaces": 1800,
    "@hw-stylistic/space-infix-ops": 1800
}

MAX_CODE_LINES = 300
MAX_CODE_CHARS = 25000
MAX_TOTAL = 1800

RULE_CATEGORIES = {
    "A": ["@performance/hp-arkui"],
    "B": ["@previewer", "foreach-args", "log-check"],
    "C": ["export"],
    "D": ["@hw-stylistic"]
}

FILE_INDEX: Dict[str, List[str]] = {}


# ============================================================================
# Syntactic & Structural Analysis Utilities
# ============================================================================

def get_category(rule_id: str) -> str:
    """Classifies rule ID into domain categories (A, B, C, D)."""
    for cat, keywords in RULE_CATEGORIES.items():
        for kw in keywords:
            if kw in rule_id:
                return cat
    return "Other"


def count_braces(text: str) -> Tuple[int, int]:
    """Counts open and close braces while ignoring comments and strings."""
    text = re.sub(r'/\*[\s\S]*?\*/', ' ', text)
    text = re.sub(r'//[^\n]*', ' ', text)
    text = re.sub(r'`[^`]*`', '""', text)
    text = re.sub(r'"(?:[^"\\]|\\.)*"', '""', text)
    text = re.sub(r"'(?:[^'\\]|\\.)*'", "''", text)
    return text.count('{'), text.count('}')


def ensure_balanced(code: str) -> Tuple[str, bool]:
    """Enforces brace balance by appending wrapping brackets if needed."""
    ob, cb = count_braces(code)
    if ob == cb:
        return code, True
    if ob > cb:
        code = code.rstrip() + '\n' + ('}\n' * (ob - cb))
    else:
        code = ('{\n' * (cb - ob)) + code
    return code, True


def determine_code_type(code: str) -> str:
    """Heuristically identifies ArkTS code construction block types."""
    if not code:
        return "context"

    first_line = code.strip().split('\n')[0].strip()

    if re.match(r'^@(Component|Reusable|Entry)', first_line):
        return "component"

    if first_line.startswith('export'):
        return "export"

    method_patterns = [
        r'^@(Builder|Styles|Extend)',
        r'^(private|public|protected)\s+',
        r'^(async\s+)?function\s+',
        r'^build\s*\(',
        r'^aboutTo(Appear|Disappear)\s*\(',
    ]
    for p in method_patterns:
        if re.match(p, first_line):
            return "method"

    ui_components = ['List', 'Grid', 'Column', 'Row', 'Stack', 'Flex', 'Scroll', 'Swiper', 'Tabs']
    for comp in ui_components:
        if first_line.startswith(comp + '(') or first_line.startswith(comp + ' ('):
            return "ui_block"

    return "context"


def validate_code_start(code: str, rule_id: str) -> Tuple[bool, Optional[str]]:
    """Validates if code starting token is logical for static code repair."""
    if not code or len(code.strip()) < 20:
        return False, "Too short"

    first_line = code.strip().split('\n')[0].strip()
    bad_starts = ['return ', ');', '});', 'else {', 'else{', 'catch', 'finally', 'case ', 'default:']
    for bs in bad_starts:
        if first_line.startswith(bs):
            return False, f"Bad start: {bs}"

    return True, None


def validate_rule_context(code: str, rule_id: str) -> Tuple[bool, Optional[str]]:
    """Ensures rule-specific syntactic markers are preserved in the snippet."""
    if "access-in-loop" in rule_id:
        loop_patterns = [r'\bfor\s*\(', r'\bwhile\s*\(', r'\.forEach\s*\(', r'\.map\s*\(', r'\bForEach\s*\(']
        if not any(re.search(p, code) for p in loop_patterns):
            return False, "Missing loop context"

    if "lazyforeach" in rule_id.lower() or "stringify" in rule_id.lower():
        if 'LazyForEach' not in code:
            return False, "Missing LazyForEach"

    if "export" in rule_id.lower() and "@hw-stylistic" not in rule_id:
        if 'export' not in code:
            return False, "Missing export"

    return True, None


# ============================================================================
# Git Repository & Path Resolution Managers
# ============================================================================

class GitRepoManager:
    """Safely retrieves historical file states from Git version control."""
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.repo_paths: Dict[str, str] = {}
        self.file_cache: Dict[Tuple[str, str, str], str] = {}
        self._discover_repos()

    def _discover_repos(self):
        if not os.path.exists(self.project_root):
            return
        for item in os.listdir(self.project_root):
            item_path = os.path.join(self.project_root, item)
            if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, '.git')):
                self.repo_paths[item] = item_path

    def get_file(self, repo_name: str, commit_hash: str, file_path: str) -> Optional[str]:
        cache_key = (repo_name, commit_hash, file_path)
        if cache_key in self.file_cache:
            return self.file_cache[cache_key]

        if repo_name not in self.repo_paths:
            return None

        repo_path = self.repo_paths[repo_name]
        git_file_path = file_path.replace("\\", "/")

        try:
            result = subprocess.run(
                ['git', 'show', f'{commit_hash}:{git_file_path}'],
                cwd=repo_path,
                capture_output=True, text=True, timeout=30,
                encoding='utf-8', errors='ignore'
            )
            if result.returncode == 0:
                self.file_cache[cache_key] = result.stdout
                return result.stdout
        except subprocess.SubprocessError:
            pass
        return None

    def verify_commit(self, repo_name: str, commit_hash: str) -> bool:
        if repo_name not in self.repo_paths:
            return False
        repo_path = self.repo_paths[repo_name]
        try:
            result = subprocess.run(
                ['git', 'cat-file', '-t', commit_hash],
                cwd=repo_path,
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0 and 'commit' in result.stdout
        except subprocess.SubprocessError:
            return False


def build_file_index(root: str) -> None:
    """Builds global system search index to resolve moved/renamed files."""
    global FILE_INDEX
    for r, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'build', 'dist', 'oh_modules']]
        for f in files:
            if f.endswith(('.ets', '.ts', '.js')):
                FILE_INDEX.setdefault(f, []).append(os.path.join(r, f))


def find_file(path: str, root: str) -> Optional[str]:
    """Resolves correct filepath relative to Workspace."""
    path = os.path.normpath(path)
    if os.path.exists(path):
        return path

    parts = path.replace("\\", "/").split("/")
    for i in range(len(parts)):
        test = os.path.join(root, *parts[i:])
        if os.path.exists(test):
            return test

    fname = os.path.basename(path)
    if fname in FILE_INDEX:
        cands = FILE_INDEX[fname]
        if len(cands) == 1:
            return cands[0]
        orig_parts = set(parts[-5:])
        best, best_score = None, 0
        for c in cands:
            score = len(orig_parts & set(c.replace("\\", "/").split("/")[-5:]))
            if score > best_score:
                best, best_score = c, score
        return best
    return None


def parse_path_from_csv(file_path: str, project_root: str, repository: str = "") -> Tuple[str, str]:
    """Extracts project name and relative path from reported violation paths."""
    file_path = os.path.normpath(file_path)

    if repository:
        file_path_normalized = file_path.replace("\\", "/")
        repo_marker = f"/{repository}/"
        if repo_marker in file_path_normalized:
            idx = file_path_normalized.find(repo_marker)
            file_in_repo = file_path_normalized[idx + len(repo_marker):]
            return repository, file_in_repo

        try:
            rel = os.path.relpath(file_path, os.path.join(project_root, repository))
            return repository, rel.replace("\\", "/")
        except ValueError:
            pass

    try:
        rel = os.path.relpath(file_path, project_root).replace("\\", "/")
    except ValueError:
        rel = file_path.replace("\\", "/")

    parts = rel.split("/")
    if len(parts) >= 2:
        return parts[0], "/".join(parts[1:])
    return "", rel


# ============================================================================
# Core Extraction Logics
# ============================================================================

def find_component_range(lines: List[str], target_idx: int) -> Tuple[Optional[int], Optional[int]]:
    """Identifies bounding indices of `@Component` decorator structure."""
    n = len(lines)
    start = -1
    for i in range(min(target_idx, n - 1), max(0, target_idx - 300), -1):
        if re.match(r'^\s*@(Component|Reusable|Entry)', lines[i]):
            start = i
            break

    if start < 0:
        return None, None

    ob, cb = 0, 0
    first = False
    end = start

    for i in range(start, min(n, start + 250)):
        o, c = count_braces(lines[i])
        ob += o
        cb += c
        end = i
        if ob > 0:
            first = True
        if first and ob == cb and ob > 0:
            break

    while end < target_idx and end < n - 1:
        end += 1
        o, c = count_braces(lines[end])
        ob += o
        cb += c

    while ob > cb and end < n - 1 and end < start + 300:
        end += 1
        o, c = count_braces(lines[end])
        ob += o
        cb += c

    return start, end + 1


def find_method_range(lines: List[str], target_idx: int) -> Tuple[int, int]:
    """Identifies boundaries of functions/methods containing violation."""
    n = len(lines)
    patterns = [
        r'^\s*@(Builder|Styles|Extend)',
        r'^\s*(private|public|protected)?\s*(static)?\s*(async\s+)?\w+\s*\(',
        r'^\s*(export\s+)?(async\s+)?function\s+',
        r'^\s*build\s*\(',
        r'^\s*aboutTo',
    ]

    start = target_idx
    for i in range(min(target_idx, n - 1), max(0, target_idx - 100), -1):
        for p in patterns:
            if re.match(p, lines[i]):
                start = i
                break
        if start != target_idx:
            break

    if start == target_idx:
        start = max(0, target_idx - 20)

    ob, cb = 0, 0
    first = False
    end = start

    for i in range(start, min(n, start + 150)):
        o, c = count_braces(lines[i])
        ob += o
        cb += c
        end = i
        if ob > 0:
            first = True
        if first and ob == cb and ob > 0:
            break

    while end < target_idx and end < n - 1:
        end += 1

    return start, end + 1


def find_loop_context(lines: List[str], target_idx: int) -> Tuple[int, int]:
    """Identifies the closest outer loop containing the target violation index."""
    n = len(lines)
    loop_patterns = [r'^\s*for\s*\(', r'^\s*while\s*\(', r'\.forEach\s*\(', r'\bForEach\s*\(']
    start = target_idx

    for i in range(min(target_idx, n - 1), max(0, target_idx - 50), -1):
        for p in loop_patterns:
            if re.search(p, lines[i]):
                start = i
                break
        if start != target_idx:
            break

    if start == target_idx:
        start = max(0, target_idx - 15)

    ob, cb = 0, 0
    end = start

    for i in range(start, min(n, target_idx + 30)):
        o, c = count_braces(lines[i])
        ob += o
        cb += c
        end = i
        if ob > 0 and ob == cb:
            break

    return start, end + 1


def extract_code(content: str, target_line: int, rule_id: str) -> Tuple[Optional[str], int, int, str]:
    """Extracts semantic slices wrapping around violating index."""
    if not content:
        return None, 0, 0, "context"

    lines = content.splitlines(keepends=True)
    if lines and not lines[-1].endswith('\n'):
        lines[-1] += '\n'

    n = len(lines)
    idx = max(0, min(target_line - 1, n - 1))

    if "export" in rule_id and "@hw-stylistic" not in rule_id:
        start = max(0, idx - 5)
        end = min(n, idx + 10)
        code = "".join(lines[start:end])
        code, _ = ensure_balanced(code)
        return code, start + 1, end, "export"

    if "@hw-stylistic" in rule_id:
        start = max(0, idx - 25)
        end = min(n, idx + 30)
        code = "".join(lines[start:end])
        code, _ = ensure_balanced(code)
        code_type = determine_code_type(code)
        return code, start + 1, end, code_type

    if "access-in-loop" in rule_id:
        start, end = find_loop_context(lines, idx)
        code = "".join(lines[start:end])
        code, _ = ensure_balanced(code)
        valid, _ = validate_rule_context(code, rule_id)
        if not valid:
            start = max(0, idx - 30)
            end = min(n, idx + 40)
            code = "".join(lines[start:end])
            code, _ = ensure_balanced(code)
        code_type = determine_code_type(code)
        return code, start + 1, end, code_type

    comp_range = find_component_range(lines, idx)
    if comp_range[0] is not None:
        start, end = comp_range # type: ignore
        code = "".join(lines[start:end])
        code, _ = ensure_balanced(code)
        if len(code) < MAX_CODE_CHARS:
            code_type = determine_code_type(code)
            return code, start + 1, end, code_type

    meth_range = find_method_range(lines, idx)
    if meth_range[0] is not None:
        start, end = meth_range
        code = "".join(lines[start:end])
        code, _ = ensure_balanced(code)
        if len(code) < MAX_CODE_CHARS:
            code_type = determine_code_type(code)
            return code, start + 1, end, code_type

    start = max(0, idx - 40)
    end = min(n, idx + 50)
    code = "".join(lines[start:end])
    code, _ = ensure_balanced(code)
    code_type = determine_code_type(code)
    return code, start + 1, end, code_type


def get_code_signature(code: str) -> str:
    """Returns normalized format-free signature for robust code deduplication."""
    clean = re.sub(r'//.*', '', code)
    clean = re.sub(r'/\*.*?\*/', '', clean, flags=re.DOTALL)
    clean = re.sub(r'\s+', '', clean)
    return clean


def get_hash(code: str) -> str:
    """Returns MD5 hash value of code signature."""
    sig = get_code_signature(code)
    return hashlib.md5(sig[:500].encode()).hexdigest()


# ============================================================================
# Main Processing Pipeline Class
# ============================================================================

class ArkTSDatasetProcessor:
    """Processes, filters, and formats collected CSV warnings into standard JSON."""
    def __init__(self, root: str, git: GitRepoManager):
        self.root = root
        self.git = git
        self.counts: Dict[str, int] = defaultdict(int)
        self.total = 0
        self.seen_exact_loc: Set[Tuple[str, int, str]] = set()
        self.seen_hash_per_rule: Dict[str, Set[str]] = defaultdict(set)
        self.stats: Dict[str, int] = defaultdict(int)
        self.data: List[Dict[str, Any]] = []

    def is_full(self, rule: str) -> bool:
        return self.counts[rule] >= TARGET_RULES.get(rule, 0)

    def all_done(self) -> bool:
        return self.total >= MAX_TOTAL

    def process(self, rec: Dict[str, str]) -> bool:
        self.stats["total"] += 1

        rule = rec.get('Rule_ID') or rec.get('RuleID') or ''
        if rule not in TARGET_RULES:
            return False

        if self.is_full(rule):
            self.stats["skip_full"] += 1
            return False

        path = rec.get('File_Path') or rec.get('FilePath') or ''
        if not path:
            return False

        commit = rec.get('Commit_Hash') or rec.get('CommitHash') or ''
        repository = rec.get('Repository') or ''
        repo_name, file_in_repo = parse_path_from_csv(path, self.root, repository)

        try:
            rel = os.path.relpath(path, self.root).replace("\\", "/")
        except ValueError:
            rel = path.replace("\\", "/")

        proj = repository or repo_name or rel.split("/")[0]

        try:
            line = int(rec.get('Line_No') or rec.get('Line') or 1)
        except ValueError:
            line = 1

        exact_loc_key = (rel, line, rule)
        if exact_loc_key in self.seen_exact_loc:
            self.stats["skip_exact_dup"] += 1
            return False

        content = None
        git_ok = False

        if self.git and repo_name and commit:
            if self.git.verify_commit(repo_name, commit):
                content = self.git.get_file(repo_name, commit, file_in_repo)
                if content:
                    git_ok = True

        if not content:
            resolved = find_file(path, self.root)
            if resolved:
                try:
                    with open(resolved, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                except IOError:
                    pass

        if not content:
            self.stats["skip_no_file"] += 1
            return False

        if not commit:
            self.stats["skip_no_commit"] += 1
            return False

        code, start, end, code_type = extract_code(content, line, rule)

        if not code or len(code.strip()) < 20:
            self.stats["skip_extract"] += 1
            return False

        valid, _ = validate_code_start(code, rule)
        if not valid:
            self.stats["skip_bad_start"] += 1
            return False

        valid, _ = validate_rule_context(code, rule)
        if not valid:
            self.stats["skip_missing_context"] += 1
            return False

        code_lines = len(code.split('\n'))
        if code_lines > MAX_CODE_LINES:
            self.stats["skip_long"] += 1
            return False

        h = get_hash(code)
        if h in self.seen_hash_per_rule[rule]:
            self.stats["skip_dup_code_same_rule"] += 1
            return False

        code, _ = ensure_balanced(code)
        ob, cb = count_braces(code)

        target_file_key = file_in_repo if file_in_repo else rel
        buggy_files_dict = {
            target_file_key: content
        }

        # Commit entry validation
        self.seen_exact_loc.add(exact_loc_key)
        self.seen_hash_per_rule[rule].add(h)
        self.counts[rule] += 1
        self.total += 1
        self.stats["ok"] += 1
        if git_ok:
            self.stats["git_ok"] += 1

        self.data.append({
            "instance_id": f"OH_{self.total:04d}",
            "project": proj,
            "rule_id": rule,
            "commit_hash": commit,

            "buggy_files": buggy_files_dict,
            "target_file": target_file_key,

            "input_snippet": code,
            "start_line": start,
            "end_line": end,

            "category": get_category(rule),
            "line_number": line,
            "code_type": code_type,
            "warning_message": rec.get('Message') or "",
            "code_lines": code_lines,
            "braces_open": ob,
            "braces_close": cb
        })

        return True


# ============================================================================
# Main Script Execution Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Clean and structure raw static logs into the final JSON dataset.")
    parser.add_argument("--csv", required=True, help="Input CSV log file from collect_violations_arkts.py")
    parser.add_argument("--workspace", required=True, help="Path to directories containing git repos")
    parser.add_argument("--output", required=True, help="Target JSON dataset output path")
    args = parser.parse_args()

    git_manager = GitRepoManager(args.workspace)
    print(f"Loaded {len(git_manager.repo_paths)} tracking git repositories.")

    build_file_index(args.workspace)
    print(f"Indexed {len(FILE_INDEX)} source files in Workspace.")

    rows = []
    rule_counts = defaultdict(int)

    with open(args.csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
            rule_id = r.get('Rule_ID') or r.get('RuleID') or ''
            if rule_id in TARGET_RULES:
                rule_counts[rule_id] += 1

    print("\n--- Available Instances in Raw Logs ---")
    for rule in sorted(TARGET_RULES.keys()):
        avail = rule_counts.get(rule, 0)
        target = TARGET_RULES[rule]
        short = rule.split("/")[-1][:30]
        print(f"  {short:<32} Available: {avail:>4} | Target Limit: {target}")

    dataset_processor = ArkTSDatasetProcessor(args.workspace, git_manager)

    for i, rec in enumerate(rows):
        if dataset_processor.all_done():
            break
        dataset_processor.process(rec)

        if (i + 1) % 200 == 0:
            done = sum(1 for r in TARGET_RULES if dataset_processor.counts[r] >= TARGET_RULES[r])
            print(f"\r  [{dataset_processor.total}] Target Rules Completed: {done}/{len(TARGET_RULES)} | Iterated: {i+1}/{len(rows)}", end="", flush=True)

    print(f"\nConstructed {dataset_processor.total} benchmark instances.")

    # Validation Checks
    balanced = sum(1 for d in dataset_processor.data if d["braces_open"] == d["braces_close"])
    print(f"  Syntactic Brace Balanced snippets: {balanced}/{len(dataset_processor.data)} ({100 * balanced / len(dataset_processor.data) if dataset_processor.data else 0:.1f}%)")

    # Save to disk
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(dataset_processor.data, f, indent=2, ensure_ascii=False)

    print(f"\n[Success] Dataset constructed successfully and saved to: {args.output}")


if __name__ == "__main__":
    main()