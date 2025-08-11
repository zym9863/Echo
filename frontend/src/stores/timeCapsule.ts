import { defineStore } from 'pinia'
import api from '../api'
import dayjs from 'dayjs'

interface TimeCapsule {
  id: string
  user_id: string
  title: string
  content: string
  unlock_date: string | null
  unlock_condition: string | null
  status: 'locked' | 'unlocked' | 'public'
  is_public: boolean
  created_at: string
  updated_at: string
}

interface TimeCapsuleState {
  capsules: TimeCapsule[]
  publicCapsules: TimeCapsule[]
  loading: boolean
  error: string | null
}

export const useTimeCapsuleStore = defineStore('timeCapsule', {
  state: (): TimeCapsuleState => ({
    capsules: [],
    publicCapsules: [],
    loading: false,
    error: null
  }),

  getters: {
    lockedCapsules: (state) => state.capsules.filter(c => c.status === 'locked'),
    unlockedCapsules: (state) => state.capsules.filter(c => c.status === 'unlocked'),
    myCapsuleCount: (state) => state.capsules.length
  },

  actions: {
    /**
     * 创建时空信箱
     */
    async createCapsule(data: {
      title: string
      content: string
      unlock_date?: string
      unlock_condition?: string
      is_public?: boolean
    }) {
      this.loading = true
      this.error = null
      try {
        const response: any = await api.post('/time-capsules/', data)
        this.capsules.unshift(response)
        return response
      } catch (error: any) {
        this.error = error.response?.data?.detail || '创建失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * 获取我的时空信箱列表
     */
    async fetchMyCapsules(status?: string) {
      this.loading = true
      this.error = null
      try {
        const params = status ? { status } : {}
        const response: any = await api.get('/time-capsules/', { params })
        this.capsules = response
        return response
      } catch (error: any) {
        this.error = error.response?.data?.detail || '获取失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * 获取公开的时空信箱
     */
    async fetchPublicCapsules() {
      this.loading = true
      this.error = null
      try {
        const response: any = await api.get('/time-capsules/public')
        this.publicCapsules = response
        return response
      } catch (error: any) {
        this.error = error.response?.data?.detail || '获取失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * 获取单个时空信箱
     */
    async fetchCapsule(id: string) {
      this.loading = true
      this.error = null
      try {
        const response: any = await api.get(`/time-capsules/${id}`)
        return response
      } catch (error: any) {
        this.error = error.response?.data?.detail || '获取失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * 更新时空信箱
     */
    async updateCapsule(id: string, data: Partial<TimeCapsule>) {
      this.loading = true
      this.error = null
      try {
        const response: any = await api.put(`/time-capsules/${id}`, data)
        const index = this.capsules.findIndex(c => c.id === id)
        if (index !== -1) {
          this.capsules[index] = response
        }
        return response
      } catch (error: any) {
        this.error = error.response?.data?.detail || '更新失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * 解锁时空信箱
     */
    async unlockCapsule(id: string) {
      this.loading = true
      this.error = null
      try {
        const response: any = await api.post(`/time-capsules/${id}/unlock`)
        if (response.success) {
          const index = this.capsules.findIndex(c => c.id === id)
          if (index !== -1) {
            this.capsules[index].status = 'unlocked'
          }
        }
        return response
      } catch (error: any) {
        this.error = error.response?.data?.detail || '解锁失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * 发布到公共回音廊
     */
    async publishCapsule(id: string) {
      this.loading = true
      this.error = null
      try {
        const response: any = await api.post(`/time-capsules/${id}/publish`)
        if (response.success) {
          const index = this.capsules.findIndex(c => c.id === id)
          if (index !== -1) {
            this.capsules[index].status = 'public'
            this.capsules[index].is_public = true
          }
        }
        return response
      } catch (error: any) {
        this.error = error.response?.data?.detail || '发布失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * 删除时空信箱
     */
    async deleteCapsule(id: string) {
      this.loading = true
      this.error = null
      try {
        const response: any = await api.delete(`/time-capsules/${id}`)
        this.capsules = this.capsules.filter(c => c.id !== id)
        return response
      } catch (error: any) {
        this.error = error.response?.data?.detail || '删除失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * 检查是否可以解锁
     */
    canUnlock(capsule: TimeCapsule): boolean {
      if (capsule.status !== 'locked') return false
      if (capsule.unlock_date) {
        return dayjs().isAfter(dayjs(capsule.unlock_date))
      }
      return false
    }
  }
})