# 22026-1-2新增：历史派工单查询
# from fastapi import APIRouter, HTTPException, Query
# from fastapi_cache.decorator import cache
from datetime import datetime
import pyodbc
import pandas as pd
import numpy as np
from typing import Optional
import os
from pydantic_settings import BaseSettings
import warnings

# warnings.filterwarnings("ignore", category=UserWarning)

# router = APIRouter()

#   conda activate devolopment
class Settings(BaseSettings):
    # 数据库配置
    db_server: str = os.getenv("DB_SERVER_APS", "192.168.41.57")
    db_database: str = os.getenv("DB_DATABASE_APS", "department2020")
    db_username: str = os.getenv("DB_USERNAME_APS", "sa")
    db_password: str = os.getenv("DB_PASSWORD_APS", "3518i")


settings = Settings()


def get_db_conn():
    """获取数据库连接"""
    conn = pyodbc.connect(
        f"DRIVER={{SQL Server}};SERVER={settings.db_server};DATABASE={settings.db_database};UID={settings.db_username};PWD={settings.db_password}"
    )
    return conn

conn = get_db_conn()
if conn:
    print(conn, '\n')
    print("连接数据库成功", '\n')
    print(settings, '\n')
else :
    print("连接数据库失败")

conn = get_db_conn()
cursor = conn.cursor()
query = """
 select distinct [生产车间]   FROM [department2020].[dbo].[PGD_WorkOrder_backup]
 where [生产车间] is not null and [生产车间] != ''
 order by [生产车间]
"""
cursor.execute(query)
rows = cursor.fetchall()
print(rows)
str_number = [row[0] for row in rows if row[0]]
print(str_number)
cursor.close()
conn.close()

dict = {
    "status" : "success",
    "data": str_number,
    "total": len(str_number),
    "timestamp": datetime.now().strftime("%Y-%m-%d  %H:%M:%S"),
}
print(dict)