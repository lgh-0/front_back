无密码window登录验证`sqlcmd -S localhost -d demo1 -E`

SELECT * FROM dbo.table1;
GO
真正有用
`sqlcmd -S localhost -U sa -P 1432 -d demo1`

下面的目录输出会好看些
`sqlcmd -S localhost -d demo1 -E -W -s"," `
`SELECT * FROM dbo.table1;`
`GO`

下面的命令是设置登录密码
```{shell}
$RegPath = "HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQLServer"
Set-ItemProperty -Path $RegPath -Name "LoginMode" -Value 2

ALTER LOGIN sa WITH PASSWORD = '1432';
ALTER LOGIN sa ENABLE;
GO
EXIT
```

# 一、常用命令

```{shell}
SELECT @@VERSION;
select count(*) from blog.attendance;
# 如果是sqlcmd要加上go语句
SELECT COUNT(*) FROM users WHERE age > 18;
# 虽然你写了 use sign2;，但 DBeaver 的 SQL 编辑器里不会自动执行 use 语句。
```

```{sql}
-- sql server
CREATE TABLE demo1.dbo.Table2 (
	id int NOT NULL,
	number int NULL,
	CONSTRAINT Table2_PK PRIMARY KEY (id)
);
EXEC demo1.sys.sp_addextendedproperty 'MS_Description', N'主键', 'schema', N'dbo', 'table', N'Table2', 'column', N'id';

SELECT COUNT(*) FROM blog.artitles ;

-- 获取某个数据库里的所有表
--上面是sql server的
SELECT TABLE_NAME
FROM demo1.INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE';

-- mysql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'sign2'
  AND table_type = 'BASE TABLE';
```

无论是 Microsoft SQL Server 还是 MySQL，它们的数据库里都有一个叫 INFORMATION_SCHEMA 的系统视图（元数据视图），专门用来存储“关于数据库本身”的信息，比如：
- 数据库里有哪些表（TABLES）

- 表里有哪些列（COLUMNS）

- 各种约束、索引等元信息

- 👉 可以理解为：
INFORMATION_SCHEMA ≈ 系统自动生成的“数据库结构说明书”表。

| 部分                               | 含义                                                                          |
| --------------------------------- | --------------------------------------------------------------------------- |
| `demo1.INFORMATION_SCHEMA.TABLES` | 表示数据库 `demo1` 中的 `INFORMATION_SCHEMA` 模式下的 `TABLES` 视图。它保存了该数据库下**所有表的信息**。 |
| `TABLE_NAME`                      | 这个列表示每张表的名字。                                                                |
| `WHERE TABLE_TYPE = 'BASE TABLE'` | 过滤条件：只要“基本表”（用户自己创建的普通表）。其他可能的类型还有 `VIEW`（视图）、`SYSTEM TABLE`（系统表）等。         |

sql的解释

| 部分                          | 含义                                                               |
| --------------------------- | ---------------------------------------------------------------- |
| `information_schema.tables` | 全局的 `INFORMATION_SCHEMA` 视图，在 MySQL 中它是**所有数据库共用的**，不是某个库下面的子对象。 |
| `table_schema = 'sign2'`    | 指定要查询的数据库名。MySQL 必须这样写，因为它的 `INFORMATION_SCHEMA` 是全局的。           |
| `table_type = 'BASE TABLE'` | 同样是过滤出用户创建的普通表。                                                  |

| 对比项                       | SQL Server                                   | MySQL                          |
| ------------------------- | -------------------------------------------- | ------------------------------ |
| `INFORMATION_SCHEMA` 所在位置 | 每个数据库下都有自己的 `INFORMATION_SCHEMA`             | 是全局的，所有数据库共用                   |
| 指定数据库方式                   | 直接在前面加数据库名：`demo1.INFORMATION_SCHEMA.TABLES` | 用条件过滤：`table_schema = 'sign2'` |
| 表类型过滤                     | `TABLE_TYPE = 'BASE TABLE'`                  | `table_type = 'BASE TABLE'`    |
| 是否能查视图                    | 可以（改成 `VIEW`）                                | 可以（改成 `VIEW`）                  |

1. [] 的用法（SQL Server 特有）

