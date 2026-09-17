# Chinook 数据库结构说明

本文档说明 `chinook.sqlite` 的数据库结构。该库是一个数字媒体商店示例库，核心业务包括艺术家、专辑、曲目、播放列表、客户、员工、发票和发票明细。

## 总览

| 表名 | 行数 | 说明 |
| --- | ---: | --- |
| `Artist` | 275 | 艺术家或乐队 |
| `Album` | 347 | 专辑，隶属于艺术家 |
| `Track` | 3,503 | 曲目，关联专辑、媒体类型和音乐流派 |
| `Genre` | 25 | 音乐流派 |
| `MediaType` | 5 | 媒体编码或文件类型 |
| `Playlist` | 18 | 播放列表 |
| `PlaylistTrack` | 8,715 | 播放列表与曲目的多对多关系表 |
| `Customer` | 59 | 客户资料 |
| `Employee` | 8 | 员工资料与上下级关系 |
| `Invoice` | 412 | 客户订单或账单 |
| `InvoiceLine` | 2,240 | 订单明细，记录每张发票购买的曲目 |

## 主要关系

```text
Artist 1 ── n Album 1 ── n Track n ── 1 Genre
                         │
                         n ── 1 MediaType

Playlist n ── n Track
通过 PlaylistTrack 连接

Employee 1 ── n Customer 1 ── n Invoice 1 ── n InvoiceLine n ── 1 Track

Employee 1 ── n Employee
通过 Employee.ReportsTo 表示直属上级
```

## 表结构明细

### `Artist`

艺术家或乐队主数据。

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| `ArtistId` | `INTEGER` | 主键，非空 | 艺术家 ID |
| `Name` | `NVARCHAR(120)` | 可空 | 艺术家名称 |

### `Album`

专辑信息，每张专辑属于一个艺术家。

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| `AlbumId` | `INTEGER` | 主键，非空 | 专辑 ID |
| `Title` | `NVARCHAR(160)` | 非空 | 专辑标题 |
| `ArtistId` | `INTEGER` | 外键，非空 | 关联 `Artist.ArtistId` |

索引：`IFK_AlbumArtistId`。

### `Track`

曲目商品信息，是销售与播放列表分析的核心表。

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| `TrackId` | `INTEGER` | 主键，非空 | 曲目 ID |
| `Name` | `NVARCHAR(200)` | 非空 | 曲目名称 |
| `AlbumId` | `INTEGER` | 外键，可空 | 关联 `Album.AlbumId` |
| `MediaTypeId` | `INTEGER` | 外键，非空 | 关联 `MediaType.MediaTypeId` |
| `GenreId` | `INTEGER` | 外键，可空 | 关联 `Genre.GenreId` |
| `Composer` | `NVARCHAR(220)` | 可空 | 作曲者 |
| `Milliseconds` | `INTEGER` | 非空 | 时长，单位为毫秒 |
| `Bytes` | `INTEGER` | 可空 | 文件大小，单位为字节 |
| `UnitPrice` | `NUMERIC(10,2)` | 非空 | 曲目单价 |

索引：`IFK_TrackAlbumId`、`IFK_TrackGenreId`、`IFK_TrackMediaTypeId`。

### `Genre`

音乐流派字典表。

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| `GenreId` | `INTEGER` | 主键，非空 | 流派 ID |
| `Name` | `NVARCHAR(120)` | 可空 | 流派名称 |

### `MediaType`

媒体类型字典表，例如 MPEG、AAC、Protected AAC 等。

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| `MediaTypeId` | `INTEGER` | 主键，非空 | 媒体类型 ID |
| `Name` | `NVARCHAR(120)` | 可空 | 媒体类型名称 |

### `Playlist`

播放列表主表。

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| `PlaylistId` | `INTEGER` | 主键，非空 | 播放列表 ID |
| `Name` | `NVARCHAR(120)` | 可空 | 播放列表名称 |

### `PlaylistTrack`

播放列表与曲目的关联表。一首曲目可以出现在多个播放列表中，一个播放列表也可以包含多首曲目。

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| `PlaylistId` | `INTEGER` | 联合主键，外键，非空 | 关联 `Playlist.PlaylistId` |
| `TrackId` | `INTEGER` | 联合主键，外键，非空 | 关联 `Track.TrackId` |

索引：`sqlite_autoindex_PlaylistTrack_1`、`IFK_PlaylistTrackPlaylistId`、`IFK_PlaylistTrackTrackId`。

### `Customer`

客户资料，包含联系方式、地址和负责服务该客户的员工。

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| `CustomerId` | `INTEGER` | 主键，非空 | 客户 ID |
| `FirstName` | `NVARCHAR(40)` | 非空 | 名 |
| `LastName` | `NVARCHAR(20)` | 非空 | 姓 |
| `Company` | `NVARCHAR(80)` | 可空 | 公司名称 |
| `Address` | `NVARCHAR(70)` | 可空 | 地址 |
| `City` | `NVARCHAR(40)` | 可空 | 城市 |
| `State` | `NVARCHAR(40)` | 可空 | 州或省 |
| `Country` | `NVARCHAR(40)` | 可空 | 国家 |
| `PostalCode` | `NVARCHAR(10)` | 可空 | 邮政编码 |
| `Phone` | `NVARCHAR(24)` | 可空 | 电话 |
| `Fax` | `NVARCHAR(24)` | 可空 | 传真 |
| `Email` | `NVARCHAR(60)` | 非空 | 邮箱 |
| `SupportRepId` | `INTEGER` | 外键，可空 | 关联 `Employee.EmployeeId`，表示客户服务代表 |

