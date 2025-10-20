```js
//vite.config.js的配置，可以同时用三个不同的后端
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      // FastAPI 的后端
      '/api': {
        target: 'http://127.0.0.1:8001',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      // Go 的后端
      '/goapi': {
        target: 'http://127.0.0.1:8083',
        changeOrigin: true,
        // 如果 Go 后端的路由就是 /api/password，就不改写
        rewrite: (path) => path.replace(/^\/goapi/, '/api'),
      },
      '/nodeapi': {
        target: 'http://127.0.0.1:3001',
        changeOrigin: true,
        // 不改写，直接保持 /nodeapi 前缀
      },
    },
  },
})


```
## vue的监视器的使用
```vue
<!-- vue2 -->
watch: {
  数据名称(新值，旧值){

  }
}
<!-- 也可与写成对象形式 -->
watch:{
  数据名称: {
    handler(newValue, oldValue){

    }
  }
}
<!-- vue3 -->

```
常见的前端事件
| 事件名               | 意思       | 适用场景                                  |
| :---------------- | :------- | :------------------------------------ |
| `@click`          | 点击事件     | 按钮、图片、图标等被点击时                         |
| `@change`         | 值变化事件    | 输入框、下拉框、日期选择器等数据改变时                   |
| `@input`          | 输入事件（实时） | 用户输入每个字符时触发（比 `change` 更频繁）           |
| `@focus`          | 获得焦点     | 用户点击或聚焦到输入框时                          |
| `@blur`           | 失去焦点     | 输入框被点击外部或切换焦点时                        |
| `@keydown`        | 键盘按下     | 监听键盘事件（例如回车）                          |
| `@keyup`          | 键盘抬起     | 输入完成后触发                               |
| `@submit`         | 表单提交     | 用于 `<form>` 提交时                       |
| `@clear`          | 清空事件     | 一些组件（如 `el-date-picker`、`el-input`）提供 |
| `@visible-change` | 弹出状态变化   | 用于下拉框、选择器等，打开/关闭时触发                   |
| `@select`         | 选择事件     | 选中某项时触发（如下拉菜单、日期、表格等）                 |

# 三、Vue 组件的事件和原生事件区别

在 Vue 中你看到的 @事件，有两类来源：

原生 HTML 事件（DOM 自带）
比如：@click、@change、@input、@keydown。

组件自定义事件（由 Element UI、AntD、自己封装的组件触发）
比如：
- el-date-picker 的 @change（选择日期时）

- el-input 的 @clear

- el-select 的 @visible-change

- el-table 的 @selection-change

这些事件不是浏览器原生的，而是组件作者自己定义的。本质上，它们是在 Vue 组件内部通过 $emit('change', value) 来触发的。
