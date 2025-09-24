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

