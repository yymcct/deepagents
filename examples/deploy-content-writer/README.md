# deploy-content-writer

这是一个通过 `deepagents deploy` 部署的内容创作代理。它可以撰写博客文章、LinkedIn 发布内容和推文，并且能够根据每位用户的身份记住其偏好，并在会话之间保留按用户隔离的记忆。

这个示例还演示了 **自定义认证**：在 `deepagents.toml` 中添加 `[auth] provider = "supabase"`，这样每个用户的记忆都会按自己的账户隔离，而且不需要编写任何自定义代码。

## 前置条件

| 变量 | 说明 |
|----------|-------------|
| `OPENAI_API_KEY` | 需要有 GPT-4.1 模型访问权限 |
| `LANGSMITH_API_KEY` | 部署时必需 |
| `SUPABASE_URL` | 你的 Supabase 项目 URL（用于认证） |
| `SUPABASE_ANON_KEY` | 你的 Supabase 匿名/公开密钥（用于认证） |

复制 `.env.example` 到 `.env`，并填写你的密钥。只有在保留 `deepagents.toml` 中的 `[auth]` 配置时，才需要 Supabase 密钥。如果不想启用认证，可以删除该部分后再部署。

## 部署

```bash
deepagents deploy
```

部署时，`deepagents.toml` 中的 `[auth]` 部分会自动生成 Supabase token 校验器，并将它接入部署流程——无需自定义中间件。

## 按用户记忆的工作方式

每个已认证用户都会获得各自的记忆文件，路径位于 `/memories/user/`：

- `preferences.md` —— 代理会读取并更新此文件，以记住语气、主题和格式偏好
- `context.md` —— 用户公司和产品的静态上下文信息

由于认证会按照用户身份为这些文件加以隔离，因此一个部署实例可以为多个用户提供服务，而不会出现账号之间互相污染的情况。

## 可以尝试的内容

部署完成后，打开 LangSmith 中的代理，并发送类似提示词：

- `"Write a blog post about the benefits of AI agents for developer teams"`
- `"Turn this into a LinkedIn post: [paste your content]"`
- `"I prefer a more casual tone — remember that for future posts"`
- `"Draft three tweet variations for our new product launch"`

## 通过 SDK 查询

在 `Authorization` 请求头中传入你的 Supabase JWT —— 部署会自动校验它并推断用户身份：

```python
from langgraph_sdk import get_client

client = get_client(
    url="https://<your-deployment-url>",
    headers={"Authorization": "Bearer <your-supabase-jwt>"},
)
thread = await client.threads.create()

async for chunk in client.runs.stream(
    thread["thread_id"], "agent",
    input={"messages": [{"role": "user", "content": "Write a tweet about AI agents"}]},
    stream_mode="messages",
):
    print(chunk.data, end="", flush=True)
```

在 LangSmith 的 **Deployments** 中找到你的部署 URL。完整示例见 `test_user_memory.py`，更多内容请参考 [LangGraph SDK 文档](https://langchain-ai.github.io/langgraph/concepts/sdk/)。

## 结构

```
deploy-content-writer/
├── AGENTS.md              # 代理指令和记忆工作流
├── deepagents.toml        # 部署配置（模型、认证）
└── skills/
    ├── blog-post/         # 长篇博客文章技能
    └── social-media/      # LinkedIn 和推文技能
```

## 资源

- [deepagents deploy 文档](https://docs.langchain.com/deepagents/deploy)
- [自定义认证文档](https://docs.langchain.com/deepagents/auth)
- [按用户记忆文档](https://docs.langchain.com/deepagents/memory)
- [LangChain Academy](https://academy.langchain.com/) — 由 LangChain 团队打造的全面免费课程，内容覆盖 LangChain 库和产品。
- [Code of Conduct](https://github.com/langchain-ai/langchain/?tab=coc-ov-file) — 社区行为准则
