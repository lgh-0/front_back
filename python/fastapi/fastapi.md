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

## 3.路由
```python
@app.get("/hello")
def say_hello():
    return {"msg": "hello"}
# 这时候 /hello 就是一个 路由路径，对应一个后端接口。
```

总结一句话：
- FastAPI 的路由就是 URL → Python 函数 的映射关系。

- @app.get("/xxx")：直接在 app 上定义路由

- @router.get("/xxx")：在子路由上定义路由

app.include_router(router)：把子路由合并到总路由

你提到的“FastAPI 使用方式”

你理解得对，FastAPI 的常见用法就是：

- 连接数据库（SQLAlchemy、TortoiseORM、pyodbc 等）

- 写一些 RESTful API 接口（@get、@post）

- 组织到不同的 APIRouter 里，最后统一在 main.py 挂载到 app

- 这样前端就能通过请求 http://host:port/xxx 调用对应接口。

✅ 所以，app.include_router(login.router) 的意思就是：把 login.py 里定义的那组 API 接口挂到后端总应用 app 上。