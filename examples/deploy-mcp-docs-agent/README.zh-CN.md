# deploy-mcp-docs-agent

一个通过 `deepagents deploy` 部署的文档研究代理。它会先通过 MCP 搜索实时文档，再在必要时依赖通用知识，回答有关 LangChain、LangGraph 和 Deep Agents 的开发者问题。

## 先决条件

| 变量 | 说明 |
|------|------|
| `ANTHROPIC_API_KEY` | Claude 模型访问权限 |
| `LANGSMITH_API_KEY` | 部署时必需 |

## 部署

```bash
deepagents deploy
```

MCP 服务器现在是工作区级资源。先注册一次 LangChain 文档服务器，然后在 `tools.json` 中引用它：

```bash
deepagents mcp-servers add --url https://docs.langchain.com/mcp --name docs-langchain
```

## 可以尝试的内容

部署完成后，在 LangSmith 中打开该代理，并尝试提问，例如：

- "How do I configure memory in Deep Agents?"
- "What's the difference between sync and async subagents?"
- "Show me how to add an MCP server to deepagents.toml"
- "What models are supported for deploy?"

翻译成中文如下：

- "如何在 Deep Agents 中配置内存？"
- "同步子代理和异步子代理有什么区别？"
- "请展示如何将 MCP 服务器添加到 deepagents.toml"
- "部署支持哪些模型？"

该代理始终会先搜索文档，并在回答中标注它找到答案的页面来源。

## 通过 SDK 查询

```python
from langgraph_sdk import get_client

client = get_client(url="https://<your-deployment-url>")
thread = await client.threads.create()

async for chunk in client.runs.stream(
    thread["thread_id"], "agent",
    input={"messages": [{"role": "user", "content": "How do I add an MCP server to deepagents.toml?"}]},
    stream_mode="messages",
):
    print(chunk.data, end="", flush=True)
```

在 LangSmith 的 **Deployments** 中找到你的部署 URL。更多信息请参见 [LangGraph SDK 文档](https://langchain-ai.github.io/langgraph/concepts/sdk/)。

## 结构

```
deploy-mcp-docs-agent/
├── AGENTS.md     # 智能体说明和回答格式
└── agent.json    # 部署配置（名称、模型）
```

## 资源

- [deepagents deploy 文档](https://docs.langchain.com/deepagents/deploy)
- [MCP server 文档](https://docs.langchain.com/deepagents/mcp)
- [LangChain Academy](https://academy.langchain.com/) — 由 LangChain 团队制作的免费综合课程，涵盖 LangChain 库和产品。
- [Code of Conduct](https://github.com/langchain-ai/langchain/?tab=coc-ov-file) — 社区指南和标准
