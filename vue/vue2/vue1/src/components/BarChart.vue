<template>
    <div ref="chart" style="width: 600px; height: 400px;"></div>
  </template>
  
  <script>
  import * as echarts from 'echarts'
  
  export default {
    name: 'BarChart',
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
  