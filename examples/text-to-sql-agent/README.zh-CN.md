# Text-to-SQL 深度 Agent（Deep Agent）

一个由 LangChain 的 **Deep Agents** 框架驱动的自然语言转 SQL 查询 Agent。这是一个进阶版的 text-to-SQL Agent，具备规划、文件系统和子 Agent 能力。

## 什么是 Deep Agents？

Deep Agents 是一个构建在 LangGraph 之上的高级 Agent 框架，提供：

- **规划能力** - 使用 `write_todos` 工具分解复杂任务
- **文件系统后端** - 通过文件操作保存和检索上下文
- **子 Agent 派生** - 将专门任务委派给专注的 Agent
- **上下文管理** - 在复杂任务中防止上下文窗口溢出

## 示例数据库

使用 [Chinook 数据库](https://github.com/lerocha/chinook-database) —— 一个代表数字媒体商店的示例数据库。

## 快速开始

### 前置要求

- Python 3.11 或更高版本
- Anthropic API key（[在此获取](https://console.anthropic.com/)）
- （可选）用于追踪的 LangSmith API key（[在此注册](https://smith.langchain.com/)）

### 安装

1. 克隆 deepagents 仓库并进入此示例目录：

```bash
git clone https://github.com/langchain-ai/deepagents.git
cd deepagents/examples/text-to-sql-agent
```

1. 下载 Chinook 数据库：

```bash
# 下载 SQLite 数据库文件
curl -L -o chinook.db https://github.com/lerocha/chinook-database/raw/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite
```

1. 创建虚拟环境并安装依赖：

```bash
# 使用 uv（推荐）
uv venv --python 3.11
source .venv/bin/activate  # Windows 上：.venv\Scripts\activate
uv sync
```

1. 配置环境变量：

```bash
cp .env.example .env
# 编辑 .env 并添加你的 API key
```

`.env` 中的必需项：

```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

可选项：

```
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=text2sql-deepagent
```

## 使用方法

### 命令行界面

通过命令行使用自然语言问题运行 Agent：

```bash
python agent.py "What are the top 5 best-selling artists?"
```

```bash
python agent.py "Which employee generated the most revenue by country?"
```

```bash
python agent.py "How many customers are from Canada?"
```

### 编程方式调用

你也可以在 Python 代码中使用该 Agent：

```python
from agent import create_sql_deep_agent

# 创建 Agent
agent = create_sql_deep_agent()

# 提出一个问题
result = agent.invoke({
    "messages": [{"role": "user", "content": "What are the top 5 best-selling artists?"}]
})

print(result["messages"][-1].content)
```

## Deep Agent 的工作原理

### 架构

```
用户提问
     ↓
Deep Agent（带规划）
     ├─ write_todos（规划方案）
     ├─ SQL 工具
     │  ├─ list_tables
     │  ├─ get_schema
     │  ├─ query_checker
     │  └─ execute_query
     ├─ 文件系统工具（可选）
     │  ├─ ls
     │  ├─ read_file
     │  ├─ write_file
     │  └─ edit_file
     └─ 子 Agent 派生（可选）
     ↓
SQLite 数据库（Chinook）
     ↓
格式化后的答案
```

### 配置

Deep Agents 通过记忆文件和技能（skills）实现 **渐进式披露（progressive disclosure）**：

**AGENTS.md**（始终加载）- 包含：

- Agent 身份和角色
- 核心原则和安全规则
- 通用准则
- 沟通风格

**skills/**（按需加载）- 专门工作流：

- **query-writing** - 如何编写和执行 SQL 查询（简单和复杂）
- **schema-exploration** - 如何发现数据库结构及其关系

Agent 在其上下文中可以看到技能的描述，但只有当它判断当前任务需要某个技能时，才会加载完整的 SKILL.md 指令。这种 **渐进式披露** 模式在保持上下文高效的同时，按需提供深入的专家知识。

## 示例查询

### 简单查询

```
"How many customers are from Canada?"
```

Agent 会直接执行查询并返回计数。

### 带规划的复杂查询

```
"Which employee generated the most revenue and from which countries?"
```

Agent 将会：

1. 使用 `write_todos` 规划方案
2. 识别所需表（Employee、Invoice、Customer）
3. 规划 JOIN 结构
4. 执行查询
5. 格式化结果并附上分析

## Deep Agent 输出示例

Deep Agent 会展示其推理过程：

```
问题：Which employee generated the most revenue by country?

[规划步骤]
使用 write_todos：
- [ ] 列出数据库中的表
- [ ] 检查 Employee 和 Invoice 表结构
- [ ] 规划多表 JOIN 查询
- [ ] 执行并按员工和国家聚合
- [ ] 格式化结果

[执行步骤]
1. 列出表...
2. 获取以下表的结构：Employee、Invoice、InvoiceLine、Customer
3. 生成 SQL 查询...
4. 执行查询...
5. 格式化结果...

[最终答案]
员工 Jane Peacock（ID: 3）创造的收入最多...
主要国家：美国（$1000）、加拿大（$500）...
```

## 项目结构

```
text-to-sql-agent/
├── agent.py                      # 核心 Deep Agent 实现（含 CLI）
├── AGENTS.md                     # Agent 身份和通用指令（始终加载）
├── skills/                       # 专门工作流（按需加载）
│   ├── query-writing/
│   │   └── SKILL.md             # SQL 查询编写工作流
│   └── schema-exploration/
│       └── SKILL.md             # 数据库结构发现工作流
├── chinook.db                    # 示例 SQLite 数据库（已下载，被 gitignore）
├── pyproject.toml                # 项目配置和依赖
├── uv.lock                       # 锁定的依赖版本
├── .env.example                  # 环境变量模板
├── .gitignore                    # Git 忽略规则
├── text-to-sql-langsmith-trace.png  # LangSmith 追踪示例图
└── README.md                     # 本文件
```

## LangSmith 集成

### 设置

1. 在 [LangSmith](https://smith.langchain.com/) 注册一个免费账户
2. 在账户设置中创建 API key
3. 将以下变量添加到你的 `.env` 文件：

```
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=text2sql-deepagent
```

### 你将看到什么

配置完成后，每次查询都会被自动追踪：

![Deep Agent LangSmith 追踪示例](text-to-sql-langsmith-trace.png)

你可以查看：

- 包含所有工具调用的完整执行追踪
- 规划步骤（write_todos）
- 文件系统操作
- Token 使用量和成本
- 生成的 SQL 查询
- 错误信息和重试尝试

在以下地址查看你的追踪记录：<https://smith.langchain.com/>

## 相关资源

- [Deep Agents 文档](https://docs.langchain.com/oss/python/deepagents/overview)
- [LangChain](https://www.langchain.com/)
- [Claude Sonnet 4.5](https://www.anthropic.com/claude)
- [Chinook 数据库](https://github.com/lerocha/chinook-database)
- [LangChain Academy](https://academy.langchain.com/) —— 由 LangChain 团队制作的关于 LangChain 库和产品的全面免费课程。
- [行为准则](https://github.com/langchain-ai/langchain/?tab=coc-ov-file) —— 社区准则和规范

## 许可证

MIT

## 贡献

欢迎贡献！请随时提交 Pull Request。
