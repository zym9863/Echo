import { defineStore } from 'pinia'
import api from '../api'

interface User {
  id: string
  email: string
  created_at: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    token: localStorage.getItem('access_token'),
    isAuthenticated: !!localStorage.getItem('access_token')
  }),

  getters: {
    currentUser: (state) => state.user,
    isLoggedIn: (state) => state.isAuthenticated
  },

  actions: {
    /**
     * 用户登录
     */
    async login(email: string, password: string) {
      try {
        const formData = new FormData()
        formData.append('username', email)
        formData.append('password', password)
        
        const response: any = await api.post('/auth/login', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        this.token = response.access_token
        this.user = response.user
        this.isAuthenticated = true
        
        // 保存到localStorage
        localStorage.setItem('access_token', response.access_token)
        localStorage.setItem('user', JSON.stringify(response.user))
        
        return response
      } catch (error) {
        this.logout()
        throw error
      }
    },

    /**
     * 用户注册
     */
    async register(email: string, password: string) {
      try {
        const response: any = await api.post('/auth/register', {
          email,
          password
        })
        
        this.token = response.access_token
        this.user = response.user
        this.isAuthenticated = true
        
        // 保存到localStorage
        localStorage.setItem('access_token', response.access_token)
        localStorage.setItem('user', JSON.stringify(response.user))
        
        return response
      } catch (error) {
        this.logout()
        throw error
      }
    },

    /**
     * 用户登出
     */
    async logout() {
      try {
        await api.post('/auth/logout')
      } catch (error) {
        // 忽略登出错误
      } finally {
        this.user = null
        this.token = null
        this.isAuthenticated = false
        
        localStorage.removeItem('access_token')
        localStorage.removeItem('user')
      }
    },

    /**
     * 获取当前用户信息
     */
    async fetchCurrentUser() {
      try {
        const response: any = await api.get('/auth/me')
        this.user = response
        localStorage.setItem('user', JSON.stringify(response))
        return response
      } catch (error) {
        this.logout()
        throw error
      }
    },

    /**
     * 修改密码
     */
    async changePassword(oldPassword: string, newPassword: string) {
      return await api.post('/auth/change-password', {
        old_password: oldPassword,
        new_password: newPassword
      })
    }
  }
})