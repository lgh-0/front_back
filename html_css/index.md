HTML 表单元素（input, select 等）都有 value 属性，表示当前输入/选中的值。

在 Vue 中，直接用 v-model 建立双向绑定，就能实时捕捉这个 value。

要把数据传给后端 → 在提交时通过 axios 把 v-model 绑定的值发送过去即可。

前端常见流程：

用户输入（input/select） → v-model 绑定变量更新

点击“提交”按钮 → 用 axios 发请求，把变量值传给后端

后端根据值操作数据库 → 返回结果 → 前端渲染