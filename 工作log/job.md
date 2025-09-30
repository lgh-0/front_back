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





