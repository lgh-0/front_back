✅class Settings(BaseSettings):
    db_server: str = os.getenv("DB_SERVER", "192.168.41.57")
    db_database: str = os.getenv("DB_DATABASE", "department2020")
    db_username: str = os.getenv("DB_USERNAME", "sa")
    db_password: str = os.getenv("DB_PASSWORD", "3518i")




```html
<!--  9-26新增销售订单交期修改记录查询 -->
<template>
    <Layout :breadcrumbItems="breadcrumbItems">
        <div>

            
        </div>

    </Layout>

</template>

<script>
import Layout from '@/components/Layout.vue'
import axios from 'axios'
export default {
    name: 'SalesOrderDueDateChangeQuery',
    components: {
        Layout
    },
    data() {
        return {
            breadcrumbItems: ['ABUS Big Data 大数据', '销售订单交期修改记录查询据字典查询'],
        }

    },
    methods: {

    }
}

</script>

<style scoped>
</style>

<!-- 2025-09-26 新增销售订单交期修改记录查询 -->

```
win连接远程服务器win + R mstsc 
# 一、重要
网络共享地址 \\192.168.1.123\Web_ABUS
node的安装地址  C:\Tools\Node

Super 123456

前端修改密码的地方
Reimbursement\ABUS\src\views\system\user-center\index.vue
9-29 完成改密码需求
9-29 新增 增加审批功能，如透明化管理
D:\start-9-19\Devolopment\code-ABUS\src\pages\TransparentManagement\apsRequirements.vue
D:\start-9-19\Devolopment\fastAPI\demo1\routers\apsRequirements.py


 bigdata中工序查询较慢 D:\start-9-19\Devolopment\code-ABUS\src\pages\ABUS_BigData\order.vue
 后端D:\start-9-19\Devolopment\fastAPI\demo1\Abus_BigData_Cal\order.py
ABUS数据系统
admin 密码3edc@YHN


项目管理表：
```sql
CREATE TABLE department2020.dbo.项目管理 (
	RequestID int IDENTITY(1,1) NOT NULL,
	申请时间 datetime NOT NULL,
	项目名称 nvarchar(255) COLLATE Chinese_PRC_CI_AS NOT NULL,
	申请经理 nvarchar(255) COLLATE Chinese_PRC_CI_AS NOT NULL,
	申请原因 nvarchar(MAX) COLLATE Chinese_PRC_CI_AS NOT NULL,
	预计完成时间 date NOT NULL,
	批复意见 nvarchar(MAX) COLLATE Chinese_PRC_CI_AS NULL,
	批复时间 datetime NULL,
	状态 varchar(50) COLLATE Chinese_PRC_CI_AS NULL
);
-- 选择前1000行
SELECT TOP 100 * 
FROM 表名;

select 
-- 查看种类数
-- ✅ 方法1：查看不同的车间名称
SELECT DISTINCT [车间名称]
FROM APS_SUO.dbo.统计后工序
WHERE [车间名称] IS NOT NULL AND [车间名称] <> '';

-- ✅ 方法2：统计有多少个不同的车间名称
SELECT COUNT(DISTINCT [车间名称]) AS 不同车间数量
FROM APS_SUO.dbo.统计后工序
WHERE [车间名称] IS NOT NULL AND [车间名称] <> '';
```
密码
Abus@123456
3edc@YHN

 
万晖五金数据平台 http://report.abushardware.com/
总地址 http://main.abushardware.com/
fastapi-cache==0.1.0
venv命令.\venv\Scripts\activate
uvicorn mains:app --reload
```shell
# 卸载原来的旧包
(venv) PS D:\start-9-19\Devolopment\fastAPI\demo1> pip list | Select-String fastapi-cache

fastapi-cache     0.1.0
fastapi-cache2    0.2.2


(venv) PS D:\start-9-19\Devolopment\fastAPI\demo1> pip uninstall fastapi-cache -y
Found existing installation: fastapi-cache 0.1.0
Uninstalling fastapi-cache-0.1.0:
  Successfully uninstalled fastapi-cache-0.1.0
(venv) PS D:\start-9-19\Devolopment\fastAPI\demo1> pip list | Select-String fastapi-cache

fastapi-cache2    0.2.2

(venv) PS D:\start-9-19\Devolopment\fastAPI\demo1> 
```

