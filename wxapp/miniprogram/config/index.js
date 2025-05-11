// 环境配置
const env = {
  development: {
    baseUrl: 'http://localhost:8080/api'
  },
  production: {
    baseUrl: 'https://api.yourdomain.com' // 生产环境URL
  }
}

// 当前环境
const currentEnv = 'development'

// 导出配置
export default {
  baseUrl: env[currentEnv].baseUrl
} 