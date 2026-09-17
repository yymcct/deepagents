<div align="center">
  <a href="https://docs.langchain.com/oss/python/deepagents/overview#deep-agents-overview">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="../.github/images/logo-dark.svg">
      <source media="(prefers-color-scheme: light)" srcset="../.github/images/logo-light.svg">
      <img alt="Deep Agents Logo" src="../.github/images/logo-dark.svg" width="50%">
    </picture>
  </a>
</div>

<h3 align="center">示例</h3>

<p align="center"><em>基于 Deep Agents 构建的真实代理和模式。</em></p>

## 精选项目

<table>
<tr>
<td width="50%" valign="top">

### Deep Agents Code

一个预构建的编码 Deep Agent，在你的终端中运行——类似于 Claude Code 或 Codex——由任何 LLM 提供支持。包括交互式 TUI、网络搜索、远程沙箱、持久内存、自定义技能和人工循环批准。

```bash
curl -LsSf https://langch.in/dcode | bash
```

<sub>[源代码](../libs/code/) · [文档](https://docs.langchain.com/oss/python/deepagents/cli/overview)</sub>

</td>
<td width="50%" valign="top">

### Open SWE

一个开源的异步编码代理，用于你的组织内部工作流程。在隔离的云沙箱中运行每个任务，集成 Slack、Linear 和 GitHub，并端到端地生成 PR。

```text
@open-swe fix this user-reported bug plz!
```

<sub>[仓库](https://github.com/langchain-ai/open-swe) · [博客文章](https://blog.langchain.com/open-swe-an-open-source-framework-for-internal-coding-agents/)</sub>

</td>
</tr>
</table>

## 实际应用

由 LangChain 技术栈驱动的生产级代理：

| 项目 | 描述 |
|---|---|
| [**LangSmith Fleet**](https://www.langchain.com/langsmith/fleet) | 无代码平台，用于从模板构建 AI 代理；连接你的账户，让代理处理日常工作 |
| [**Chat LangChain**](https://chat.langchain.com/) | 文档助手，回答关于 LangChain、LangGraph 和 LangSmith 的问题（[源代码](https://github.com/langchain-ai/chat-langchain)） |

## 所有示例

### 研究

| 示例 | 描述 |
|---|---|
| [**Deep Research**](deep_research/) | 使用 Tavily 的多步网络研究、并行子代理和战略性反思 |
| [**MCP Docs Agent**](deploy-mcp-docs-agent/) | 使用 MCP 工具对 LangChain 文档进行研究的文档代理 |

### 编码

| 示例 | 描述 |
|---|---|
| [**Coding Agent**](deploy-coding-agent/) | LangSmith 沙箱中的自主编码代理 |
| [**Nemotron Research Agent**](nvidia_deep_agent/) | NVIDIA Nemotron Super 用于研究 + 通过 RAPIDS 的 GPU 加速执行 |

### 内容

| 示例 | 描述 |
|---|---|
| [**Content Builder**](content-builder-agent/) | 博客文章、LinkedIn 帖子和推文，带有内存（`AGENTS.md`）、技能和子代理 |
| [**Text-to-SQL**](text-to-sql-agent/) | 在 Chinook 演示数据库上使用规划和基于技能的工作流程的自然语言转 SQL |
| [**LLM Wiki**](llm-wiki/) | 通过 `langsmith hub init/pull/push` 同步的脚本优先 LLM wiki |

### 可部署服务

| 示例 | 描述 |
|---|---|
| [**Content Writer**](deploy-content-writer/) | 具有每用户内存和 Supabase 身份验证的内容编写器 |
| [**GTM Strategist**](deploy-gtm-agent/) | 协调同步和异步子代理的 GTM 策略代理 |
| [**Async Subagent Server**](async-subagent-server/) | 自托管的 Agent Protocol 服务器，将研究员公开为异步子代理 |

### 高级模式

| 示例 | 描述 |
|---|---|
| [**Ralph Loop**](ralph_mode/) | 自主循环，每次迭代使用新上下文，使用文件系统进行持久化 |
| [**Agents as Folders**](downloading_agents/) | 下载 zip、解压和运行 |
| [**Better Harness**](better-harness/) | 使用 eval 驱动的外循环优化 Deep Agents 工具 |
| [**Rubric Middleware**](rubric_middleware/) | 分级模型评分反馈循环，修改输出直到满足所有条件 |

每个示例都有自己的 `README`，包含设置说明。

<details>
<summary><h2>贡献一个示例</h2></summary>

有关一般贡献指南，请参阅[贡献指南](https://docs.langchain.com/oss/python/contributing/overview)。

添加新示例时：

- **使用 uv** 进行依赖管理，使用 `pyproject.toml` 和 `uv.lock`（提交锁定文件）
- **固定 deepagents 版本** —— 在依赖项中使用版本范围（例如 `>=0.3.5,<0.4.0`）
- **包含 `README`** —— 提供清晰的设置和使用说明
- **添加测试** —— 针对可重用的实用程序或非平凡的辅助逻辑
- **保持专注** —— 每个示例应演示一个用例或工作流
- **遵循结构** —— 遵循现有示例的结构（参考 `deep_research/` 或 `text-to-sql-agent/`）

</details>

## 资源

- [LangChain Academy](https://academy.langchain.com/) —— 关于 LangChain 库和产品的综合、免费课程，由 LangChain 团队制作。
- [行为准则](https://github.com/langchain-ai/langchain/?tab=coc-ov-file) —— 社区指南和标准
