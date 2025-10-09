from fastapi import APIRouter, HTTPException, params, status
from fastapi_cache.decorator import cache
from fastapi import Query
from datetime import date, datetime
import pyodbc
import pandas as pd
import numpy as np
from typing import Optional

router=APIRouter()
# 表
# 1️⃣ huayueerp.dbo.obas_part
# 2️⃣ huayueerp.dbo.obas_part1
# 3️⃣ huayueerp.dbo.obas_part_type
# 4️⃣ abuspricerp.dbo.发票报表组合装产品设置表


DB_SERVER = "192.168.1.1"
DB_DATABASE = "huayueerp"
DB_USERNAME = "sa"
DB_PASSWORD = "3518i"

# 改函数返回的是一个数据库连接对象pyodbc.Connection对象
def get_db_connection():
    conn_str = f"DRIVER={{SQL Server}};SERVER={DB_SERVER};DATABASE={DB_DATABASE};UID={DB_USERNAME};PWD={DB_PASSWORD};CHARSET=UTF8"
    return pyodbc.connect(conn_str)

@router.get("/product",summary="产品查询",description="产品数据")
@cache(expire=3600)
async def get_energy_data(
    产品系列: Optional[str] = Query(None, description="系列"),
    料品规格: Optional[str] = Query(None, description="料品规格"),
    料品编号: Optional[str] = Query(None,description="料品编号")
):
    if not 产品系列 and not 料品规格 and not 料品编号:
        return {
                "status": "success",
                "data": [],
                "total": 0,
                "timestamp": datetime.now().strftime('%Y-%m-%d')
        }
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        select * from(
            SELECT 
                obas_part.item_no 料品编号,
                obas_part.part_name 料品名称,
                obas_part.part_spec 料品规格,
                CASE 
                    WHEN obas_part.define4 = '是' THEN ss.发票报表产品名称
                    ELSE obas_part.define1
                END AS 产品系列,
            
                obas_part.define4 组合件,
                
                case 
                    when obas_part.act_sw = 1 then '已审核'
                end as 审核状态,
                obas_part.create_date 创建日期
            FROM obas_part
            INNER JOIN obas_part1 ON obas_part1.part_no = obas_part.part_no
            INNER JOIN obas_part_type ON obas_part_type.type_no = obas_part1.part_type
            LEFT JOIN 发票报表组合装产品设置表 ss ON obas_part.item_no = ss.item_no

            where obas_part.item_no like '1%' and obas_part.act_sw=1
        ) as product_data
        where 1=1
        AND 产品系列 IS NOT NULL
        
        """
        params=[]
        conditions = []
        if 料品编号:
            conditions.append("料品编号 LIKE ?")
            params.append(f"%{料品编号}%")

        if 产品系列:
            conditions.append("产品系列 LIKE ?")
            params.append(f"%{产品系列}%")

        if 料品规格:
            conditions.append("料品规格 LIKE ?")
            params.append(f"%{料品规格}%")
        if conditions:
            full_query = query + " and " + " and ".join(conditions) + " order by 创建日期 desc"
        else:
            full_query = query + " order by 创建日期 desc"
        cursor.execute(full_query,params)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        result =[]
        for row in rows:
            row_dict={}
            for i,value in enumerate(row):
                if isinstance(value,(datetime,pd.Timestamp)):
                    value=value.isoformat()

                row_dict[columns[i]]=value
            result.append(row_dict)
        
        cursor.close()
        conn.close()
        return{
            "status":"success",
            "data":result,
            "total":len(result),
            "timestamp":datetime.now().isoformat()
        }
    except pyodbc.Error as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库错误: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"服务器错误: {str(e)}"
        )

@router.get("/product/stats", summary="产品系列统计", description="获取产品系列统计信息")
@cache(expire=3600)
async def get_product_stats(
    产品系列: Optional[str] = Query(None, description="系列")
):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if 产品系列:
            query = """
            SELECT 
                CASE 
                    WHEN obas_part.define4 = '是' THEN ss.发票报表产品名称
                    ELSE obas_part.define1
                END AS 产品系列,
                COUNT(*) as 数量
            FROM obas_part
            INNER JOIN obas_part1 ON obas_part1.part_no = obas_part.part_no
            INNER JOIN obas_part_type ON obas_part_type.type_no = obas_part1.part_type
            LEFT JOIN abuspricerp.dbo.发票报表组合装产品设置表 ss ON obas_part.item_no = ss.item_no
            WHERE obas_part.item_no like '1%' 
            AND obas_part.act_sw=1
            AND (
                CASE 
                    WHEN obas_part.define4 = '是' THEN ss.发票报表产品名称
                    ELSE obas_part.define1
                END
            ) LIKE ?
            AND (
                CASE 
                    WHEN obas_part.define4 = '是' THEN ss.发票报表产品名称
                    ELSE obas_part.define1
                END
            ) IS NOT NULL
            GROUP BY 
                CASE 
                    WHEN obas_part.define4 = '是' THEN ss.发票报表产品名称
                    ELSE obas_part.define1
                END
            """
            params = [f"%{产品系列}%"]
        else:
            query = """
            SELECT 
                CASE 
                    WHEN obas_part.define4 = '是' THEN ss.发票报表产品名称
                    ELSE obas_part.define1
                END AS 产品系列,
                COUNT(*) as 数量
            FROM obas_part
            INNER JOIN obas_part1 ON obas_part1.part_no = obas_part.part_no
            INNER JOIN obas_part_type ON obas_part_type.type_no = obas_part1.part_type
            LEFT JOIN abuspricerp.dbo.发票报表组合装产品设置表 ss ON obas_part.item_no = ss.item_no
            WHERE obas_part.item_no like '1%' 
            AND obas_part.act_sw=1
            AND (
                CASE
                    WHEN obas_part.define4 = '是' THEN ss.发票报表产品名称
                    ELSE obas_part.define1
                END
            ) IS NOT NULL
            GROUP BY 
                CASE 
                    WHEN obas_part.define4 = '是' THEN ss.发票报表产品名称
                    ELSE obas_part.define1
                END
            """
            params = []

        cursor.execute(query, params)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            row_dict = {}
            for i, value in enumerate(row):
                row_dict[columns[i]] = value
            result.append(row_dict)
        
        cursor.close()
        conn.close()
        
        return {
            "status": "success",
            "data": result,
            "total": len(result),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"服务器错误: {str(e)}"
        )

# 2025-10-9新增的饼图和直方图需求
'''
正如你说的，这是一个路由装饰器，告诉 FastAPI：这是一个 HTTP GET 请求接口；路径为 /product/chart-data；
文档中显示的标题和描述分别由 summary 与 description 指定

这个是 缓存装饰器（来自第三方库，比如 fastapi-cache2）。
意思是：如果启用缓存，该接口在第一次执行后，会把返回结果缓存起来，后面相同请求直接返回缓存数据。
expire=3600 表示缓存过期时间为 3600秒（1小时）。
它的作用是避免频繁查询数据库、减少服务器压力。
'''
@router.get("/product/chart-data", summary="产品类型图表数据", description="获取产品类型统计数据用于饼图和柱状图展示")
@cache(expire=3600)
async def get_product_chart_data():
    """
    获取产品类型统计数据，包括类型名称、系列数量和占比百分比
    3️⃣ async def get_product_chart_data():

