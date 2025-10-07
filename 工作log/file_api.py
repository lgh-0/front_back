# 文件查询相关
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import os
import pyodbc
from datetime import datetime
from typing import Optional, List
import uuid
import shutil
from pathlib import Path

router = APIRouter()

class Settings(BaseSettings):
    db_server: str = os.getenv("DB_SERVER", "192.168.41.57")
    db_database: str = os.getenv("DB_DATABASE", "Abus2020")
    db_username: str = os.getenv("DB_USERNAME", "sa")
    db_password: str = os.getenv("DB_PASSWORD", "3518i")

auth_settings = Settings()

class FileCreate(BaseModel):
    类别: Optional[str] = None
    细分项目: Optional[str] = None
    文件名称: Optional[str] = None
    制作日期: Optional[str] = None
    负责人: Optional[str] = None
    文件类型: Optional[str] = None
    备注: Optional[str] = None

class LinkCreate(BaseModel):
    类别: str
    细分项目: str
    文件名称: str
    制作日期: str
    文件类型: str
    链接地址: str
    负责人: Optional[str] = "admin"

def get_db_connection():
    conn_str = (
        f"DRIVER={{SQL Server}};SERVER={auth_settings.db_server};DATABASE={auth_settings.db_database};"
        f"UID={auth_settings.db_username};PWD={auth_settings.db_password};"
    )
    try:
        return pyodbc.connect(conn_str)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"数据库连接失败: {exc}")

# 获取上传文件目录
def get_upload_dir():
    # 改为使用绝对路径 D:\uploads
    upload_dir = r"D:\\uploads"
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir

def format_date(date_value):
    """格式化日期字段，处理datetime对象和字符串"""
    if not date_value:
        return ""
    
    if hasattr(date_value, 'strftime'):  # 如果是datetime对象
        return date_value.strftime('%Y-%m-%d')
    else:  # 如果是字符串
        date_str = str(date_value)
        # 如果字符串包含时间部分，只取日期部分
        if ' ' in date_str:
            date_str = date_str.split(' ')[0]
        return date_str

