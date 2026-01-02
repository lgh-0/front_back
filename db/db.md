- sqlserver 无密码window登录验证`sqlcmd -S localhost -d demo1 -E`

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
```sql
select 
   [_Identify],
   [工单编号],
   [订单批号],
   ...
from [department2020].[dbo].[派工单]
where [订单批号] = '24-2716XH-KEYSF_022';
```

✅ 正确：

数据库名 department2020, 模式 dbo, 表名 派工单（中文，用 [] 包裹正确）

列名 [工单编号]、[订单批号] 等（中文列名，也必须 []）

3. 在 MySQL 里

MySQL 用 反引号  ` 作为引用符。

中文列名/表名虽然不推荐，但也能写：
```sql
select 
  `工单编号`,
  `订单批号`
from `派工单`
where `订单批号` = '24-2716XH-KEYSF_022';
```
4. 在 PostgreSQL 里
PostgreSQL 用 双引号 " " 作为引用符。如果不用双引号，系统会自动把标识符转为小写。中文名或大小写敏感时要用双引号：
```sql
select 
  "工单编号",
  "订单批号"
from "派工单"
where "订单批号" = '24-2716XH-KEYSF_022';
```
🔑 总结
SQL Server: []
MySQL: `
PostgreSQL: "
字符串常量在这三个数据库里都是 '单引号'。
数据库、表名、列名如果是中文、带特殊符号、大小写敏感或关键字，必须加对应的引用符。

要不要我帮你写一份这条查询在 三种数据库（SQL Server / MySQL / PostgreSQL） 的完整对照版本？


```sql
SELECT 
    [datetime]
FROM [IOServer].[dbo].[NoiseSecord]
ORDER BY [datetime] DESC; --日期值大的降序

SELECT 
    value,
    FORMAT(datetime, 'yyyy-MM-ddTHH:mm:ss.fff') AS datetime
FROM [IOServer].[dbo].[NoiseSecord]
WHERE 
    esn = 'LCZS0001'
    AND datetime >= '2025-09-18 00:00:00'
    AND datetime <  '2025-09-19 00:00:00'
ORDER BY datetime ASC; 

✅统计某个表整行不重复的行数
SELECT COUNT(*)
FROM (
    SELECT DISTINCT *
    FROM [department2020].[dbo].[PGD_WorkOrder_backup]
) AS t;

```




