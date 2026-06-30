# OH-Bench

OH-Bench 是一个用于评估代码修复结果的实验项目。项目通过预置数据集读取任务信息，将模型或 Agent 生成的补丁提交到 Docker 评测环境中执行，并统计目标告警是否被消除、是否引入新问题以及整体通过率。

## 项目结构

```text
.
├── data/                    # 数据集、Agent 输出与评测结果
├── docker/                  # Docker 评测环境定义
├── scripts/                 # 数据构建、仓库准备和容器内评测脚本
├── run_experiment.py        # 标准评测入口
└── run_experiment_quick.py  # 快速评测入口，支持持久容器和区间执行
```

## 环境要求

- Python 3.8+
- Docker
- 已构建的 Docker 镜像：`oh-bench-env`

如果需要从 Dockerfile 构建镜像，请先准备 Dockerfile 中引用的外部资源：

- `tools_archive/codelinter`
- `tools_archive/ohos-sdk`
- `repositories_slim`

然后在项目根目录执行：

```bash
docker build -f docker/Dockerfile -t oh-bench-env .
```

## 数据准备

评测脚本默认读取以下数据集文件：

```text
data/arkts_dataset_final.json
data/cpp_dataset_final.json
```

Agent 结果文件通常存放在：

```text
data/arkts/
data/cpp/
```

结果 JSON 中需要包含 `instance_id`，以及 `model_patch` 或 `patch` 字段。

## 运行评测

评测 ArkTS 数据：

```bash
python run_experiment_quick.py --dataset arkts --results data/arkts/agent_results_example.json
```

评测 C++ 数据：

```bash
python run_experiment_quick.py --dataset cpp --results data/cpp/agent_results_example.json
```

同时评测两个数据集：

```bash
python run_experiment_quick.py --dataset both --results path/to/agent_results.json
```

使用慢速但隔离性更强的 `docker run --rm` 模式：

```bash
python run_experiment_quick.py --dataset arkts --results path/to/results.json --slow
```

只评测指定区间：

```bash
python run_experiment_quick.py --dataset arkts --results path/to/results.json --start task_001 --end task_020
```

## 输出说明

脚本会在终端输出每个任务的评测结果，常见状态包括：

- `PASS`：目标告警已消除，且没有新增告警
- `LINTER_FAIL`：目标告警仍然存在
- `SECONDARY_DEFECT`：目标告警消除，但引入了新告警
- `SYNTAX_FAIL`：补丁导致语法或构建错误
- `APPLY_ERROR`：补丁应用失败
- `TIMEOUT`：评测超时

`run_experiment_quick.py` 默认会将汇总报告写入 `logs/` 目录。

## 辅助脚本

- `scripts/prepare_repos.py`：准备待评测仓库
- `scripts/build_dataset.py`：构建 ArkTS 数据集
- `scripts/build_cpp_dataset.py`：构建 C++ 数据集
- `scripts/merge_datasets.py`：合并数据集
- `scripts/evaluate_in_docker.py`：Docker 容器内的实际评测入口

## 注意事项

- 运行前请确认 `oh-bench-env` 镜像已经构建成功。
- 数据集路径需要与脚本中的默认配置一致，或在代码中调整 `DATASET_MAP`。
- Docker 评测环境会在目标仓库内应用补丁、运行 linter，然后恢复工作区。
