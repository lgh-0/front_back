<template>
  <div>
    <div ref="chart" style="width: 600px; height: 400px;"></div>
    <hr>
    <el-table
    :data="tableData"
    border
    stripe
    style="width: 100%">
    <el-table-column
      prop="date"
      label="日期"
      width="180">
    </el-table-column>
    <el-table-column
      prop="name"
      label="姓名"
      width="180">
    </el-table-column>
    <el-table-column
      prop="address"
      label="地址">
    </el-table-column>
  </el-table>
  <hr>
  <P>这是分割线</P>
  </div>
  </template>
  
  <script>
  import * as echarts from 'echarts'
  
  export default {
    name: 'BarChart',
    data(){
      return {
        tableData: [{
          date: '2016-05-02',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          date: '2016-05-04',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1517 弄'
        }, {
          date: '2016-05-01',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1519 弄'
        }, {
          date: '2016-05-03',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1516 弄'
        }]
      }
    },
    mounted() {
      // 1️⃣ 获取容器
      const chartDom = this.$refs.chart
      // 2️⃣ 初始化 ECharts 实例
      const myChart = echarts.init(chartDom)
      // 3️⃣ 配置图表
      const option = {
        title: {
          text: '销售统计',
        },
        tooltip: {},
        xAxis: {
          data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子'],
        },
        yAxis: {},
        series: [
          {
            name: '销量',
            type: 'bar', // 柱状图
            data: [5, 20, 36, 10, 10, 20],
          },
        ],
      }
      // 4️⃣ 渲染图表
      myChart.setOption(option)
      // 5️⃣ 自适应窗口大小
      window.addEventListener('resize', () => {
        myChart.resize()
      })
    },
  }
  </script>
  