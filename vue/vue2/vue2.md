npm install -g @vue/cli
vue create myproject

elementui的用法
| 功能   | Element UI 组件名      | Element Plus 组件名    | 用途          |
| ---- | ------------------- | ------------------- | ----------- |
| 表单容器 | `<el-form>`         | `<el-form>`         | 包裹输入项，支持校验  |
| 表单项  | `<el-form-item>`    | `<el-form-item>`    | 包裹每一个输入框等控件 |
| 输入框  | `<el-input>`        | `<el-input>`        | 单行文本输入      |
| 下拉框  | `<el-select>`       | `<el-select>`       | 选择器         |
| 表格   | `<el-table>`        | `<el-table>`        | 展示结构化数据     |
| 表格列  | `<el-table-column>` | `<el-table-column>` | 定义列         |
```html
<template>
  <el-form :model="form">
    <el-form-item label="姓名">
      <el-input v-model="form.name"></el-input>
    </el-form-item>
    <el-form-item label="性别">
      <el-select v-model="form.gender">
        <el-option label="男" value="male" />
        <el-option label="女" value="female" />
      </el-select>
    </el-form-item>
  </el-form>

  <el-table :data="tableData">
    <el-table-column prop="name" label="姓名" />
    <el-table-column prop="age" label="年龄" />
  </el-table>
</template>

```