---
name: schema-exploration
description: 列出表、描述列和数据类型、识别外键关系，并映射数据库中的实体关系。适用于用户询问数据库 schema、表结构、列类型、有哪些表、ER 图、外键或实体之间关系的场景。
---

# Schema 探索技能

## 工作流

### 1. 列出所有表
使用 `sql_db_list_tables` 工具查看数据库中可用的全部表。

它会返回可以查询的完整表列表。

### 2. 获取特定表的 schema
使用 `sql_db_schema` 工具检查表：
- **列名** - 有哪些字段可用
- **数据类型** - INTEGER、TEXT、DATETIME 等
- **样例数据** - 3 条示例记录，帮助理解内容
- **主键** - 行的唯一标识符
- **外键** - 与其他表的关系

### 3. 映射关系
识别表之间如何连接：
- 查找以 "Id" 结尾的列（例如 CustomerId、ArtistId）
- 外键连接到其他表中的主键
- 记录父子关系

### 4. 回答问题
提供清晰的信息，包括：
- 可用表及其用途
- 列名及其含义
- 表之间的关联方式
- 样例数据用于说明内容

## 示例："有哪些表可用？"

**步骤 1：** 使用 `sql_db_list_tables`

**返回：**
```
Chinook 数据库有 11 张表：
1. Artist - 音乐艺术家
2. Album - 音乐专辑
3. Track - 单曲/歌曲
4. Genre - 音乐类型
5. MediaType - 文件格式（MP3、AAC 等）
6. Playlist - 用户创建的播放列表
7. PlaylistTrack - 播放列表中的歌曲
8. Customer - 商店客户
9. Employee - 商店员工
10. Invoice - 客户购买记录
11. InvoiceLine - 发票中的单项商品
```

## 示例："Customer 表有哪些列？"

**步骤 1：** 使用表名 "Customer" 调用 `sql_db_schema`

**返回：**
```
Customer 表包含以下列：

- CustomerId (INTEGER) - 主键，唯一客户 ID
- FirstName (NVARCHAR) - 客户名字
- LastName (NVARCHAR) - 客户姓氏
- Company (NVARCHAR) - 公司名称（可选）
- Address, City, State, Country, PostalCode - 地址字段
- Phone (NVARCHAR) - 电话号码
- Fax (NVARCHAR) - 传真号码
- Email (NVARCHAR) - 邮箱
- SupportRepId (INTEGER) - 指向 Employee 表的外键

样例数据显示客户包括：
- Luís Gonçalves，来自巴西
- Leonie Köhler，来自德国
- François Tremblay，来自加拿大
```

## 示例："如何按艺术家统计收入？"

**步骤 1：** 确定需要的表
- Artist（拥有艺术家名称）
- Album（连接艺术家和曲目）
- Track（连接专辑和销售）
- InvoiceLine（保存销售数据）
- Invoice（保存收入总额）

**步骤 2：** 映射关系
```
Artist (ArtistId)
  ↓ 1:many
Album (ArtistId, AlbumId)
  ↓ 1:many
Track (AlbumId, TrackId)
  ↓ 1:many
InvoiceLine (TrackId, UnitPrice, Quantity)
```

**返回：**
```
要按艺术家统计收入，你需要：
1. 从 Artist 表开始
2. 按 ArtistId 连接 Album
3. 按 AlbumId 连接 Track
4. 按 TrackId 连接 InvoiceLine
5. 对收入做求和（UnitPrice * Quantity）
6. 按艺术家名称分组

这需要使用 query-writing 技能来执行查询。
```

## 质量规范

**针对“列出表”类问题：**
- 展示所有表名
- 简要说明每张表包含什么内容
- 按相关类别分组（例如音乐目录、交易、人群）

**针对“描述表结构”类问题：**
- 列出所有列及其数据类型
- 解释每列的含义
- 展示样例数据作为上下文
- 标注主键和外键
- 说明与其他表的关系

**针对“如何查询 X”类问题：**
- 确定所需表
- 绘制 JOIN 路径
- 解释关系链
- 给出下一步建议（使用 query-writing 技能）

