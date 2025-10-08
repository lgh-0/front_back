<!-- 2025-10-7新增历史离职员工查询 -->
<!-- 带有某页能选择多少条数量的组件 -->
<template>
    <Layout :breadcrumbItems="breadcrumbItems">
      <div class="resigned-people-container">
        <!-- 查询表单 -->
        <el-card class="search-card">
          <el-form :model="searchForm" inline>
            <el-form-item label="部门">
              <el-input v-model="searchForm.部门" placeholder="请输入部门名称" clearable style="width: 200px" />
            </el-form-item>
            
            <el-form-item label="入职时间">
              <el-date-picker
                v-model="searchForm.入职时间"
                type="daterange"
                range-separator="-"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                value-format="yyyy-MM-dd"
                style="width: 300px"
              />
            </el-form-item>
            
            <el-form-item label="离职时间">
              <el-date-picker
                v-model="searchForm.离职时间"
                type="daterange"
                range-separator="-"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                value-format="yyyy-MM-dd"
                style="width: 300px"
              />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="handleSearch" :loading="loading">查询</el-button>
              <el-button @click="handleReset">重置</el-button>
              <el-button type="success" @click="handleExport">导出Excel</el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <!-- 数据表格 -->
        <el-card class="table-card">
          <div class="table-header">
            <div class="header-left">
              <span class="title">离职员工列表</span>
            </div>
            <div class="header-right">
              <span class="stat-item">总数据条数：<strong>{{ totalCount }}</strong></span>
              <span class="stat-item">符合条件：<strong>{{ tableData.length }}</strong> 条</span>
              <span class="stat-item">当前页：<strong>{{ currentPage }}</strong> / {{ totalPages }}</span>
            </div>
          </div>
          
          <el-table
            :data="paginatedData"
            v-loading="loading"
            border
            stripe
            style="width: 100%"
            max-height="600"
            :header-cell-style="{ background: '#409EFF', color: '#fff', fontWeight: 'bold' }"
          >
            <el-table-column type="index" label="序号" width="60" align="center" :index="indexMethod" />
            <el-table-column prop="姓名" label="姓名" width="100" align="center" />
            <el-table-column prop="性别" label="性别" width="60" align="center" />
            <el-table-column prop="年龄" label="年龄" width="60" align="center" />
            <el-table-column prop="学历" label="学历" width="80" align="center" />
            <el-table-column prop="工号" label="工号" width="120" align="center" />
            <el-table-column prop="部门" label="部门" width="150" align="center" />
            <el-table-column prop="车间" label="车间" width="120" align="center" />
            <el-table-column prop="分区" label="分区" width="100" align="center" />
            <el-table-column prop="工位" label="工位" width="100" align="center" />
            <el-table-column prop="线别" label="线别" width="100" align="center" />
            <el-table-column prop="所属技工" label="所属技工" width="120" align="center" />
            <el-table-column prop="所属上级" label="所属上级" width="120" align="center" />
            <el-table-column prop="联系方式" label="联系方式" width="130" align="center" />
            <el-table-column prop="居住地址" label="居住地址" width="200" show-overflow-tooltip />
            <el-table-column prop="电子邮箱" label="电子邮箱" width="180" show-overflow-tooltip />
            <el-table-column prop="在职状态" label="在职状态" width="100" align="center" />
            <el-table-column prop="入职时间" label="入职时间" width="120" align="center" />
            <el-table-column prop="离职时间" label="离职时间" width="120" align="center" />
          </el-table>
          
          <!-- 分页组件 -->
          <div class="pagination-container">
            <el-pagination
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :current-page="currentPage"
              :page-sizes="[10, 20, 30, 50, 100]"
              :page-size="pageSize"
              layout="total, sizes, prev, pager, next, jumper"
              :total="tableData.length"
              background
            />
          </div>
        </el-card>
      </div>
    </Layout>
</template>