这里的 async 表示异步函数。

🔹作用：

异步函数能让 FastAPI 在等待 I/O（例如数据库查询）时不阻塞其他请求；

它使服务器能同时处理多个请求，提高并发性能。

🔹你问的重点：

不用和 await 同时出现的吗？

✅ 结论是：

一般情况下，async 函数里会配合 await 调用异步操作（如异步数据库或网络请求）；

但如果调用的库（如 pyodbc）是同步的，你仍可以用 async 修饰，只是异步优势没发挥出来。

所以这里虽然写了 async，但函数内部操作是同步的（pyodbc 不是异步库），这在 FastAPI 中也不会报错，只是不会获得真正的异步性能。
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        '''
        conn = get_db_connection()
conn 是数据库连接对象；一般来说，它来自 pyodbc.connect(...)；
典型返回值是一个 pyodbc.Connection 对象；它代表与数据库（如 SQL Server）的一个会话。 
cursor = conn.cursor()
这行创建一个游标对象；
游标是用来执行 SQL 语句和获取查询结果的。
你可以理解为：
“数据库连接” 是一扇门，
“游标” 是通过这扇门交互的“手”。     
        '''
        # 执行复杂的统计查询
        query = """
        SELECT
            t.type_name,
            COUNT(*) AS 系列数量,
            CAST(COUNT(*) * 100.0 / 总系列.总数量 AS DECIMAL(5,2)) AS 占比百分比
        FROM
        (
            SELECT 
                系列统计.产品系列,
                系列统计.数量 AS 系列总量,
                t2.type_name
            FROM
            (
                SELECT 
                    CASE 
                        WHEN p.define4 = '是' THEN ss.发票报表产品名称
                        ELSE p.define1
                    END AS 产品系列,
                    COUNT(*) AS 数量
                FROM obas_part p
                LEFT JOIN obas_part1 p1 ON p1.part_no = p.part_no
                LEFT JOIN abuspricerp.dbo.发票报表组合装产品设置表 ss 
                    ON p.item_no = ss.item_no
                WHERE p.item_no LIKE '1%' 
                  AND p.act_sw = 1
                  AND (
                      CASE 
                          WHEN p.define4 = '是' THEN ss.发票报表产品名称
                          ELSE p.define1
                      END
                  ) IS NOT NULL
                GROUP BY 
                    CASE 
                        WHEN p.define4 = '是' THEN ss.发票报表产品名称
                        ELSE p.define1
                    END
            ) 系列统计
            LEFT JOIN
            (
                SELECT t1.产品系列, MIN(t1.type_name) AS type_name
                FROM
                (
                    SELECT DISTINCT
                        CASE 
                            WHEN p.define4 = '是' THEN ss.发票报表产品名称
                            ELSE p.define1
                        END AS 产品系列,
                        t.type_name
                    FROM obas_part p
                    LEFT JOIN obas_part1 p1 ON p1.part_no = p.part_no
                    LEFT JOIN obas_part_type t ON t.type_no = p1.part_type
                    LEFT JOIN abuspricerp.dbo.发票报表组合装产品设置表 ss 
                        ON p.item_no = ss.item_no
                    WHERE p.item_no LIKE '1%' 
                      AND p.act_sw = 1
                      AND (
                          CASE 
                              WHEN p.define4 = '是' THEN ss.发票报表产品名称
                              ELSE p.define1
                          END
                      ) IS NOT NULL
                ) t1
                GROUP BY t1.产品系列
            ) t2
            ON 系列统计.产品系列 = t2.产品系列
        ) t
        CROSS JOIN
        (
            SELECT COUNT(*) AS 总数量
            FROM
            (
                SELECT 
                    系列统计.产品系列
                FROM
                (
                    SELECT 
                        CASE 
                            WHEN p.define4 = '是' THEN ss.发票报表产品名称
                            ELSE p.define1
                        END AS 产品系列,
                        COUNT(*) AS 数量
                    FROM obas_part p
                    LEFT JOIN obas_part1 p1 ON p1.part_no = p.part_no
                    LEFT JOIN abuspricerp.dbo.发票报表组合装产品设置表 ss 
                        ON p.item_no = ss.item_no
                    WHERE p.item_no LIKE '1%' 
                      AND p.act_sw = 1
                      AND (
                          CASE 
                              WHEN p.define4 = '是' THEN ss.发票报表产品名称
                              ELSE p.define1
                          END
                      ) IS NOT NULL
                    GROUP BY 
                        CASE 
                            WHEN p.define4 = '是' THEN ss.发票报表产品名称
                            ELSE p.define1
                        END
                ) 系列统计
            ) t_total
        ) 总系列
        WHERE t.type_name IS NOT NULL
        GROUP BY t.type_name, 总系列.总数量
        ORDER BY 系列数量 DESC
        """
        
        print("开始执行产品类型图表数据查询...")
        cursor.execute(query)
        rows = cursor.fetchall()
        print(f"查询完成，共获取 {len(rows)} 条数据")
        '''
rows = cursor.fetchall()
fetchall() 的意思是“取出所有查询结果”；
它会返回一个列表，每个元素是一行数据（通常是 tuple）。
例如：rows = [('锁芯', 10, 20.5), ('把手', 5, 10.2)]        
        '''
        # 组织数据结构
        result = []
        for row in rows:
            type_name = row[0]
            series_count = row[1]
            percentage = float(row[2])
            
            print(f"类型: {type_name}, 系列数量: {series_count}, 占比: {percentage}%")
            
            result.append({
                'type_name': type_name,
                '系列数量': int(series_count),
                '占比百分比': percentage
            })
        '''这是在把 SQL 查询结果转化成更方便前端使用的 JSON 格式。
最终 result 会是：
[
  {"type_name": "锁芯", "系列数量": 10, "占比百分比": 20.5},
  {"type_name": "把手", "系列数量": 5, "占比百分比": 10.2}
]
        '''
        cursor.close()
        conn.close()
        '''
        这就是接口的最终响应，FastAPI 会自动转成 JSON 返回给前端。
        '''
        return {
            "status": "success",
            "data": result,
            "total": len(result),
            "timestamp": datetime.now().isoformat()
        }
    except pyodbc.Error as e:
        print(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库错误: {str(e)}"
        )
    except Exception as e:
        print(f"服务器错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"服务器错误: {str(e)}"
        )