```sql
-- 只是查询前一周
SELECT  top 1000
    t.*,
    o.proccess AS 下一道工序ID
FROM (
    SELECT 
        a.JobExternalId AS 工单编号,
        OrderNumber AS 订单批号,
        ResName AS 生产线编号,
        emp_name AS 员工名称,
        ItemExternalId AS 料品编码,
        EachFinishedQty AS 报工数量,
        StartDate AS 开始日期,
        FinishedDate AS 结束日期, 
        b.生产车间,
        CASE 
          WHEN b.OpExternalId IS NULL OR b.OpExternalId NOT LIKE 'op%' 
               THEN b.OpExternalId
          ELSE COALESCE(p.proccess, b.OpExternalId)  -- 防止没匹配到时为空
        END AS 当前工序ID
    FROM APS_FinishedQty a
    LEFT JOIN 派工单_backup b 
        ON a.JobExternalId = b.工单编号
    LEFT JOIN APS.APS_SUO.dbo.item_proccess p
        ON b.OpExternalId = p.opexternalid
       AND b.OpExternalId LIKE 'op%'

    UNION ALL
    SELECT 
        a.JobExternalId, OrderNumber, ResName, emp_name,
        ItemExternalId, EachFinishedQty, StartDate, FinishedDate, 
        b.生产车间,
          CASE 
          WHEN b.OpExternalId IS NULL OR b.OpExternalId NOT LIKE 'op%' 
               THEN b.OpExternalId
          ELSE COALESCE(p.proccess, b.OpExternalId)  -- 防止没匹配到时为空
        END AS 当前工序ID
    FROM APS_FinishedQty_Key a
    LEFT JOIN 派工单_backup b ON a.JobExternalId=b.工单编号

  LEFT JOIN APS.APS_SUO.dbo.item_proccess p
        ON b.OpExternalId = p.opexternalid
       AND b.OpExternalId LIKE 'op%'

    UNION ALL
    SELECT 
        a.JobExternalId, OrderNumber, ResName, emp_name,
        ItemExternalId, EachFinishedQty, StartDate, FinishedDate, 
        b.生产车间,
         CASE 
          WHEN b.OpExternalId IS NULL OR b.OpExternalId NOT LIKE 'op%' 
               THEN b.OpExternalId
          ELSE COALESCE(p.proccess, b.OpExternalId)  -- 防止没匹配到时为空
        END AS 当前工序ID
    FROM APS_FinishedQty_ST a
    LEFT JOIN 派工单_backup b ON a.JobExternalId=b.工单编号
	  LEFT JOIN APS.APS_SUO.dbo.item_proccess p
        ON b.OpExternalId = p.opexternalid
       AND b.OpExternalId LIKE 'op%'

    UNION ALL
    SELECT 
        a.JobExternalId, OrderNumber, ResName, emp_name,
        ItemExternalId, EachFinishedQty, StartDate, FinishedDate, 
        b.生产车间,
          CASE 
          WHEN b.OpExternalId IS NULL OR b.OpExternalId NOT LIKE 'op%' 
               THEN b.OpExternalId
          ELSE COALESCE(p.proccess, b.OpExternalId)  -- 防止没匹配到时为空
        END AS 当前工序ID
    FROM APS_FinishedQty_SX a
    LEFT JOIN 派工单_backup b ON a.JobExternalId=b.工单编号
	  LEFT JOIN APS.APS_SUO.dbo.item_proccess p
        ON b.OpExternalId = p.opexternalid
       AND b.OpExternalId LIKE 'op%'
    UNION ALL
    SELECT 
        a.JobExternalId, OrderNumber, ResName, emp_name,
        ItemExternalId, EachFinishedQty, StartDate, FinishedDate, 
        b.生产车间,
         CASE 
          WHEN b.OpExternalId IS NULL OR b.OpExternalId NOT LIKE 'op%' 
               THEN b.OpExternalId
          ELSE COALESCE(p.proccess, b.OpExternalId)  -- 防止没匹配到时为空
        END AS 当前工序ID
    FROM APS_FinishedQty_SL a
    LEFT JOIN 派工单_backup b ON a.JobExternalId=b.工单编号
	  LEFT JOIN APS.APS_SUO.dbo.item_proccess p
        ON b.OpExternalId = p.opexternalid
       AND b.OpExternalId LIKE 'op%'
) t
LEFT JOIN APS.APS_SUO.dbo.offline_process o
    ON t.当前工序ID = o.before_proccess
	and t.料品编码 like o.item_no +'%'
WHERE t.结束日期 >=getdate()-7




```

