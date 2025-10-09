// import Vue from 'vue'
// import App from './App.vue'

// Vue.config.productionTip = false

// new Vue({
//   render: h => h(App),
// }).$mount('#app')
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css' // 样式文件一定要引入

import App from './App.vue'

Vue.use(ElementUI)

new Vue({
  render: h => h(App),
}).$mount('#app')
