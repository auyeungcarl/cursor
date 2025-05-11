import App from './App'
import Vue from 'vue'
import './uni.promisify.adaptor'
import request from './utils/request'

Vue.config.productionTip = false

// 注册HTTP请求工具
Vue.prototype.$http = request

App.mpType = 'app'

const app = new Vue({
  ...App
})
app.$mount()

// #ifdef VUE3
import { createSSRApp } from 'vue'
export function createApp() {
  const app = createSSRApp(App)
  return {
    app
  }
}
// #endif