<script>
import axios from 'axios'
import Layout from '@/components/Layout.vue'
import { eventBus } from '../../eventBus'

export default {
    name: 'resignedPeople',
    components: {
        Layout
    },
    data() {
        return {
            breadcrumbItems: ['HR人力资源资讯', '历史离职员工信息查询'],
            searchForm: {
                部门: '',
                入职时间: [],
                离职时间: []
            },
            tableData: [],
            totalCount: 0, // 总数据条数
            loading: false,
            currentPage: 1, // 当前页码
            pageSize: 30 // 每页显示条数
        }
    },
    computed: {
        // 分页后的数据
        paginatedData() {
            const start = (this.currentPage - 1) * this.pageSize
            const end = start + this.pageSize
            return this.tableData.slice(start, end)
        },
        // 总页数
        totalPages() {
            return Math.ceil(this.tableData.length / this.pageSize)
        }
    },
    mounted() {
        this.handleSearch()
    },
    methods: {
        async handleSearch() {
            this.loading = true
            try {
                const params = {}
                
                // 部门
                if (this.searchForm.部门) {
                    params.部门 = this.searchForm.部门
                }
                
                // 入职时间
                if (this.searchForm.入职时间 && this.searchForm.入职时间.length === 2) {
                    params.入职时间开始 = this.searchForm.入职时间[0]
                    params.入职时间结束 = this.searchForm.入职时间[1]
                }
                
                // 离职时间
                if (this.searchForm.离职时间 && this.searchForm.离职时间.length === 2) {
                    params.离职时间开始 = this.searchForm.离职时间[0]
                    params.离职时间结束 = this.searchForm.离职时间[1]
                }
                
                const res = await axios.get('/api/resigned-people', { params })
                
                if (res.data.status === 'success') {
                    this.tableData = res.data.data
                    this.totalCount = res.data.count // 保存总数据条数
                    this.currentPage = 1 // 重置到第一页
                    this.$message.success(`查询成功，共 ${res.data.count} 条记录`)
                } else {
                    this.$message.error('查询失败')
                }
            } catch (error) {
                console.error('查询失败:', error)
                this.$message.error('查询失败，请检查网络')
            } finally {
                this.loading = false
            }
        },
        
        handleReset() {
            this.searchForm = {
                部门: '',
                入职时间: [],
                离职时间: []
            }
            this.handleSearch()
        },
        
        handleExport() {
            if (this.tableData.length === 0) {
                this.$message.warning('暂无数据可导出')
                return
            }
            
            // 导出Excel功能（需要安装 xlsx 库）
            import('xlsx').then(XLSX => {
                const worksheet = XLSX.utils.json_to_sheet(this.tableData)
                const workbook = XLSX.utils.book_new()
                XLSX.utils.book_append_sheet(workbook, worksheet, '离职员工')
                XLSX.writeFile(workbook, `离职员工信息_${new Date().toLocaleDateString()}.xlsx`)
                this.$message.success('导出成功')
            }).catch(() => {
                this.$message.error('导出失败，请安装 xlsx 库')
            })
        },
        
        // 分页：每页显示条数改变
        handleSizeChange(val) {
            this.pageSize = val
            this.currentPage = 1
        },
        
        // 分页：当前页改变
        handleCurrentChange(val) {
            this.currentPage = val
        },
        
        // 序号计算方法
        indexMethod(index) {
            return (this.currentPage - 1) * this.pageSize + index + 1
        }
    }
}
</script>

<style scoped>
.resigned-people-container {
  padding: 20px;
}

.search-card {
  margin-bottom: 20px;
}

.table-card {
  margin-top: 20px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 12px 16px;
  background: #f5f7fa;
  border-radius: 4px;
}

.header-left .title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.header-right {
  display: flex;
  gap: 20px;
}

.stat-item {
  font-size: 14px;
  color: #606266;
}

.stat-item strong {
  color: #409EFF;
  font-size: 16px;
  margin: 0 4px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>