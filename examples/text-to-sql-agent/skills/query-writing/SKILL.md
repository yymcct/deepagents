---
name: query-writing
description: 从简单 SELECT 到复杂多表 JOIN、聚合和子查询，编写并执行 SQL 查询。适用于用户要求查询数据库、编写 SQL、执行 SELECT 语句、检索数据、筛选记录或生成数据库报表的场景。
---

# 查询编写技能

## 简单查询的工作流

针对单表的直接问题：

1. **确定表** - 哪张表包含所需数据？
2. **获取 schema** - 使用 `sql_db_schema` 查看列信息
3. **编写查询** - 使用 SELECT 选择相关列，并结合 WHERE/LIMIT/ORDER BY
4. **执行查询** - 通过 `sql_db_query` 运行
5. **整理答案** - 清晰展示结果

## 复杂查询的工作流

针对需要多表参与的问题：

### 1. 规划方案
**使用 `write_todos` 将任务拆解：**
- 识别所需的所有表
- 映射关系（外键）
- 规划 JOIN 结构
- 确定聚合方式

### 2. 检查表结构
对每张表使用 `sql_db_schema`，找出关联列和所需字段。

### 3. 构造查询
- SELECT - 选择列和聚合字段
- FROM/JOIN - 按 FK = PK 连接表
- WHERE - 在聚合前筛选数据
- GROUP BY - 所有非聚合列都要参与分组
- ORDER BY - 按有意义的字段排序
- LIMIT - 默认 5 行

### 4. 验证并执行
检查所有 JOIN 都有条件，GROUP BY 正确无误，然后再执行查询。

## 示例：按国家统计收入
```sql
SELECT
    c.Country,
    ROUND(SUM(i.Total), 2) as TotalRevenue
FROM Invoice i
INNER JOIN Customer c ON i.CustomerId = c.CustomerId
GROUP BY c.Country
ORDER BY TotalRevenue DESC
LIMIT 5;
```

## 错误恢复

如果查询失败或返回异常结果：
1. **空结果** — 对照 schema 核对列名和 WHERE 条件，检查大小写敏感性或 NULL 值
2. **语法错误** — 重新检查 JOIN、GROUP BY 完整性和别名引用
3. **超时** — 添加更严格的 WHERE 条件或 LIMIT 以减少结果集，然后再细化

## 质量规范

- 只查询相关列（不要使用 SELECT *）
- 始终应用 LIMIT（默认 5）
- 使用表别名提高可读性
- 对复杂查询：使用 write_todos 进行规划
- 不要使用 DML 语句（INSERT、UPDATE、DELETE、DROP）