SELECT  top 1000
    t.*,
    o.proccess AS 下一道工序ID
FROM (
    SELECT 
        a.JobExternalId AS 工单编号,
        OrderNumber AS 订单批号,
        ResName AS 生产线编号,
        emp_name AS 员工名称,
        ItemExternalId AS 料品编码,
        EachFinishedQty AS 报工数量,
        StartDate AS 开始日期,
        FinishedDate AS 结束日期, 
        b.生产车间,
        CASE 
          WHEN b.OpExternalId IS NULL OR b.OpExternalId NOT LIKE 'op%' 
               THEN b.OpExternalId
          ELSE COALESCE(p.proccess, b.OpExternalId)  -- 防止没匹配到时为空
        END AS 当前工序ID
    FROM APS_FinishedQty a
    LEFT JOIN 派工单_backup b 
        ON a.JobExternalId = b.工单编号
    LEFT JOIN APS.APS_SUO.dbo.item_proccess p
        ON b.OpExternalId = p.opexternalid
       AND b.OpExternalId LIKE 'op%'

    UNION ALL
    SELECT 
        a.JobExternalId, OrderNumber, ResName, emp_name,
        ItemExternalId, EachFinishedQty, StartDate, FinishedDate, 
        b.生产车间,
          CASE 
          WHEN b.OpExternalId IS NULL OR b.OpExternalId NOT LIKE 'op%' 
               THEN b.OpExternalId
          ELSE COALESCE(p.proccess, b.OpExternalId)  -- 防止没匹配到时为空
        END AS 当前工序ID
    FROM APS_FinishedQty_Key a
    LEFT JOIN 派工单_backup b ON a.JobExternalId=b.工单编号

  LEFT JOIN APS.APS_SUO.dbo.item_proccess p
        ON b.OpExternalId = p.opexternalid
       AND b.OpExternalId LIKE 'op%'

    UNION ALL
    SELECT 
        a.JobExternalId, OrderNumber, ResName, emp_name,
        ItemExternalId, EachFinishedQty, StartDate, FinishedDate, 
        b.生产车间,
         CASE 
          WHEN b.OpExternalId IS NULL OR b.OpExternalId NOT LIKE 'op%' 
               THEN b.OpExternalId
          ELSE COALESCE(p.proccess, b.OpExternalId)  -- 防止没匹配到时为空
        END AS 当前工序ID
    FROM APS_FinishedQty_ST a
    LEFT JOIN 派工单_backup b ON a.JobExternalId=b.工单编号
	  LEFT JOIN APS.APS_SUO.dbo.item_proccess p
        ON b.OpExternalId = p.opexternalid
       AND b.OpExternalId LIKE 'op%'

    UNION ALL
    SELECT 
        a.JobExternalId, OrderNumber, ResName, emp_name,
        ItemExternalId, EachFinishedQty, StartDate, FinishedDate, 
        b.生产车间,
          CASE 
          WHEN b.OpExternalId IS NULL OR b.OpExternalId NOT LIKE 'op%' 
               THEN b.OpExternalId
          ELSE COALESCE(p.proccess, b.OpExternalId)  -- 防止没匹配到时为空
        END AS 当前工序ID
    FROM APS_FinishedQty_SX a
    LEFT JOIN 派工单_backup b ON a.JobExternalId=b.工单编号
	  LEFT JOIN APS.APS_SUO.dbo.item_proccess p
        ON b.OpExternalId = p.opexternalid
       AND b.OpExternalId LIKE 'op%'
    UNION ALL
    SELECT 
        a.JobExternalId, OrderNumber, ResName, emp_name,
        ItemExternalId, EachFinishedQty, StartDate, FinishedDate, 
        b.生产车间,
         CASE 
          WHEN b.OpExternalId IS NULL OR b.OpExternalId NOT LIKE 'op%' 
               THEN b.OpExternalId
          ELSE COALESCE(p.proccess, b.OpExternalId)  -- 防止没匹配到时为空
        END AS 当前工序ID
    FROM APS_FinishedQty_SL a
    LEFT JOIN 派工单_backup b ON a.JobExternalId=b.工单编号
	  LEFT JOIN APS.APS_SUO.dbo.item_proccess p
        ON b.OpExternalId = p.opexternalid
       AND b.OpExternalId LIKE 'op%'
) t
LEFT JOIN APS.APS_SUO.dbo.offline_process o
    ON t.当前工序ID = o.before_proccess
	and t.料品编码 like o.item_no +'%'
WHERE t.结束日期 >=getdate()-7




# 2025-10-27
## 万晖五金报销系统的账号密码 
系统管理员-Super-123456
审核人-department-123456
经理-manager-123456
财务管理员-10022-123456
申请人-User-123456

## pnpm run dev

## 2025-10-31数据库的快照
```sql
-- ============================================
-- 1. 用户表
-- ============================================
CREATE TABLE Reimbursement.dbo.[user] (
    id INT IDENTITY(1,1) NOT NULL,
    name NVARCHAR(50) NOT NULL,                    -- 改为NOT NULL
    username NVARCHAR(50) NOT NULL UNIQUE,         -- 添加UNIQUE约束
    password VARCHAR(100) NOT NULL,                -- 改为NOT NULL
    [role] NVARCHAR(20) NOT NULL                   -- 改为NOT NULL
        CHECK ([role] IN ('员工', '经理', '系统管理员', '财务管理员')),  -- 添加CHECK约束
    supervisor_id INT NULL,
    department NVARCHAR(50) NULL,
    workshop NVARCHAR(50) NULL,
    created_at DATETIME NOT NULL DEFAULT GETDATE(), -- 添加DEFAULT
    
    CONSTRAINT PK_user PRIMARY KEY (id),
    CONSTRAINT FK_user_supervisor FOREIGN KEY (supervisor_id) 
        REFERENCES [user](id) ON DELETE NO ACTION  -- 添加外键
);

-- 创建索引
CREATE INDEX IX_user_username ON [user](username);
CREATE INDEX IX_user_supervisor ON [user](supervisor_id);

-- ============================================
-- 2. 报销单主表
-- ============================================
CREATE TABLE Reimbursement.dbo.expense_reports (
    id INT IDENTITY(1,1) NOT NULL,                 -- 添加IDENTITY
    user_id INT NOT NULL,                          -- 改为NOT NULL
    applicant NVARCHAR(50) NOT NULL,               -- 改为NOT NULL
    input_date DATE NOT NULL,                      -- 改为NOT NULL
    total_amount DECIMAL(18,2) NOT NULL,           -- 改为NOT NULL
    
    -- 审核人(经理)审批
    current_approver INT NULL,                     -- 当前审核人ID
    status NVARCHAR(20) NULL                       -- 待审/已批/退回
        CHECK (status IN ('待审', '已批', '退回')),
    reject_reason NVARCHAR(500) NULL,              -- 增加长度
    approver_time DATETIME NULL,                   -- 新增：审核时间
    
    -- 财务审批
    finance_approver INT NULL,                     -- 新增：财务审核人ID
    finance_status NVARCHAR(20) NULL               -- 待审/已批/退回
        CHECK (finance_status IN ('待审', '已批', '退回')),
    finance_reason NVARCHAR(500) NULL,             -- 统一长度
    finance_time DATETIME NULL,
    
    created_at DATETIME NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT PK_expense_reports PRIMARY KEY (id),
    CONSTRAINT FK_reports_user FOREIGN KEY (user_id) 
        REFERENCES [user](id) ON DELETE NO ACTION,
    CONSTRAINT FK_reports_approver FOREIGN KEY (current_approver) 
        REFERENCES [user](id) ON DELETE NO ACTION,
    CONSTRAINT FK_reports_finance FOREIGN KEY (finance_approver) 
        REFERENCES [user](id) ON DELETE NO ACTION
);

-- 创建索引
CREATE INDEX IX_reports_user ON expense_reports(user_id);
CREATE INDEX IX_reports_status ON expense_reports(status, finance_status);
CREATE INDEX IX_reports_approver ON expense_reports(current_approver);
CREATE INDEX IX_reports_date ON expense_reports(input_date);

-- ============================================
-- 3. 报销明细表
-- ============================================
CREATE TABLE Reimbursement.dbo.expense_items (
    id INT IDENTITY(1,1) NOT NULL,
    report_id INT NOT NULL,                        -- 改为NOT NULL
    [date] DATE NOT NULL,                          -- 改为NOT NULL
    category NVARCHAR(100) NULL,                   -- 改为NVARCHAR
    sub_cat NVARCHAR(100) NULL,
    reason NVARCHAR(500) NULL,                     -- 增加长度
    department NVARCHAR(50) NULL,
    workshop NVARCHAR(50) NULL,
    licence NVARCHAR(50) NULL,
    invoice NVARCHAR(100) NULL,
    attachments INT NULL DEFAULT 0,                -- 添加DEFAULT
    amount DECIMAL(18,2) NOT NULL,                 -- 改为NOT NULL
    
    CONSTRAINT PK_expense_items PRIMARY KEY (id),
    CONSTRAINT FK_items_report FOREIGN KEY (report_id) 
        REFERENCES expense_reports(id) ON DELETE CASCADE  -- 级联删除
);

-- 创建索引
CREATE INDEX IX_items_report ON expense_items(report_id);
CREATE INDEX IX_items_date ON expense_items([date]);
CREATE TABLE Reimbursement.dbo.expense_reports (
    id INT IDENTITY(1,1) NOT NULL,
    user_id INT NOT NULL,
    applicant NVARCHAR(50) NOT NULL,              -- 申请人姓名（快照）
    input_date DATE NOT NULL,
    total_amount DECIMAL(18,2) NOT NULL,
    
    -- 审核人信息（提交时快照）
    approver_id INT NULL,                          -- 审核人ID（快照）
    approver_name NVARCHAR(50) NULL,               -- 审核人姓名（快照）
    approver_department NVARCHAR(50) NULL,         -- 审核人部门（快照）
    status NVARCHAR(20) NULL,
    reject_reason NVARCHAR(500) NULL,
    approver_time DATETIME NULL,
    
    -- 财务信息
    finance_id INT NULL,                           -- 财务审核人ID
    finance_name NVARCHAR(50) NULL,                -- 财务审核人姓名（快照）
    finance_status NVARCHAR(20) NULL,
    finance_reason NVARCHAR(500) NULL,
    finance_time DATETIME NULL,
    
    created_at DATETIME NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT PK_expense_reports PRIMARY KEY (id),
    CONSTRAINT FK_reports_user FOREIGN KEY (user_id) 
        REFERENCES [user](id) ON DELETE NO ACTION,
    -- 注意：不对approver_id和finance_id设置外键，允许人员离职后仍保留历史记录
);

```