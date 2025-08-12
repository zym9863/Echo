import axios from 'axios'
import { API_BASE_URL, NETWORK_CONFIG } from '../config'

// 创建axios实例
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: NETWORK_CONFIG.API_TIMEOUT, // 使用配置文件中的超时设置
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    if (error.response?.status === 401) {
      // token过期或无效，清除token并跳转到登录页
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api