在 SQL Server 里，[ ] 用来引用标识符（库名、表名、列名）。

当标识符 包含空格、中文、特殊字符（如 -）、或者与关键字冲突（如 select, order），必须加 []。

例如：

select [工单编号], [订单批号] from [派工单];


即使是英文，如果你担心和关键字冲突（如 order），也可以用 []。

2. 你的语句解析
select 
   [_Identify],
   [工单编号],
   [订单批号],
   ...
from [department2020].[dbo].[派工单]
where [订单批号] = '24-2716XH-KEYSF_022';


✅ 正确：

数据库名 department2020

模式 dbo

表名 派工单（中文，用 [] 包裹正确）

列名 [工单编号]、[订单批号] 等（中文列名，也必须 []）

3. 在 MySQL 里

MySQL 用 反引号 ` ` 作为引用符。

中文列名/表名虽然不推荐，但也能写：

select 
  `工单编号`,
  `订单批号`
from `派工单`
where `订单批号` = '24-2716XH-KEYSF_022';

4. 在 PostgreSQL 里

PostgreSQL 用 双引号 " " 作为引用符。

如果不用双引号，系统会自动把标识符转为小写。

中文名或大小写敏感时要用双引号：

select 
  "工单编号",
  "订单批号"
from "派工单"
where "订单批号" = '24-2716XH-KEYSF_022';

🔑 总结

SQL Server: []

