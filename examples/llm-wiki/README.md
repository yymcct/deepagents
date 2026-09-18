# LLM Wiki

这是一个“脚本优先”的 Deep Agents 示例，用于构建持久化 wiki，并通过 `langsmith hub` 命令同步到 Context Hub。

## 它是如何工作的

这个示例实现了一个工作流：代理研究某个主题，并把结果写入 Context Hub 条目中。

代理会被提供源材料和问题，然后收集信息、整理结构，并逐步构建一个可复用的 wiki，供未来代理参考。随着时间推移，wiki 会通过 ingest、query 和 lint 这几轮处理不断演化，而不是每次运行都从头开始。

`ingest`、`query` 和 `lint` 均由 Deep Agents（`create_deep_agent`）驱动，并运行在 LangSmith Sandbox 中：query 阶段会读取当前 wiki 状态，评估相关页面，生成基于事实的答案，并在有用时把可长期复用的结果归档到 `wiki/query/`。

每次运行都会把更新同步到 Context Hub，因此团队成员可以审阅变更、发表评论并推广版本。

## 结构

- `runner.py` - 轻量级 CLI 入口
- `helpers.py` - 公共辅助函数、CLI 参数解析和模式编排
- `index.py` - `wiki/index.md` 目录构建与分类逻辑
- `log.py` - `log.md` 追加式时间线格式化与写入
- `models.py` - 共享配置、依赖和结果数据类
- `init.py` - `init` 模式工作流和内部源校验
- `ingest.py` - `ingest` 模式的源扩展 + 审核/应用流程
- `query.py` - `query` 模式的分析 + 可选持久化归档流程
- `lint.py` - `lint` 模式的健康检查与修正流程
- `README.md` - 安装与使用说明
- `pyproject.toml` - 示例本地依赖配置

## 工作区布局

`init` 会在 wiki 仓库中创建以下顶层结构：

- `AGENTS.md` - wiki 的 schema/config 和 ingest/query/lint 工作流规则。`init` 在缺失时创建，并在重跑时保留已有修改。
- `raw/` - 供 ingest 使用的不可变源文件（文章、笔记、数据集）。
- `wiki/` - 由 LLM 维护的知识页面（实体、概念、摘要、综合内容）。
- `wiki/index.md` - 面向内容的 wiki 导航和检索目录：按类别展示页面链接、单行摘要，以及可选元数据（如日期/来源数）。query 流程会先读取它。
- `log.md` - 追加式的时间线日志。每次 ingest/query/lint 阶段都会追加一条可解析标题：`## [YYYY-MM-DD] mode.phase | outcome=...`，并附带时间戳和摘要列表。

## 依赖要求

- Python 3.11+
- 可用 `langsmith[sandbox]` 和 `hub` 命令（由 `uv sync` 在示例环境中安装）
- `ingest`、`query` 和 `lint` 模式需要设置 `LANGSMITH_API_KEY`

## 安装与设置

```bash
# 在 deepagents 仓库根目录执行：
uv sync --project examples/llm-wiki
```

## 预检步骤

```bash
# 验证示例环境中的 Hub 命令。
uv run --project examples/llm-wiki langsmith hub --help

# 验证 sandbox 模式所需的认证环境变量。
echo "${LANGSMITH_API_KEY:+set}"
```

`init` 会从 `hub init --help` 自动检测可用的 source 参数，并在首次推送前通过 `/api/v1/repos` 预创建/校验仓库，要求 `source=internal`。如果已有仓库不是 internal 类型，init 会快速失败并给出可操作的错误信息。

## 使用方法

```bash
# 初始化 wiki 并发布首个 Context Hub 修订版本
uv run --project examples/llm-wiki \
  python examples/llm-wiki/runner.py \
  --mode init \
  --repo "ada-lovelace-wiki"

# 把源笔记导入到规范化 wiki 页面（文件 + 文件夹）
uv run --project examples/llm-wiki \
  python examples/llm-wiki/runner.py \
  --mode ingest \
  --repo "ada-lovelace-wiki" \
  --source ./notes/ada.md \
  --source ./notes/speeches/

# 基于维护中的 wiki 提问并获取有依据的回答
uv run --project examples/llm-wiki \
  python examples/llm-wiki/runner.py \
  --mode query \
  --repo "ada-lovelace-wiki" \
  --question "What did Ada contribute to computing?"

# 执行 wiki 维护并发布更新后的 Context Hub 修订版本
#（修复链接、去重页面、刷新 index.md、追加 log.md 记录）
uv run --project examples/llm-wiki \
  python examples/llm-wiki/runner.py \
  --mode lint \
  --repo "ada-lovelace-wiki"

# 可选参数：
#   --owner "acme"       # 当仓库位于显式 owner 下时使用
#   --review             # 仅 ingest：应用前先审阅
#   --description "..."  # 仅 init：设置 Hub 仓库描述
```

