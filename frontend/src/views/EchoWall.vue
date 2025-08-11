<template>
  <div class="page-container">
    <div class="container">
      <h1 class="page-title">回音壁</h1>
      
      <div class="echo-input-section">
        <div class="echo-input-card">
          <h3>向世界发出你的呼喊</h3>
          <textarea
            v-model="newEcho"
            class="form-control"
            placeholder="写下你此刻的心情..."
            rows="4"
            maxlength="500"
          ></textarea>
          
          <div class="echo-options">
            <select v-model="selectedEmotion" class="form-control emotion-select">
              <option value="">选择情感标签（可选）</option>
              <option v-for="tag in emotionTags" :key="tag.value" :value="tag.value">
                {{ tag.label }}
              </option>
            </select>
            
            <button 
              @click="sendEcho" 
              class="btn btn-primary"
              :disabled="!newEcho.trim() || sending"
            >
              {{ sending ? '发送中...' : '发送呼喊' }}
            </button>
          </div>
        </div>
      </div>
      
      <div class="echo-sections">
        <div class="echo-section">
          <h2 class="section-title">我的呼喊</h2>
          
          <div v-if="myEchoes.length === 0" class="empty-state">
            <div class="empty-state-text">还没有发出呼喊</div>
          </div>
          
          <div v-else class="echo-list">
            <div v-for="echo in myEchoes" :key="echo.id" class="echo-card">
              <p class="echo-content">{{ echo.content }}</p>
              <div class="echo-meta">
                <span v-if="echo.emotion_tag" class="emotion-tag">
                  {{ getEmotionLabel(echo.emotion_tag) }}
                </span>
                <span class="echo-date">{{ formatDate(echo.created_at) }}</span>
                <span v-if="echo.is_matched" class="matched-badge">已匹配</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="echo-section">
          <h2 class="section-title">收到的回音</h2>
          
          <div v-if="myMatches.length === 0" class="empty-state">
            <div class="empty-state-text">还没有收到回音</div>
          </div>
          
          <div v-else class="matches-list">
            <div v-for="match in myMatches" :key="match.id" class="match-card">
              <div class="match-echo">
                <div class="match-label">你的呼喊</div>
                <p class="echo-content">{{ getMyEchoFromMatch(match)?.content }}</p>
              </div>
              <div class="match-arrow">↔️</div>
              <div class="match-echo">
                <div class="match-label">收到的回音</div>
                <p class="echo-content">{{ getMatchedEcho(match)?.content }}</p>
              </div>
              <div class="match-date">
                匹配于 {{ formatDate(match.matched_at) }}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="recent-echoes">
        <h2 class="section-title">最近的回音</h2>
        <div class="recent-echoes-grid">
          <div v-for="echo in recentEchoes" :key="echo.id" class="recent-echo-card">
            <p class="echo-content">{{ echo.content }}</p>
            <div class="echo-meta">
              <span v-if="echo.emotion_tag" class="emotion-tag">
                {{ getEmotionLabel(echo.emotion_tag) }}
              </span>
              <span class="echo-time">{{ formatTime(echo.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useEchoWallStore } from '../stores/echoWall'
import { storeToRefs } from 'pinia'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'

dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

const echoWallStore = useEchoWallStore()
const { myEchoes, myMatches, recentEchoes, emotionTags } = storeToRefs(echoWallStore)

const newEcho = ref('')
const selectedEmotion = ref('')
const sending = ref(false)

onMounted(async () => {
  await Promise.all([
    echoWallStore.fetchEmotionTags(),
    echoWallStore.fetchMyEchoes(),
    echoWallStore.fetchMyMatches(),
    echoWallStore.fetchRecentEchoes()
  ])
})

/**
 * 发送呼喊
 */
const sendEcho = async () => {
  if (!newEcho.value.trim()) return
  
  sending.value = true
  try {
    await echoWallStore.createEcho(newEcho.value.trim(), selectedEmotion.value || undefined)
    newEcho.value = ''
    selectedEmotion.value = ''
    
    // 刷新列表
    await Promise.all([
      echoWallStore.fetchMyEchoes(),
      echoWallStore.fetchRecentEchoes()
    ])
  } catch (error) {
    alert('发送失败，请稍后重试')
  } finally {
    sending.value = false
  }
}

/**
 * 获取情感标签名称
 */
const getEmotionLabel = (tag: string) => {
  return echoWallStore.getEmotionLabel(tag)
}

/**
 * 从匹配中获取我的回音
 */
const getMyEchoFromMatch = (match: any) => {
  return myEchoes.value.find(e => 
    e.id === match.echo_id || e.id === match.matched_echo_id
  )
}

/**
 * 获取匹配的回音
 */
const getMatchedEcho = (match: any) => {
  const myEcho = getMyEchoFromMatch(match)
  if (!myEcho) return null
  
  // 返回另一个回音
  return {
    content: '另一个灵魂的回音...'  // 这里应该从match中获取实际内容
  }
}

/**
 * 格式化日期
 */
const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

/**
 * 格式化时间（相对时间）
 */
const formatTime = (date: string) => {
  return dayjs(date).fromNow()
}
</script>

<style scoped>
.page-container {
  min-height: calc(100vh - 70px);
  padding: 40px 0;
  background: #f8f9fa;
}

.echo-input-section {
  margin-bottom: 40px;
}

.echo-input-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.echo-input-card h3 {
  margin-bottom: 16px;
  color: #333;
}

.echo-options {
  display: flex;
  gap: 16px;
  margin-top: 16px;
}

.emotion-select {
  flex: 1;
  max-width: 200px;
}

.echo-sections {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  margin-bottom: 40px;
}

.echo-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.section-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.echo-list,
.matches-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.echo-card {
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.echo-content {
  color: #333;
  line-height: 1.6;
  margin-bottom: 8px;
}

.echo-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: #999;
}

.emotion-tag {
  padding: 2px 8px;
  background: #e8eaf6;
  color: #5c6bc0;
  border-radius: 12px;
  font-size: 12px;
}

.matched-badge {
  padding: 2px 8px;
  background: #e8f5e9;
  color: #388e3c;
  border-radius: 12px;
  font-size: 12px;
}

.match-card {
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.match-echo {
  padding: 12px;
  background: white;
  border-radius: 8px;
  margin-bottom: 8px;
}

.match-label {
  font-size: 12px;
  color: #999;
  margin-bottom: 4px;
}

.match-arrow {
  text-align: center;
  margin: 8px 0;
  font-size: 20px;
}

.match-date {
  text-align: center;
  font-size: 12px;
  color: #999;
  margin-top: 8px;
}

.recent-echoes {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.recent-echoes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.recent-echo-card {
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  transition: transform 0.3s;
}

.recent-echo-card:hover {
  transform: translateY(-2px);
}

.echo-time {
  font-size: 12px;
  color: #999;
}

@media (max-width: 768px) {
  .echo-sections {
    grid-template-columns: 1fr;
  }
  
  .echo-options {
    flex-direction: column;
  }
  
  .emotion-select {
    max-width: 100%;
  }
}
</style>