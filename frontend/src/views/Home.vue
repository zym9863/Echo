<template>
  <div class="home-page">
    <!-- 粒子背景 -->
    <div class="particles-bg"></div>
    
    <div class="hero">
      <div class="container">
        <h1 class="hero-title animate-fadeInDown">
          <span class="gradient-text">回响 Echo</span>
        </h1>
        <div class="hero-subtitle animate-fadeIn animation-delay-200">
          <span class="typing-text">时空信箱 · 情感回音壁</span>
        </div>
        <p class="hero-description animate-fadeIn animation-delay-400">
          在这里，将遗憾封存于时光，让期盼穿越时空<br>
          每一声呼喊，都会找到它的回音
        </p>
        
        <div class="hero-actions animate-fadeIn animation-delay-600" v-if="!isLoggedIn">
          <router-link to="/register" class="btn btn-primary btn-lg hover-lift">
            <span>开始旅程</span>
          </router-link>
          <router-link to="/login" class="btn btn-glass btn-lg hover-lift">
            <span>登录</span>
          </router-link>
        </div>
        
        <div class="hero-actions animate-fadeIn animation-delay-600" v-else>
          <router-link to="/time-capsules" class="btn btn-primary btn-lg hover-lift">
            <span>我的时空信箱</span>
          </router-link>
          <router-link to="/echo-wall" class="btn btn-glass btn-lg hover-lift">
            <span>回音壁</span>
          </router-link>
        </div>
      </div>
    </div>
    
    <div class="features">
      <div class="container">
        <div class="grid grid-cols-2">
          <div class="feature-card animate-fadeInLeft" style="animation-delay: 0.8s">
            <div class="feature-icon animate-float">📮</div>
            <h3 class="feature-title">时空信箱</h3>
            <p class="feature-description">
              写下你的遗憾与期盼，设定未来的某个时间点或触发条件，
              让时间成为最好的见证者。当信箱解锁时，
              你会重新遇见那个曾经的自己。
            </p>
            <div class="feature-decoration"></div>
          </div>
          
          <div class="feature-card animate-fadeInRight" style="animation-delay: 1s">
            <div class="feature-icon animate-float" style="animation-delay: 0.5s">🌊</div>
            <h3 class="feature-title">情感回音壁</h3>
            <p class="feature-description">
              向世界发出你的呼喊，系统会为你找到情感共鸣的回音。
              这不是即时聊天，而是跨越时空的心灵连接，
              让每一份孤独都能找到温暖的回应。
            </p>
            <div class="feature-decoration"></div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="public-gallery" v-if="publicCapsules.length > 0">
      <div class="container">
        <h2 class="section-title animate-fadeIn">公共回音廊</h2>
        <div class="grid grid-cols-3">
          <div 
            v-for="(capsule, index) in publicCapsules.slice(0, 6)" 
            :key="capsule.id" 
            class="capsule-card hover-lift animate-scaleIn"
            :style="`animation-delay: ${1.2 + index * 0.1}s`"
          >
            <div class="capsule-card-inner">
              <h4 class="capsule-title">{{ capsule.title }}</h4>
              <p class="capsule-content">{{ truncateText(capsule.content, 100) }}</p>
              <div class="capsule-meta">
                <span class="capsule-date">
                  <i class="icon-calendar"></i>
                  {{ formatDate(capsule.created_at) }}
                </span>
              </div>
              <div class="capsule-overlay">
                <router-link :to="`/time-capsules/${capsule.id}`" class="btn btn-glass btn-sm">
                  查看详情
                </router-link>
              </div>
            </div>
          </div>
        </div>
        <div class="text-center animate-fadeIn" style="animation-delay: 2s">
          <router-link to="/echo-gallery" class="btn btn-secondary btn-lg hover-grow">
            查看更多
          </router-link>
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
@import '../styles/animations.css';
@import '../styles/variables.css';

.home-page {
  min-height: 100vh;
  background: var(--primary-gradient);
  position: relative;
  overflow: hidden;
}

/* 粒子背景 */
.particles-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 0;
}

