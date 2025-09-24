# 一、连接数据库
## 1.连接sql server
```python
#模板字符串最后的分号可加可不加
# 一种是使用复杂点的
import pyodbc
import os
from fastapi import HTTPException
from pydantic import BaseSettings
class Settings(BaseSettings):
    """Database settings – fall back to environment variables so they can be
    overridden without changing the code. Defaults match the values provided
    by the user in the chat instructions."""

    db_server: str = os.getenv("DB_SERVER", "192.168.1.1")
    db_database: str = os.getenv("DB_DATABASE", "huayueerp")
    db_username: str = os.getenv("DB_USERNAME", "sa")
    db_password: str = os.getenv("DB_PASSWORD", "3518i")

settings = Settings()


def get_db_connection():
    """Return a live pyodbc connection to the SQL-Server instance."""
    conn_str = (
        f"DRIVER={{SQL Server}};SERVER={settings.db_server};DATABASE={settings.db_database};"
        f"UID={settings.db_username};PWD={settings.db_password};"
    )
    try:
        return pyodbc.connect(conn_str)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"数据库连接失败: {exc}")

'''
Settings 是一个类，环境变量优先，没设置就用默认值。

os.getenv 是获取环境变量的函数。

f"..." 是模板字符串。

pyodbc.connect(...) 返回的是一个 pyodbc.Connection 对象，用来和数据库交互。

print(conn) 打印出来的只是对象的内存地址，而不是 SQL Server 的状态。
pyodbc.connect(...) 返回的是一个 Connection 对象，类型是 pyodbc.Connection。

这个对象相当于一个「数据库连接」，你可以用它：

.cursor() 获取游标执行 SQL

.commit() 提交事务

.close() 关闭连接
'''
# 另一种是使用简单点的
def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS,1433;DATABASE=demo1;UID=sa;PWD=1432"
    )
    print("数据库连接成功")
    print(conn)
    return conn

```


## 2. 连接mysql
```python
import pymysql
def get_connection():
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="1432",
        database="sign2",
        charset="utf8mb4",   # 建议 utf8mb4
        cursorclass=pymysql.cursors.DictCursor
    )
    print("数据库连接成功")
    return conn

```