## Ingest 工作流

默认情况下，`ingest` 会直接应用。

如果传入 `--review`，ingest 会变成一个双阶段、人工参与的流程：

1. Review 阶段（只读）：模型读取已分发的源文件，返回关键信息、建议的 wiki 更新、矛盾点以及索引更新。
2. Apply 阶段（写入）：在你确认后，模型写入规范化的概念/实体/主题更新，并将证据直接整合到对应页面中。
3. runner 会刷新 `wiki/index.md`，并在 `log.md` 中追加结构化的 `ingest.review` / `ingest.apply` 时间线条目。
4. 在 `--review` 模式下，如果你拒绝确认，wiki 不会修改，但系统仍会追加 `ingest.apply | outcome=canceled` 记录并推送，以确保时间线完整。

批量 ingest 是默认行为。一次运行可以处理多个文件和目录。

## Query 工作流

`query` 会自动分为两个阶段：

1. Analysis 阶段（只读）：模型会读取 `wiki/index.md`，然后查看最近的 `log.md` 条目获取时效性上下文，再在必要时查阅先前的 `wiki/query/*.md` 页面用于发现和路由，展开到规范化 wiki 页面进行事实支撑，回答时附带引用，并决定结果是否值得保存用于未来复用。query 页面被视为路由提示，而不是主要证据来源。
2. Filing 阶段（写入，条件性）：如果答案具备长期价值，runner 会把它写入 `wiki/query/<question-slug>.md`，并刷新 `wiki/index.md`。
3. runner 始终会向 `log.md` 写入结构化的 query 时间线条目（`query.review`，并在需要时追加 `query.apply`），并推送到 Context Hub，因此查询历史即使在 `skip` 时也会保持完整。

## Lint 工作流

`lint` 是单次执行，并会立即应用：

1. Health-check 阶段（应用）：模型会读取最近的 `log.md` 条目获取上下文，然后直接修正 `/wiki/` 下的矛盾、过时/被替代的声明、孤立页面、缺失的相互引用，以及关键概念覆盖度问题（必要时创建新的规范化页面）。
2. Gap reporting 阶段（响应中）：模型返回一段简明总结，说明已修正内容、剩余差距，以及建议的下一步问题和来源。
3. runner 会刷新 `wiki/index.md`，向 `log.md` 追加结构化的 `lint.apply` 记录，并完成推送。

## 日志时间线

`log.md` 由 runner 管理，是追加式日志，适合用简单 shell 工具解析。

- 代理不应直接编辑 `log.md`；它由 runner 统一追加记录。
- 每次交互都会记录：
  - `ingest.review`（在启用 `--review` 时）
  - `ingest.apply`（`outcome=applied` 或 `outcome=canceled`）
  - `query.review`（`outcome=file` 或 `outcome=skip`）
  - `query.apply`（仅在归档时，`outcome=filed`）
  - `lint.apply`（`outcome=applied`）
- 条目结构：
  - 标题：`## [YYYY-MM-DD] mode.phase | outcome=... key=value ...`
  - 正文列表：`timestamp`（UTC）和 `summary`

```bash
# 显示最近 5 条时间线记录。
grep "^## \\[" log.md | tail -5

# 显示最近的 query review 结果。
grep "^## \[.*\] query.review \|" log.md | tail -10
```

## 资源

- [LangChain Academy](https://academy.langchain.com/) — 由 LangChain 团队提供的全面免费课程，覆盖 LangChain 库和产品。
- [Code of Conduct](https://github.com/langchain-ai/langchain/?tab=coc-ov-file) — 社区准则与标准