MySQL: `

PostgreSQL: "

字符串常量在这三个数据库里都是 '单引号'。
数据库、表名、列名如果是中文、带特殊符号、大小写敏感或关键字，必须加对应的引用符。

要不要我帮你写一份这条查询在 三种数据库（SQL Server / MySQL / PostgreSQL） 的完整对照版本？





CREATE TABLE department2020.dbo.派工单 (
	[_Identify] int IDENTITY(1,1) NOT NULL,
	[_Locked] bit NULL,
	[_SortKey] numeric(28,14) NULL,
	PublishDate datetime NULL,
	工单编号 nvarchar(250) COLLATE Chinese_PRC_CI_AS NULL,
	工单状态 nvarchar(16) COLLATE Chinese_PRC_CI_AS NULL,
	生产车间 nvarchar(16) COLLATE Chinese_PRC_CI_AS NULL,
	锁类分区 nvarchar(16) COLLATE Chinese_PRC_CI_AS NULL,
	锁体分区 nvarchar(16) COLLATE Chinese_PRC_CI_AS NULL,
	生产线编号 nvarchar(30) COLLATE Chinese_PRC_CI_AS NULL,
	订单批号 nvarchar(50) COLLATE Chinese_PRC_CI_AS NULL,
	料品编码 nvarchar(50) COLLATE Chinese_PRC_CI_AS NULL,
	料品名称 nvarchar(50) COLLATE Chinese_PRC_CI_AS NULL,
	料品类别 nvarchar(30) COLLATE Chinese_PRC_CI_AS NULL,
	规格型号 nvarchar(255) COLLATE Chinese_PRC_CI_AS NULL,
	规格备注 ntext COLLATE Chinese_PRC_CI_AS NULL,
	订单数量 int NULL,
	计划工时 float NULL,
	计划开始时间 datetime NULL,
	计划完成时间 datetime NULL,
	计划产量 int NULL,
	标准产量 int NULL,
	ERP报工产量 int NULL,
	实际产量 int NULL,
	上报产量 int NULL,
	装嵌计划开始时间 datetime NULL,
	确定交期 datetime NULL,
	工序规格码 nvarchar(30) COLLATE Chinese_PRC_CI_AS NULL,
	工作内容 nvarchar(200) COLLATE Chinese_PRC_CI_AS NULL,
	员工编号 nvarchar(500) COLLATE Chinese_PRC_CI_AS NULL,
	员工姓名 nvarchar(100) COLLATE Chinese_PRC_CI_AS NULL,
	员工工号 nvarchar(100) COLLATE Chinese_PRC_CI_AS NULL,
	实际开始时间 datetime NULL,
	实际完工时间 datetime NULL,
	实际工时 int NULL,
	合格品数 int NULL,
	不合格数 int NULL,
	任务审核 bit NULL,
	任务审核人 nvarchar(16) COLLATE Chinese_PRC_CI_AS NULL,
	车间确认 bit NULL,
	车间确认时间 datetime NULL,
	车间确认人 nvarchar(16) COLLATE Chinese_PRC_CI_AS NULL,
	备注 ntext COLLATE Chinese_PRC_CI_AS NULL,
	商标 nvarchar(50) COLLATE Chinese_PRC_CI_AS NULL,
	年份代号 nvarchar(50) COLLATE Chinese_PRC_CI_AS NULL,
	邮箱编码 nvarchar(150) COLLATE Chinese_PRC_CI_AS NULL,
	客户 nvarchar(50) COLLATE Chinese_PRC_CI_AS NULL,
	订单备注 ntext COLLATE Chinese_PRC_CI_AS NULL,
	钥匙备注 ntext COLLATE Chinese_PRC_CI_AS NULL,
	计划产能 float NULL,
	安排备注 ntext COLLATE Chinese_PRC_CI_AS NULL,
	JOBExternalID nvarchar(250) COLLATE Chinese_PRC_CI_AS NULL,
	MoExternalId nvarchar(250) COLLATE Chinese_PRC_CI_AS NULL,
	OpExternalId nvarchar(250) COLLATE Chinese_PRC_CI_AS NULL,
	ActExternalID nvarchar(250) COLLATE Chinese_PRC_CI_AS NULL,
	任务编号 nvarchar(30) COLLATE Chinese_PRC_CI_AS NULL,
	任务批号 nvarchar(30) COLLATE Chinese_PRC_CI_AS NULL,
	订单编号 nvarchar(50) COLLATE Chinese_PRC_CI_AS NULL,
	产品内码 nvarchar(30) COLLATE Chinese_PRC_CI_AS NULL,
	publish_history nvarchar(MAX) COLLATE Chinese_PRC_CI_AS NULL,
	PRT_QTY int NULL,
	weight_before real NULL,
	weight_after real NULL,
	update_date datetime NULL,
	old_id int NULL,
	FirstCheck int NULL,
	proccess2 varchar(50) COLLATE Chinese_PRC_CI_AS NULL,
	drawName varchar(50) COLLATE Chinese_PRC_CI_AS NULL,
	drawUrl varchar(50) COLLATE Chinese_PRC_CI_AS NULL,
	[position] varchar(100) COLLATE Chinese_PRC_CI_AS NULL,
	general_name varchar(100) COLLATE Chinese_PRC_CI_AS NULL,
	issued int NULL,
	CONSTRAINT PK_派工单 PRIMARY KEY ([_Identify])
);
 CREATE NONCLUSTERED INDEX IX_派工单_确定交期_Covering ON department2020.dbo.派工单 (  确定交期 ASC  , 生产线编号 ASC  , 料品编码 ASC  )  
	 INCLUDE ( PublishDate , 不合格数 , 订单批号 , 订单数量 , 工单编号 , 工单状态 , 工序规格码 , 规格型号 , 合格品数 , 计划产量 , 计划工时 , 计划开始时间 , 计划完成时间 , 料品名称 , 实际产量 , 实际开始时间 , 实际完工时间 ) 
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE NONCLUSTERED INDEX [NonClusteredIndex-20220916-095654] ON department2020.dbo.派工单 (  计划开始时间 ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE NONCLUSTERED INDEX [NonClusteredIndex-20220916-095728] ON department2020.dbo.派工单 (  锁类分区 ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE NONCLUSTERED INDEX [NonClusteredIndex-20230206-153320] ON department2020.dbo.派工单 (  计划开始时间 ASC  , 生产线编号 ASC  , OpExternalId ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE NONCLUSTERED INDEX [NonClusteredIndex-20230221-154530] ON department2020.dbo.派工单 (  生产线编号 ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE NONCLUSTERED INDEX [_dta_index_派工单_13_1767677345__K17_1_21] ON department2020.dbo.派工单 (  订单数量 ASC  )  
	 INCLUDE ( _Identify , 计划产量 ) 
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE NONCLUSTERED INDEX [_dta_index_派工单_13_1767677345__K52_6_10_11_12_21_23_53] ON department2020.dbo.派工单 (  MoExternalId ASC  )  
	 INCLUDE ( OpExternalId , 订单批号 , 工单状态 , 计划产量 , 料品编码 , 生产线编号 , 实际产量 ) 
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE NONCLUSTERED INDEX [_dta_index_派工单_13_1767677345__K5_1_2_3_4_6_7_8_9_10_11_12_13_14_15_17_18_19_20_21_22_23_24_25_26_27_28_29_30_31_32_33_34_35_36_] ON department2020.dbo.派工单 (  工单编号 ASC  )  
	 INCLUDE ( _Identify , _Locked , _SortKey , ActExternalID , ERP报工产量 , JOBExternalID , MoExternalId , old_id , OpExternalId , PRT_QTY , publish_history , PublishDate , update_date , weight_after , weight_before , 不合格数 , 产品内码 , 车间确认 , 车间确认人 , 车间确认时间 , 订单编号 , 订单批号 , 订单数量 , 工单状态 , 工序规格码 , 工作内容 , 规格型号 , 合格品数 , 计划产量 , 计划产能 , 计划工时 , 计划开始时间 , 计划完成时间 , 客户 , 料品编码 , 料品类别 , 料品名称 , 年份代号 , 确定交期 , 任务编号 , 任务批号 , 任务审核 , 任务审核人 , 商标 , 上报产量 , 生产车间 , 生产线编号 , 实际产量 , 实际工时 , 实际开始时间 , 实际完工时间 , 锁类分区 , 锁体分区 , 邮箱编码 , 员工编号 , 员工工号 , 员工姓名 , 装嵌计划开始时间 ) 
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE NONCLUSTERED INDEX [_dta_index_派工单_13_1767677345__K7_K23_K19_K6_K26_1_2_3_4_5_8_9_10_11_12_13_14_15_17_18_20_21_22_24_25_27_28_29_30_31_32_33_34_] ON department2020.dbo.派工单 (  生产车间 ASC  , 实际产量 ASC  , 计划开始时间 ASC  , 工单状态 ASC  , 确定交期 ASC  )  
	 INCLUDE ( _Identify , _Locked , _SortKey , ActExternalID , ERP报工产量 , JOBExternalID , MoExternalId , old_id , OpExternalId , PRT_QTY , publish_history , PublishDate , update_date , weight_after , weight_before , 不合格数 , 产品内码 , 车间确认 , 车间确认人 , 车间确认时间 , 订单编号 , 订单批号 , 订单数量 , 工单编号 , 工序规格码 , 工作内容 , 规格型号 , 合格品数 , 计划产量 , 计划产能 , 计划工时 , 计划完成时间 , 客户 , 料品编码 , 料品类别 , 料品名称 , 年份代号 , 任务编号 , 任务批号 , 任务审核 , 任务审核人 , 商标 , 上报产量 , 生产线编号 , 实际工时 , 实际开始时间 , 实际完工时间 , 锁类分区 , 锁体分区 , 邮箱编码 , 员工编号 , 员工工号 , 员工姓名 , 装嵌计划开始时间 ) 
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;




CREATE TABLE Dictionary.dbo.Abus2020 (
	表名 nvarchar(255) COLLATE Chinese_PRC_CI_AS NULL,
	中文表名 nvarchar(255) COLLATE Chinese_PRC_CI_AS NULL,
	字段 nvarchar(255) COLLATE Chinese_PRC_CI_AS NULL,
	数据类型 nvarchar(255) COLLATE Chinese_PRC_CI_AS NULL,
	中文字段名 nvarchar(255) COLLATE Chinese_PRC_CI_AS NULL,
	示例 nvarchar(255) COLLATE Chinese_PRC_CI_AS NULL,
	是否主键 nvarchar(255) COLLATE Chinese_PRC_CI_AS NULL,
	是否允许为空 nvarchar(255) COLLATE Chinese_PRC_CI_AS NULL,
	备注 nvarchar(255) COLLATE Chinese_PRC_CI_AS NULL
);


// 派工单1

-- department2020.dbo.派工单1 definition

-- Drop table

-- DROP TABLE department2020.dbo.派工单1;

CREATE TABLE department2020.dbo.派工单1 (
	[_Identify] int IDENTITY(1,1) NOT NULL,
	[_Locked] bit NULL,
	[_SortKey] numeric(28,14) NULL,
	PublishDate datetime NULL,
	工单编号 nvarchar(30) COLLATE Chinese_PRC_CI_AS NULL,
	工单状态 nvarchar(16) COLLATE Chinese_PRC_CI_AS NULL,
	生产车间 nvarchar(16) COLLATE Chinese_PRC_CI_AS NULL,
	锁类分区 nvarchar(16) COLLATE Chinese_PRC_CI_AS NULL,
	锁体分区 nvarchar(16) COLLATE Chinese_PRC_CI_AS NULL,
	生产线编号 nvarchar(30) COLLATE Chinese_PRC_CI_AS NULL,
	订单批号 nvarchar(50) COLLATE Chinese_PRC_CI_AS NULL,
	料品编码 nvarchar(30) COLLATE Chinese_PRC_CI_AS NULL,
	料品名称 nvarchar(30) COLLATE Chinese_PRC_CI_AS NULL,
	料品类别 nvarchar(30) COLLATE Chinese_PRC_CI_AS NULL,
	规格型号 nvarchar(255) COLLATE Chinese_PRC_CI_AS NULL,
	规格备注 ntext COLLATE Chinese_PRC_CI_AS NULL,
	订单数量 int NULL,
	计划工时 float NULL,
	计划开始时间 datetime NULL,
	计划完成时间 datetime NULL,
	计划产量 int NULL,
	ERP报工产量 int NULL,
	实际产量 int NULL,
	装嵌计划开始时间 datetime NULL,
	确定交期 datetime NULL,
	工序规格码 nvarchar(30) COLLATE Chinese_PRC_CI_AS NULL,
	工作内容 nvarchar(200) COLLATE Chinese_PRC_CI_AS NULL,
	员工编号 nvarchar(100) COLLATE Chinese_PRC_CI_AS NULL,
	员工姓名 nvarchar(100) COLLATE Chinese_PRC_CI_AS NULL,
	员工工号 nvarchar(100) COLLATE Chinese_PRC_CI_AS NULL,
	实际开始时间 datetime NULL,
	实际完工时间 datetime NULL,
	实际工时 int NULL,
	合格品数 int NULL,
	不合格数 int NULL,
	任务审核 bit NULL,
	任务审核人 nvarchar(16) COLLATE Chinese_PRC_CI_AS NULL,
	车间确认 bit NULL,
	车间确认时间 datetime NULL,
	车间确认人 nvarchar(16) COLLATE Chinese_PRC_CI_AS NULL,
	备注 ntext COLLATE Chinese_PRC_CI_AS NULL,
	商标 nvarchar(16) COLLATE Chinese_PRC_CI_AS NULL,
	年份代号 nvarchar(16) COLLATE Chinese_PRC_CI_AS NULL,
	邮箱编码 nvarchar(30) COLLATE Chinese_PRC_CI_AS NULL,
	客户 nvarchar(30) COLLATE Chinese_PRC_CI_AS NULL,
	订单备注 ntext COLLATE Chinese_PRC_CI_AS NULL,
	计划产能 float NULL,
	安排备注 ntext COLLATE Chinese_PRC_CI_AS NULL,
	JOBExternalID nvarchar(100) COLLATE Chinese_PRC_CI_AS NULL,
	MoExternalId nvarchar(100) COLLATE Chinese_PRC_CI_AS NULL,
	OpExternalId nvarchar(100) COLLATE Chinese_PRC_CI_AS NULL,
	ActExternalID nvarchar(100) COLLATE Chinese_PRC_CI_AS NULL,
	任务编号 nvarchar(30) COLLATE Chinese_PRC_CI_AS NULL,
	任务批号 nvarchar(30) COLLATE Chinese_PRC_CI_AS NULL,
	订单编号 nvarchar(30) COLLATE Chinese_PRC_CI_AS NULL,
	产品内码 nvarchar(30) COLLATE Chinese_PRC_CI_AS NULL,
	publish_history ntext COLLATE Chinese_PRC_CI_AS NULL
);