@router.get("/file", summary="查询文件列表")
async def get_files(
    类别: Optional[str] = Query(None, description="类别筛选"),
    细分项目: Optional[str] = Query(None, description="细分项目筛选"),
    文件名称: Optional[str] = Query(None, description="文件名称筛选"),
    制作日期: Optional[str] = Query(None, description="制作日期筛选"),
    文件类型: Optional[str] = Query(None, description="文件类型筛选"),
    负责人: Optional[str] = Query(None, description="负责人筛选")
):
    """查询文件列表，支持多条件筛选"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 构建SQL查询语句 - 注意表名中的特殊字符
        sql = """
        SELECT [id], [类别], [细分项目], [文件名称], [制作日期], [负责人], [文件类型], [备注]
        FROM [Abus2020].[dbo].[FolderCategories​]
        WHERE 1=1
        """
        params = []
        
        # 添加筛选条件
        if 类别:
            sql += " AND [类别] LIKE ?"
            params.append(f"%{类别}%")
        
        if 细分项目:
            sql += " AND [细分项目] LIKE ?"
            params.append(f"%{细分项目}%")
            
        if 文件名称:
            sql += " AND [文件名称] LIKE ?"
            params.append(f"%{文件名称}%")
            
        if 制作日期:
            sql += " AND CONVERT(VARCHAR(10), [制作日期], 120) = ?"
            params.append(制作日期)
            
        if 文件类型:
            sql += " AND [文件类型] LIKE ?"
            params.append(f"%{文件类型}%")
            
        if 负责人:
            sql += " AND [负责人] LIKE ?"
            params.append(f"%{负责人}%")
        
        sql += " ORDER BY [制作日期] DESC, [id] DESC"
        
        cursor.execute(sql, params)
        files = []
        
        for row in cursor.fetchall():
            # 从备注字段中提取文件URL
            备注 = row[7] or ""
            url = ""
            if 备注:
                # 备注格式可能是: "/static/uploads/filename.ext" 或 "/static/uploads/filename.ext | 描述: xxx | 文件大小: xxx"
                parts = 备注.split(' | ')
                if parts[0].startswith('/static/'):
                    url = parts[0]
                elif parts[0].startswith('/api/static/'):
                    url = parts[0]
            
            file_data = {
                "id": row[0],
                "类别": row[1] or "",
                "细分项目": row[2] or "",
                "文件名称": row[3] or "",
                "制作日期": format_date(row[4]),
                "负责人": row[5] or "",
                "文件类型": row[6] or "",
                "备注": row[7] or "",
                "url": url
            }
            files.append(file_data)
        
        return {
            "status": "success",
            "data": files,
            "total": len(files),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as exc:
        print(f"查询文件失败: {exc}")
        raise HTTPException(status_code=500, detail=f"服务器错误: {exc}")
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

@router.post("/file/upload", summary="上传文件")
async def upload_file(
    file: UploadFile = File(...),
    类别: str = Form(...),
    细分项目: str = Form(...),
    文件名称: str = Form(...),
    制作日期: str = Form(...),
    文件类型: str = Form(...),
    负责人: str = Form(default="admin"),
    备注: str = Form(default="")
):
    """上传文件并保存记录到数据库"""
    conn = None
    try:
        # 验证必填字段
        if not all([类别, 细分项目, 文件名称, 制作日期, 文件类型]):
            raise HTTPException(status_code=400, detail="请填写所有必填字段")
        
        # 验证文件类型
        allowed_extensions = ['.doc', '.docx', '.xls', '.xlsx', '.pdf', '.ppt', '.pptx']
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail=f"不支持的文件类型: {file_ext}")
        
        # 生成唯一文件名
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # 精确到毫秒
        unique_filename = f"{timestamp}{file_ext}"
        
        # 保存文件
        upload_dir = get_upload_dir()
        file_path = os.path.join(upload_dir, unique_filename)
        file_url = f"/static/uploads/{unique_filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 保存到数据库
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 插入文件记录到现有表
        insert_sql = """
        INSERT INTO [Abus2020].[dbo].[FolderCategories​] 
        ([类别], [细分项目], [文件名称], [制作日期], [负责人], [文件类型], [备注])
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        # 将文件URL存储在备注字段中
        备注_with_url = file_url
        if 备注:
            备注_with_url += f" | 备注: {备注}"
        
        cursor.execute(insert_sql, (
            类别, 细分项目, 文件名称, 制作日期, 负责人, 文件类型, 备注_with_url
        ))
        conn.commit()
        
        return {
            "status": "success",
            "message": "文件上传成功",
            "data": {
                "filename": unique_filename,
                "url": file_url,
                "size": file.size if hasattr(file, 'size') else 0
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as exc:
        print(f"文件上传失败: {exc}")
        # 如果数据库插入失败，删除已上传的文件
        try:
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass
        raise HTTPException(status_code=500, detail=f"文件上传失败: {exc}")
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

@router.get("/file/{file_id}", summary="获取文件详情")
async def get_file_detail(file_id: int):
    """获取单个文件的详细信息"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT [id], [类别], [细分项目], [文件名称], [制作日期], [负责人], [文件类型], [备注]
            FROM [Abus2020].[dbo].[FolderCategories​]
            WHERE [id] = ?
        """, file_id)
        
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        # 从备注字段中提取文件URL
        备注 = row[7] or ""
        url = ""
        if 备注:
            parts = 备注.split(' | ')
            if parts[0].startswith('/static/'):
                url = parts[0]
            elif parts[0].startswith('/api/static/'):
                url = parts[0]
        
        file_data = {
            "id": row[0],
            "类别": row[1] or "",
            "细分项目": row[2] or "",
            "文件名称": row[3] or "",
            "制作日期": format_date(row[4]),
            "负责人": row[5] or "",
            "文件类型": row[6] or "",
            "备注": row[7] or "",
            "url": url
        }
        
        return {
            "status": "success",
            "data": file_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as exc:
        print(f"获取文件详情失败: {exc}")
        raise HTTPException(status_code=500, detail=f"服务器错误: {exc}")
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

@router.delete("/file/{file_id}", summary="删除文件")
async def delete_file(file_id: int):
    """删除文件记录和物理文件"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 检查文件是否存在
        cursor.execute("""
            SELECT COUNT(*) FROM [Abus2020].[dbo].[FolderCategories​] WHERE [id] = ?
        """, file_id)
        
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        # 删除数据库记录
        cursor.execute("DELETE FROM [Abus2020].[dbo].[FolderCategories​] WHERE [id] = ?", file_id)
        conn.commit()
        
        return {
            "status": "success",
            "message": "文件删除成功",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as exc:
        print(f"删除文件失败: {exc}")
        raise HTTPException(status_code=500, detail=f"服务器错误: {exc}")
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

@router.put("/file/{file_id}", summary="更新文件信息")
async def update_file(file_id: int, file_data: FileCreate):
    """更新文件信息（不包括文件本身）"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 检查文件是否存在
        cursor.execute("SELECT COUNT(*) FROM [Abus2020].[dbo].[FolderCategories​] WHERE [id] = ?", file_id)
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        # 构建更新SQL
        update_fields = []
        params = []
        
        if file_data.类别 is not None:
            update_fields.append("[类别] = ?")
            params.append(file_data.类别)
        
        if file_data.细分项目 is not None:
            update_fields.append("[细分项目] = ?")
            params.append(file_data.细分项目)
            
        if file_data.文件名称 is not None:
            update_fields.append("[文件名称] = ?")
            params.append(file_data.文件名称)
            
        if file_data.制作日期 is not None:
            update_fields.append("[制作日期] = ?")
            params.append(file_data.制作日期)
            
        if file_data.负责人 is not None:
            update_fields.append("[负责人] = ?")
            params.append(file_data.负责人)
            
        if file_data.文件类型 is not None:
            update_fields.append("[文件类型] = ?")
            params.append(file_data.文件类型)
            
        if file_data.备注 is not None:
            update_fields.append("[备注] = ?")
            params.append(file_data.备注)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="没有要更新的字段")
        
        params.append(file_id)
        update_sql = f"""
        UPDATE [Abus2020].[dbo].[FolderCategories​] 
        SET {', '.join(update_fields)}
        WHERE [id] = ?
        """
        
        cursor.execute(update_sql, params)
        conn.commit()
        
        return {
            "status": "success",
            "message": "文件信息更新成功",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as exc:
        print(f"更新文件信息失败: {exc}")
        raise HTTPException(status_code=500, detail=f"服务器错误: {exc}")
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

@router.get("/file/stats/summary", summary="文件统计信息")
async def get_file_stats():
    """获取文件统计信息"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 总文件数
        cursor.execute("SELECT COUNT(*) FROM [Abus2020].[dbo].[FolderCategories​]")
        total_files = cursor.fetchone()[0]
        
        # 按类别统计
        cursor.execute("""
            SELECT [类别], COUNT(*) as count 
            FROM [Abus2020].[dbo].[FolderCategories​] 
            WHERE [类别] IS NOT NULL 
            GROUP BY [类别] 
            ORDER BY count DESC
        """)
        category_stats = [{"category": row[0], "count": row[1]} for row in cursor.fetchall()]
        
        # 按文件类型统计
        cursor.execute("""
            SELECT [文件类型], COUNT(*) as count 
            FROM [Abus2020].[dbo].[FolderCategories​] 
            WHERE [文件类型] IS NOT NULL 
            GROUP BY [文件类型] 
            ORDER BY count DESC
        """)
        filetype_stats = [{"type": row[0], "count": row[1]} for row in cursor.fetchall()]
        
        # 最近上传的文件
        cursor.execute("""
            SELECT TOP 5 [文件名称], [制作日期], [类别]
            FROM [Abus2020].[dbo].[FolderCategories​] 
            ORDER BY [制作日期] DESC, [id] DESC
        """)
        recent_files = []
        for row in cursor.fetchall():
            recent_files.append({
                "filename": row[0],
                "date": format_date(row[1]),
                "category": row[2] or ""
            })
        
        return {
            "status": "success",
            "data": {
                "total_files": total_files,
                "category_stats": category_stats,
                "filetype_stats": filetype_stats,
                "recent_files": recent_files
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as exc:
        print(f"获取统计信息失败: {exc}")
        raise HTTPException(status_code=500, detail=f"服务器错误: {exc}")
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

@router.get("/file/download/{file_id}", summary="下载文件")
async def download_file(file_id: int):
    """根据文件ID下载文件"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取文件信息
        cursor.execute("""
            SELECT [文件名称], [备注] FROM [Abus2020].[dbo].[FolderCategories​] WHERE [id] = ?
        """, file_id)
        
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        文件名称 = row[0]
        备注 = row[1] or ""
        
        # 从备注中提取文件URL
        file_url = ""
        if 备注:
            parts = 备注.split(' | ')
            if parts[0].startswith('/static/'):
                file_url = parts[0]
            elif parts[0].startswith('/api/static/'):
                file_url = parts[0]
        
        if not file_url:
            raise HTTPException(status_code=404, detail="文件路径不存在")
        
        # 构建实际文件路径
        if file_url.startswith('/static/uploads/'):
            filename = os.path.basename(file_url)
            upload_dir = get_upload_dir()
            file_path = os.path.join(upload_dir, filename)
        else:
            raise HTTPException(status_code=404, detail="无效的文件路径")
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="物理文件不存在")
        
        # 返回文件
        return FileResponse(
            path=file_path,
            filename=文件名称,
            media_type='application/octet-stream'
        )
        
    except HTTPException:
        raise
    except Exception as exc:
        print(f"下载文件失败: {exc}")
        raise HTTPException(status_code=500, detail=f"服务器错误: {exc}")
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

@router.get("/file/view/{file_id}", summary="预览文件")
async def view_file(file_id: int):
    """根据文件ID预览文件"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取文件信息
        cursor.execute("""
            SELECT [文件名称], [文件类型], [备注] FROM [Abus2020].[dbo].[FolderCategories​] WHERE [id] = ?
        """, file_id)
        
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        文件名称 = row[0]
        文件类型 = row[1] or ""
        备注 = row[2] or ""
        
        # 从备注中提取文件URL
        file_url = ""
        if 备注:
            parts = 备注.split(' | ')
            if parts[0].startswith('/static/'):
                file_url = parts[0]
            elif parts[0].startswith('/api/static/'):
                file_url = parts[0]
        
        if not file_url:
            raise HTTPException(status_code=404, detail="文件路径不存在")
        
        # 构建实际文件路径
        if file_url.startswith('/static/uploads/'):
            filename = os.path.basename(file_url)
            upload_dir = get_upload_dir()
            file_path = os.path.join(upload_dir, filename)
        else:
            raise HTTPException(status_code=404, detail="无效的文件路径")
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="物理文件不存在")
        
        # 根据文件类型设置媒体类型
        media_type = "application/octet-stream"
        if 文件类型.lower() in ['pdf']:
            media_type = "application/pdf"
        elif 文件类型.lower() in ['jpg', 'jpeg', 'png', 'gif']:
            media_type = f"image/{文件类型.lower()}"
        elif 文件类型.lower() in ['docx']:
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        elif 文件类型.lower() in ['xlsx']:
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        
        # 返回文件用于预览
        return FileResponse(
            path=file_path,
            media_type=media_type,
            headers={"Content-Disposition": "inline"}
        )
        
    except HTTPException:
        raise
    except Exception as exc:
        print(f"预览文件失败: {exc}")
        raise HTTPException(status_code=500, detail=f"服务器错误: {exc}")
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

# 2025-10-7新增上传链接
@router.post("/file/upload-link", summary="上传链接")
async def upload_link(link_data: LinkCreate):
    """保存链接到数据库"""
    conn = None
    try:
        # 验证必填字段
        if not all([link_data.类别, link_data.细分项目, link_data.文件名称, link_data.制作日期, link_data.链接地址]):
            raise HTTPException(status_code=400, detail="请填写所有必填字段")
        
        # 处理链接格式：如果没有协议，自动添加 https://（支持各种新闻链接）
        link_url = link_data.链接地址.strip()
        if not link_url.startswith(('http://', 'https://', 'ftp://')):
            # 如果没有协议，自动添加 https://
            link_data.链接地址 = 'https://' + link_url
        else:
            link_data.链接地址 = link_url
        
        # 保存到数据库
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 插入链接记录
        insert_sql = """
        INSERT INTO [Abus2020].[dbo].[FolderCategories​] 
        ([类别], [细分项目], [文件名称], [制作日期], [负责人], [文件类型], [备注])
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        # 将链接地址存储在备注字段中
        备注_with_link = link_data.链接地址
        
        cursor.execute(insert_sql, (
            link_data.类别, 
            link_data.细分项目, 
            link_data.文件名称, 
            link_data.制作日期, 
            link_data.负责人, 
            '链接',  # 文件类型固定为"链接"
            备注_with_link
        ))
        conn.commit()
        
        return {
            "status": "success",
            "message": "链接添加成功",
            "data": {
                "link": link_data.链接地址
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as exc:
        print(f"链接添加失败: {exc}")
        raise HTTPException(status_code=500, detail=f"链接添加失败: {exc}")
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass


@router.get("/file/test", summary="测试数据库连接")
async def test_connection():
    """测试数据库连接"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        # 检查表是否存在
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_name = 'FolderCategories​' AND table_schema = 'dbo'
        """)
        table_exists = cursor.fetchone()[0] > 0
        
        return {
            "status": "success",
            "message": "数据库连接正常",
            "test_result": result[0] if result else None,
            "table_exists": table_exists,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as exc:
        print(f"数据库连接测试失败: {exc}")
        raise HTTPException(status_code=500, detail=f"数据库连接失败: {exc}")
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass
