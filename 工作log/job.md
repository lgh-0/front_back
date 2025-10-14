192.168.41.57
sa  
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





