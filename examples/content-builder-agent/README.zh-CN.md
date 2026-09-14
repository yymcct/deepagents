# 内容创作智能体（Content Builder Agent）

<img width="1255" height="756" alt="content-cover-image" src="https://github.com/user-attachments/assets/4ebe0aba-2780-4644-8a00-ed4b96680dc9" />

一个用于撰写博客文章、LinkedIn 帖子和推文的内容创作智能体，并会自动配好封面图。

**本示例演示了如何通过三个文件系统原语来定义一个智能体：**
- **记忆（Memory）**（`AGENTS.md`）—— 持久化上下文，例如品牌语调与风格指南
- **技能（Skills）**（`skills/*/SKILL.md`）—— 针对特定任务的工作流，按需加载
- **子智能体（Subagents）**（`subagents.yaml`）—— 用于委派任务（如资料研究）的专用智能体

`content_writer.py` 脚本展示了如何将它们组合成一个可运行的智能体。

## 快速开始

```bash
# 设置 API 密钥
export ANTHROPIC_API_KEY="..."
export GOOGLE_API_KEY="..."      # 用于图像生成
export TAVILY_API_KEY="..."      # 用于网络搜索（可选）

# 运行（uv 会在首次运行时自动安装依赖）
cd examples/content-builder-agent
uv run python content_writer.py "写一篇关于提示词工程的博客文章"
```

**更多示例：**
```bash
uv run python content_writer.py "创建一条关于 AI 智能体的 LinkedIn 帖子"
uv run python content_writer.py "写一个关于编程未来的 Twitter 推文串"
```

## 工作原理

该智能体由磁盘上的文件进行配置，而非代码：

```
content-builder-agent/
├── AGENTS.md                    # 品牌语调与风格指南
├── subagents.yaml               # 子智能体定义
├── skills/
│   ├── blog-post/
│   │   └── SKILL.md             # 博客写作工作流
│   └── social-media/
│       └── SKILL.md             # 社交媒体工作流
└── content_writer.py            # 将它们串联起来（包含工具）
```

| 文件 | 用途 | 加载时机 |
|------|------|----------|
| `AGENTS.md` | 品牌语调、语气、写作标准 | 始终（系统提示词） |
| `subagents.yaml` | 研究及其他委派任务 | 始终（定义 `task` 工具） |
| `skills/*/SKILL.md` | 特定内容类型的工作流 | 按需加载 |

**技能里都有什么？** 每个技能都会教会智能体一套特定的工作流：
- **博客文章：** 结构（钩子 → 背景 → 主体内容 → 行动号召）、SEO 最佳实践、研究优先的方法
- **社交媒体：** 针对不同平台的格式（LinkedIn 字数限制、Twitter 推文串结构）、话题标签的使用
- **图像生成：** 详细的提示词工程指南，并附有面向不同内容类型（技术文章、公告、思想领导力）的示例

## 架构

```python
agent = create_deep_agent(
    memory=["./AGENTS.md"],                        # ← 中间件将其加载到系统提示词
    skills=["./skills/"],                          # ← 中间件按需加载
    tools=[generate_cover, generate_social_image], # ← 图像生成工具
    subagents=load_subagents("./subagents.yaml"),  # ← 见下方说明
    backend=FilesystemBackend(root_dir="./"),
)
```

`memory` 和 `skills` 参数由 deepagents 中间件原生处理。工具在脚本中定义并直接传入。

**关于子智能体的说明：** 与 `memory` 和 `skills` 不同，子智能体必须在代码中定义。我们使用一个小的 `load_subagents()` 辅助函数将配置外置到 YAML 中。你也可以以内联方式定义它们：

```python
subagents=[
    {
        "name": "researcher",
        "description": "在写作前研究主题……",
        "model": "anthropic:claude-haiku-4-5-20251001",
        "system_prompt": "你是一名研究助理……",
        "tools": [web_search],
    }
],
```

**流程：**
1. 智能体接收任务 → 加载相关技能（blog-post 或 social-media）
2. 将研究委派给 `researcher` 子智能体 → 保存到 `research/`
3. 按照技能工作流撰写内容 → 保存到 `blogs/` 或 `linkedin/`
4. 使用 Gemini 生成封面图 → 与内容一并保存

## 输出

```
blogs/
└── prompt-engineering/
    ├── post.md       # 博客内容
    └── hero.png      # 生成的封面图

linkedin/
└── ai-agents/
    ├── post.md       # 帖子内容
    └── image.png     # 生成的图片

research/
└── prompt-engineering.md   # 研究笔记
```

## 自定义

**更改语调：** 编辑 `AGENTS.md` 以修改品牌语气与风格。

**添加内容类型：** 创建 `skills/<name>/SKILL.md`，并带上 YAML frontmatter：
```yaml
---
name: newsletter
description: 在撰写电子邮件简报时使用此技能
---
# 简报技能
...
```

**添加子智能体：** 添加到 `subagents.yaml`：
```yaml
editor:
  description: 审阅并改进草稿内容
  model: anthropic:claude-haiku-4-5-20251001
  system_prompt: |
    你是一名编辑。请审阅内容并提出改进建议……
  tools: []
```

**添加工具：** 在 `content_writer.py` 中使用 `@tool` 装饰器定义它，并加入 `tools=[]`。

## 安全说明

该智能体拥有文件系统访问权限，可以读取、写入和删除你机器上的文件。发布前请检查生成的内容，并避免在包含敏感数据的目录中运行。

## 环境要求

- Python 3.11+
- `ANTHROPIC_API_KEY` —— 用于主智能体
- `GOOGLE_API_KEY` —— 用于图像生成（通过 `gemini-2.5-flash-image` 使用 Gemini 的 [Imagen / "nano banana"](https://ai.google.dev/gemini-api/docs/image-generation)）
- `TAVILY_API_KEY` —— 用于网络搜索（可选，没有它研究功能依然可用）

## 相关资源

- [LangChain Academy](https://academy.langchain.com/) —— 由 LangChain 团队制作的全面、免费的 LangChain 库与产品课程。
- [Code of Conduct](https://github.com/langchain-ai/langchain/?tab=coc-ov-file) —— 社区准则与标准