索引：`IFK_CustomerSupportRepId`。

### `Employee`

员工资料，包含岗位、联系方式和直属上级。

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| `EmployeeId` | `INTEGER` | 主键，非空 | 员工 ID |
| `LastName` | `NVARCHAR(20)` | 非空 | 姓 |
| `FirstName` | `NVARCHAR(20)` | 非空 | 名 |
| `Title` | `NVARCHAR(30)` | 可空 | 职位 |
| `ReportsTo` | `INTEGER` | 外键，可空 | 关联 `Employee.EmployeeId`，表示直属上级 |
| `BirthDate` | `DATETIME` | 可空 | 出生日期 |
| `HireDate` | `DATETIME` | 可空 | 入职日期 |
| `Address` | `NVARCHAR(70)` | 可空 | 地址 |
| `City` | `NVARCHAR(40)` | 可空 | 城市 |
| `State` | `NVARCHAR(40)` | 可空 | 州或省 |
| `Country` | `NVARCHAR(40)` | 可空 | 国家 |
| `PostalCode` | `NVARCHAR(10)` | 可空 | 邮政编码 |
| `Phone` | `NVARCHAR(24)` | 可空 | 电话 |
| `Fax` | `NVARCHAR(24)` | 可空 | 传真 |
| `Email` | `NVARCHAR(60)` | 可空 | 邮箱 |

索引：`IFK_EmployeeReportsTo`。

### `Invoice`

发票或订单主表，记录客户某次购买的账单信息。

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| `InvoiceId` | `INTEGER` | 主键，非空 | 发票 ID |
| `CustomerId` | `INTEGER` | 外键，非空 | 关联 `Customer.CustomerId` |
| `InvoiceDate` | `DATETIME` | 非空 | 发票日期 |
| `BillingAddress` | `NVARCHAR(70)` | 可空 | 账单地址 |
| `BillingCity` | `NVARCHAR(40)` | 可空 | 账单城市 |
| `BillingState` | `NVARCHAR(40)` | 可空 | 账单州或省 |
| `BillingCountry` | `NVARCHAR(40)` | 可空 | 账单国家 |
| `BillingPostalCode` | `NVARCHAR(10)` | 可空 | 账单邮编 |
| `Total` | `NUMERIC(10,2)` | 非空 | 发票总金额 |

索引：`IFK_InvoiceCustomerId`。

### `InvoiceLine`

发票明细表，记录每张发票购买了哪些曲目、购买数量和成交单价。

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| `InvoiceLineId` | `INTEGER` | 主键，非空 | 发票明细 ID |
| `InvoiceId` | `INTEGER` | 外键，非空 | 关联 `Invoice.InvoiceId` |
| `TrackId` | `INTEGER` | 外键，非空 | 关联 `Track.TrackId` |
| `UnitPrice` | `NUMERIC(10,2)` | 非空 | 成交单价 |
| `Quantity` | `INTEGER` | 非空 | 数量 |

索引：`IFK_InvoiceLineInvoiceId`、`IFK_InvoiceLineTrackId`。

## 外键清单

| 来源表 | 来源字段 | 目标表 | 目标字段 | 关系含义 |
| --- | --- | --- | --- | --- |
| `Album` | `ArtistId` | `Artist` | `ArtistId` | 专辑属于艺术家 |
| `Track` | `AlbumId` | `Album` | `AlbumId` | 曲目属于专辑 |
| `Track` | `GenreId` | `Genre` | `GenreId` | 曲目属于流派 |
| `Track` | `MediaTypeId` | `MediaType` | `MediaTypeId` | 曲目使用某种媒体类型 |
| `PlaylistTrack` | `PlaylistId` | `Playlist` | `PlaylistId` | 播放列表包含曲目 |
| `PlaylistTrack` | `TrackId` | `Track` | `TrackId` | 曲目被加入播放列表 |
| `Customer` | `SupportRepId` | `Employee` | `EmployeeId` | 客户由员工负责支持 |
| `Employee` | `ReportsTo` | `Employee` | `EmployeeId` | 员工向另一名员工汇报 |
| `Invoice` | `CustomerId` | `Customer` | `CustomerId` | 发票属于客户 |
| `InvoiceLine` | `InvoiceId` | `Invoice` | `InvoiceId` | 明细属于发票 |
| `InvoiceLine` | `TrackId` | `Track` | `TrackId` | 明细对应购买曲目 |

## 常用查询路径

- 查询艺术家作品：`Artist` → `Album` → `Track`
- 查询曲目分类：`Track` → `Genre`，`Track` → `MediaType`
- 查询播放列表内容：`Playlist` → `PlaylistTrack` → `Track`
- 查询客户消费：`Customer` → `Invoice` → `InvoiceLine` → `Track`
- 查询销售负责人业绩：`Employee` → `Customer` → `Invoice`
- 查询曲目销售表现：`Track` → `InvoiceLine` → `Invoice`

## 设计备注

- `PlaylistTrack` 使用 `PlaylistId` 和 `TrackId` 作为联合主键，用于避免同一个播放列表中重复关联同一首曲目。
- 大多数外键索引以 `IFK_` 开头，用于优化关联查询。
- 金额字段包括 `Invoice.Total` 与 `InvoiceLine.UnitPrice`，类型为 `NUMERIC(10,2)`。
- 时间字段包括 `Invoice.InvoiceDate`、`Employee.BirthDate`、`Employee.HireDate`。
- 该数据库没有视图；所有业务数据都存储在上述 11 张表中。