.particles-bg::before {
  content: '';
  position: absolute;
  width: 200%;
  height: 200%;
  top: -50%;
  left: -50%;
  background-image: 
    radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px),
    radial-gradient(circle, rgba(255,255,255,0.05) 1px, transparent 1px);
  background-size: 50px 50px, 100px 100px;
  animation: float 20s linear infinite;
}

.hero {
  padding: 120px 0;
  text-align: center;
  color: white;
  position: relative;
  z-index: 1;
}

.hero-title {
  font-size: 72px;
  font-weight: 900;
  margin-bottom: 20px;
  letter-spacing: -2px;
}

.hero-title .gradient-text {
  background: linear-gradient(
    90deg,
    #ffffff 0%,
    #f0f0f0 25%,
    #ffffff 50%,
    #f0f0f0 75%,
    #ffffff 100%
  );
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradientShift 3s linear infinite;
}

/* 打字机效果 */
.hero-subtitle {
  font-size: 28px;
  margin-bottom: 30px;
  opacity: 0.95;
  position: relative;
  display: inline-block;
}

.typing-text {
  position: relative;
  font-family: monospace;
}

.typing-text::after {
  content: '|';
  position: absolute;
  right: -10px;
  animation: cursorBlink 1s infinite;
}

.hero-description {
  font-size: 20px;
  line-height: 1.8;
  margin-bottom: 60px;
  opacity: 0.9;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.hero-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-lg {
  padding: 18px 40px;
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.features {
  background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(248,249,250,0.95) 100%);
  backdrop-filter: blur(10px);
  padding: 100px 0;
  position: relative;
  z-index: 1;
}

.feature-card {
  text-align: center;
  padding: 50px 40px;
  background: white;
  border-radius: var(--border-radius-xl);
  box-shadow: var(--shadow-xl);
  position: relative;
  overflow: hidden;
  transition: all var(--transition-normal);
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--primary-gradient);
  transform: scaleX(0);
  transition: transform var(--transition-normal);
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.15);
}

.feature-card:hover::before {
  transform: scaleX(1);
}

.feature-icon {
  font-size: 72px;
  margin-bottom: 30px;
  filter: drop-shadow(0 10px 20px rgba(0,0,0,0.1));
}

.feature-title {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 20px;
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.feature-description {
  font-size: 18px;
  line-height: 1.8;
  color: var(--text-secondary);
}

.feature-decoration {
  position: absolute;
  bottom: -50px;
  right: -50px;
  width: 150px;
  height: 150px;
  background: var(--primary-gradient);
  opacity: 0.05;
  border-radius: 50%;
  transition: all var(--transition-normal);
}

.feature-card:hover .feature-decoration {
  transform: scale(1.5);
  opacity: 0.1;
}

.public-gallery {
  background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
  padding: 100px 0;
  position: relative;
  z-index: 1;
}

.section-title {
  font-size: 42px;
  font-weight: 900;
  text-align: center;
  margin-bottom: 60px;
  position: relative;
  display: inline-block;
  width: 100%;
}

.capsule-card {
  background: white;
  padding: 0;
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  transition: all var(--transition-normal);
  position: relative;
}

.capsule-card-inner {
  padding: 30px;
}

.capsule-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.capsule-title {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 15px;
  color: var(--text-primary);
}

.capsule-content {
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-secondary);
  margin-bottom: 20px;
}

.capsule-meta {
  font-size: 14px;
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  gap: 8px;
}

.capsule-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(124, 58, 237, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity var(--transition-normal);
}

.capsule-card:hover .capsule-overlay {
  opacity: 1;
}

.text-center {
  text-align: center;
  margin-top: 60px;
}

/* 响应式 */
@media (max-width: 768px) {
  .hero-title {
    font-size: 48px;
  }
  
  .hero-subtitle {
    font-size: 22px;
  }
  
  .hero-description {
    font-size: 18px;
    padding: 0 20px;
  }
  
  .hero-actions {
    flex-direction: column;
    align-items: center;
    padding: 0 20px;
  }
  
  .btn-lg {
    width: 100%;
    max-width: 300px;
  }
  
  .grid-cols-2,
  .grid-cols-3 {
    grid-template-columns: 1fr;
  }
  
  .feature-card {
    margin-bottom: 20px;
  }
}
</style>