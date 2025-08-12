<template>
  <div class="home-page">
    <div class="hero">
      <div class="container">
        <h1 class="hero-title">回响 Echo</h1>
        <p class="hero-subtitle">时空信箱 · 情感回音壁</p>
        <p class="hero-description">
          在这里，将遗憾封存于时光，让期盼穿越时空<br>
          每一声呼喊，都会找到它的回音
        </p>
        
        <div class="hero-actions" v-if="!isLoggedIn">
          <router-link to="/register" class="btn btn-primary">开始旅程</router-link>
          <router-link to="/login" class="btn btn-secondary">登录</router-link>
        </div>
        
        <div class="hero-actions" v-else>
          <router-link to="/time-capsules" class="btn btn-primary">我的时空信箱</router-link>
          <router-link to="/echo-wall" class="btn btn-secondary">回音壁</router-link>
        </div>
      </div>
    </div>
    
    <div class="features">
      <div class="container">
        <div class="grid grid-cols-2">
          <div class="feature-card">
            <div class="feature-icon">📮</div>
            <h3 class="feature-title">时空信箱</h3>
            <p class="feature-description">
              写下你的遗憾与期盼，设定未来的某个时间点或触发条件，
              让时间成为最好的见证者。当信箱解锁时，
              你会重新遇见那个曾经的自己。
            </p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">🌊</div>
            <h3 class="feature-title">情感回音壁</h3>
            <p class="feature-description">
              向世界发出你的呼喊，系统会为你找到情感共鸣的回音。
              这不是即时聊天，而是跨越时空的心灵连接，
              让每一份孤独都能找到温暖的回应。
            </p>
          </div>
        </div>
      </div>
    </div>
    
    <div class="public-gallery" v-if="publicCapsules.length > 0">
      <div class="container">
        <h2 class="section-title">公共回音廊</h2>
        <div class="grid grid-cols-3">
          <div v-for="capsule in publicCapsules.slice(0, 6)" :key="capsule.id" class="capsule-card">
            <h4 class="capsule-title">{{ capsule.title }}</h4>
            <p class="capsule-content">{{ truncateText(capsule.content, 100) }}</p>
            <div class="capsule-meta">
              <span class="capsule-date">{{ formatDate(capsule.created_at) }}</span>
            </div>
          </div>
        </div>
        <div class="text-center">
          <router-link to="/echo-gallery" class="btn btn-secondary">查看更多</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useTimeCapsuleStore } from '../stores/timeCapsule'
import { storeToRefs } from 'pinia'
import dayjs from 'dayjs'

const authStore = useAuthStore()
const timeCapsuleStore = useTimeCapsuleStore()
const { isLoggedIn } = storeToRefs(authStore)
const { publicCapsules } = storeToRefs(timeCapsuleStore)

onMounted(async () => {
  // 获取公开的时空信箱
  try {
    await timeCapsuleStore.fetchPublicCapsules()
  } catch (error) {
    console.error('Failed to fetch public capsules:', error)
  }
})

/**
 * 截断文本
 */
const truncateText = (text: string, maxLength: number) => {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

/**
 * 格式化日期
 */
const formatDate = (date: string) => {
  return dayjs(date).format('YYYY年MM月DD日')
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.hero {
  padding: 100px 0;
  text-align: center;
  color: white;
}

.hero-title {
  font-size: 64px;
  font-weight: bold;
  margin-bottom: 16px;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.hero-subtitle {
  font-size: 24px;
  margin-bottom: 24px;
  opacity: 0.9;
}

.hero-description {
  font-size: 18px;
  line-height: 1.8;
  margin-bottom: 48px;
  opacity: 0.85;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.hero-actions .btn {
  padding: 16px 32px;
  font-size: 18px;
}

.hero-actions .btn-secondary {
  background: white;
  color: #667eea;
}

.features {
  background: white;
  padding: 80px 0;
}

.feature-card {
  text-align: center;
  padding: 40px;
}

.feature-icon {
  font-size: 64px;
  margin-bottom: 24px;
}

.feature-title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 16px;
  color: #333;
}

.feature-description {
  font-size: 16px;
  line-height: 1.8;
  color: #666;
}

.public-gallery {
  background: #f8f9fa;
  padding: 80px 0;
}

.section-title {
  font-size: 36px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 48px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.capsule-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.capsule-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.capsule-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 12px;
  color: #333;
}

.capsule-content {
  font-size: 14px;
  line-height: 1.6;
  color: #666;
  margin-bottom: 16px;
}

.capsule-meta {
  font-size: 12px;
  color: #999;
}

.text-center {
  text-align: center;
  margin-top: 48px;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 48px;
  }
  
  .hero-subtitle {
    font-size: 20px;
  }
  
  .hero-description {
    font-size: 16px;
  }
  
  .hero-actions {
    flex-direction: column;
    align-items: center;
  }
}
</style>