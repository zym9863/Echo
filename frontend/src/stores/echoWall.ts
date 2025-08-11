import { defineStore } from 'pinia'
import api from '../api'

interface EchoWall {
  id: string
  user_id: string
  content: string
  emotion_tag: string | null
  is_matched: boolean
  created_at: string
}

interface EchoMatch {
  id: string
  echo_id: string
  matched_echo_id: string
  matched_at: string
  echo?: EchoWall
  matched_echo?: EchoWall
}

interface EchoWallState {
  myEchoes: EchoWall[]
  myMatches: EchoMatch[]
  recentEchoes: EchoWall[]
  emotionTags: Array<{
    value: string
    label: string
    type: string
  }>
  loading: boolean
  error: string | null
}

export const useEchoWallStore = defineStore('echoWall', {
  state: (): EchoWallState => ({
    myEchoes: [],
    myMatches: [],
    recentEchoes: [],
    emotionTags: [],
    loading: false,
    error: null
  }),

  getters: {
    matchedEchoes: (state) => state.myEchoes.filter(e => e.is_matched),
    unmatchedEchoes: (state) => state.myEchoes.filter(e => !e.is_matched),
    matchCount: (state) => state.myMatches.length
  },

  actions: {
    /**
     * 发送呼喊到回音壁
     */
    async createEcho(content: string, emotion_tag?: string) {
      this.loading = true
      this.error = null
      try {
        const response: any = await api.post('/echo-wall/', {
          content,
          emotion_tag
        })
        this.myEchoes.unshift(response)
        return response
      } catch (error: any) {
        this.error = error.response?.data?.detail || '发送失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * 获取我的呼喊列表
     */
    async fetchMyEchoes() {
      this.loading = true
      this.error = null
      try {
        const response: any = await api.get('/echo-wall/my-echoes')
        this.myEchoes = response
        return response
      } catch (error: any) {
        this.error = error.response?.data?.detail || '获取失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * 获取我的匹配列表
     */
    async fetchMyMatches() {
      this.loading = true
      this.error = null
      try {
        const response: any = await api.get('/echo-wall/my-matches')
        this.myMatches = response
        return response
      } catch (error: any) {
        this.error = error.response?.data?.detail || '获取失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * 获取最近的回音
     */
    async fetchRecentEchoes(limit: number = 20) {
      this.loading = true
      this.error = null
      try {
        const response: any = await api.get('/echo-wall/recent', {
          params: { limit }
        })
        this.recentEchoes = response
        return response
      } catch (error: any) {
        this.error = error.response?.data?.detail || '获取失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * 获取情感标签列表
     */
    async fetchEmotionTags() {
      try {
        const response: any = await api.get('/echo-wall/emotions')
        this.emotionTags = response
        return response
      } catch (error: any) {
        this.error = error.response?.data?.detail || '获取失败'
        throw error
      }
    },

    /**
     * 手动创建匹配（测试用）
     */
    async createManualMatch(echo_id: string, matched_echo_id: string) {
      this.loading = true
      this.error = null
      try {
        const response: any = await api.post('/echo-wall/manual-match', {
          echo_id,
          matched_echo_id
        })
        await this.fetchMyMatches()
        return response
      } catch (error: any) {
        this.error = error.response?.data?.detail || '匹配失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * 根据情感标签获取标签名称
     */
    getEmotionLabel(tag: string): string {
      const emotion = this.emotionTags.find(e => e.value === tag)
      return emotion?.label || tag
    },

    /**
     * 根据情感标签获取标签类型
     */
    getEmotionType(tag: string): string {
      const emotion = this.emotionTags.find(e => e.value === tag)
      return emotion?.type || 'default'
    }
  }
})