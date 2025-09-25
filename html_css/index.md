HTML 表单元素（input, select 等）都有 value 属性，表示当前输入/选中的值。

在 Vue 中，直接用 v-model 建立双向绑定，就能实时捕捉这个 value。

要把数据传给后端 → 在提交时通过 axios 把 v-model 绑定的值发送过去即可。

前端常见流程：

用户输入（input/select） → v-model 绑定变量更新

点击“提交”按钮 → 用 axios 发请求，把变量值传给后端

后端根据值操作数据库 → 返回结果 → 前端渲染

# 2.块级元素
块级子元素如果没指定宽度，默认会填满父元素的宽度；但高度不会自动继承父的高度，而是由内容决定。

父元素如果没写高度，就会被子元素的内容高度撑开；父的宽度一般不被子撑开，除非父是 inline-block 或者宽度未受限。


```html
背景颜色常用的是beige 然后red green这样不会遮挡看不清


justify-content: space-between; 👉 控制 主轴（这里是水平方向），但是：

当只有一个子元素时，space-between 会把它放在起始位置，并且没有东西可以“分布”，所以不会居中。
<style scoped>
    
.div2 { 控制子元素
  display: flex;
  justify-content: center;  /* 主轴(水平方向) 居中 */
  align-items: center;      /* 交叉轴(垂直方向) 居中 */
}
/* flex容器内的属性的常用值
flex（弹性盒子布局）就是用来解决块级元素在一行排列、水平或垂直对齐、子元素空间分配这些问题的。
justify-content: space-between; → 三个子元素两端对齐，中间自动分散

justify-content: center; → 三个子元素整体在中间挤在一起

justify-content: space-around; → 每个子元素左右有均等空隙

justify-content: space-evenly; → 子元素和边界之间的空隙完全一致

你这种「让块元素在一行排列」就是 flex 的常见用法之一

子元素样式一般写 flex: 1（自动分配），或者 flex-grow / flex-shrink / flex-basis 来控制伸缩

你想控制谁大谁小 → 调整 flex 值；想控制对齐方式 → 用 justify-content 和 align-items

一行排多个块：导航栏、按钮组、卡片布局

居中对齐：justify-content: center; align-items: center; → 水平 + 垂直居中

等比分配空间：响应式布局（子元素宽度自适应）

换行布局：图文列表，自动换行
*/
<style>
```
# 二、elementUI
✅ 第一种：el-table
```html
<el-table :data="tableData">
  <!-- 固定的序号列 -->
  <el-table-column type="index" label="序号" />
  
  <!-- 动态渲染的其他列 -->
  <el-table-column v-for="col in columns" :prop="col.prop" :label="col.label" />
</el-table>
```
特点

核心用途：表格展示型数据（数据库查询结果、列表、报表等）。

优势：

内置分页、排序、筛选、斑马纹、固定列、合并单元格等丰富功能。

列定义清晰，配合 v-for 可以动态渲染列配置。

天然适合后端接口返回的 二维表结构数据（数组对象）。

使用场景

显示查询结果（比如你的“派工单查询”）。

展示订单列表、用户表、库存表等典型表格。

✅ 第二种：el-form + el-row + el-col
```html
<el-form>
  <el-row>
    <el-col :span="8">
      <el-form-item label="订单批号">
        <el-input v-model="form.orderBatch" />
      </el-form-item>
    </el-col>
    <el-col :span="8">
      <el-form-item label="料品编码">
        <el-input v-model="form.partCode" />
      </el-form-item>
    </el-col>
  </el-row>
</el-form>
```
特点

核心用途：表单布局（数据输入、参数筛选、配置项编辑）。

优势：

基于栅格系统（el-row/el-col），可以很灵活地实现响应式布局。

和 el-form-item 结合，方便做 表单校验。

更适合做“数据录入”而不是“数据展示”。

使用场景

搜索条件表单（比如上面你的 filters 就可以用它渲染）。

用户注册、信息编辑、配置页面。

📊 总结对比
功能	el-table	el-form + el-row/el-col
主要作用	展示数据	输入/编辑数据
渲染方式	表格化，每一行表示一条记录	栅格布局，每一行表示一组字段
内置功能	排序、分页、合并单元格、固定列	表单校验、输入控件绑定
适用场景	数据报表、查询结果	筛选条件、配置界面、注册表单

👉 所以你看到的“派工单查询”其实是 el-form（上方搜索区）+ el-table（下方结果区） 的组合，这是一个常见模式：

上面用表单做查询条件

下面用表格展示查询结果


