<template>
  <div class="page-container">
    <div class="container">
      <div class="page-header animate-fadeInDown">
        <h1 class="page-title gradient-text">我的时空信箱</h1>
        <router-link to="/time-capsules/create" class="btn btn-primary hover-lift">
          <span class="btn-icon">+</span>
          创建新信箱
        </router-link>
      </div>
      
      <!-- 骨架屏加载 -->
      <div v-if="loading" class="capsules-grid">
        <div v-for="i in 6" :key="i" class="skeleton skeleton-card"></div>
      </div>
      
      <div v-else-if="capsules.length === 0" class="empty-state animate-fadeIn">
        <div class="empty-state-icon animate-float">📮</div>
        <div class="empty-state-text">还没有时空信箱</div>
        <router-link to="/time-capsules/create" class="btn btn-primary hover-lift">
          创建第一个时空信箱
        </router-link>
      </div>
      
      <!-- 时间轴布局 -->
      <div v-else class="timeline-container">
        <div class="timeline-line"></div>
        <div 
          v-for="(capsule, index) in capsules" 
          :key="capsule.id" 
          :class="['timeline-item', index % 2 === 0 ? 'left' : 'right', 'animate-fadeIn']"
          :style="`animation-delay: ${index * 0.1}s`"
        >
          <div class="timeline-dot"></div>
          <div class="capsule-card hover-lift">
            <div class="capsule-header">
              <h3 class="capsule-title">{{ capsule.title }}</h3>
              <span :class="['capsule-status', `status-${capsule.status}`]">
                <span class="status-dot"></span>
                {{ getStatusText(capsule.status) }}
              </span>
            </div>
            
            <p class="capsule-content">{{ truncateText(capsule.content, 100) }}</p>
            
            <div class="capsule-meta">
              <span v-if="capsule.unlock_date" class="meta-item">
                <span class="meta-icon">🔓</span>
                {{ formatUnlockDate(capsule.unlock_date) }}
              </span>
              <span v-if="capsule.unlock_condition" class="meta-item">
                <span class="meta-icon">📝</span>
                {{ capsule.unlock_condition }}
              </span>
              <span class="meta-item">
                <span class="meta-icon">📅</span>
                {{ formatDate(capsule.created_at) }}
              </span>
            </div>
            
            <div class="capsule-actions">
              <router-link 
                :to="`/time-capsules/${capsule.id}`" 
                class="btn btn-glass btn-sm hover-grow"
              >
                查看详情
              </router-link>
              
              <button 
                v-if="capsule.status === 'locked' && canUnlock(capsule)"
                @click="handleUnlock(capsule.id)"
                class="btn btn-primary btn-sm hover-grow animate-pulse"
              >
                <span class="btn-icon">🔓</span>
                解锁
              </button>
              
              <button 
                v-if="capsule.status === 'unlocked'"
                @click="handlePublish(capsule.id)"
                class="btn btn-secondary btn-sm hover-grow"
              >
                <span class="btn-icon">🌍</span>
                发布到回音廊
              </button>
            </div>
            
            <!-- 装饰元素 -->
            <div class="capsule-decoration"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useTimeCapsuleStore } from '../stores/timeCapsule'
import { storeToRefs } from 'pinia'
import dayjs from 'dayjs'

const timeCapsuleStore = useTimeCapsuleStore()
const { capsules, loading } = storeToRefs(timeCapsuleStore)

onMounted(async () => {
  await timeCapsuleStore.fetchMyCapsules()
})

/**
 * 获取状态文本
 */
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    locked: '已锁定',
    unlocked: '已解锁',
    public: '已公开'
  }
  return statusMap[status] || status
}

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
  return dayjs(date).format('YYYY-MM-DD')
}

/**
 * 格式化解锁日期
 */
const formatUnlockDate = (date: string) => {
  const unlockDate = dayjs(date)
  if (unlockDate.isBefore(dayjs())) {
    return '可解锁'
  }
  return unlockDate.format('YYYY-MM-DD HH:mm')
}

/**
 * 检查是否可以解锁
 */
const canUnlock = (capsule: any) => {
  return timeCapsuleStore.canUnlock(capsule)
}

/**
 * 解锁信箱
 */
const handleUnlock = async (id: string) => {
  try {
    const result = await timeCapsuleStore.unlockCapsule(id)
    if (result.success) {
      alert('解锁成功！')
      await timeCapsuleStore.fetchMyCapsules()
    } else {
      alert(result.message)
    }
  } catch (error) {
    alert('解锁失败')
  }
}

/**
 * 发布到回音廊
 */
const handlePublish = async (id: string) => {
  if (confirm('确定要将这个时空信箱发布到公共回音廊吗？')) {
    try {
      const result = await timeCapsuleStore.publishCapsule(id)
      if (result.success) {
        alert('发布成功！')
        await timeCapsuleStore.fetchMyCapsules()
      }
    } catch (error) {
      alert('发布失败')
    }
  }
}
</script>

<style scoped>
@import '../styles/animations.css';
@import '../styles/variables.css';

.page-container {
  min-height: calc(100vh - 70px);
  padding: 60px 0;
  background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 60px;
}

.btn-icon {
  margin-right: 8px;
  font-size: 20px;
  vertical-align: middle;
}

/* 时间轴布局 */
.timeline-container {
  position: relative;
  padding: 20px 0;
  max-width: 1000px;
  margin: 0 auto;
}

.timeline-line {
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 3px;
  background: var(--primary-gradient);
  transform: translateX(-50%);
}

.timeline-item {
  position: relative;
  margin-bottom: 50px;
  width: 45%;
}

.timeline-item.left {
  left: 0;
  text-align: right;
}

.timeline-item.right {
  left: 55%;
  text-align: left;
}

.timeline-dot {
  position: absolute;
  width: 20px;
  height: 20px;
  background: white;
  border: 4px solid var(--color-primary);
  border-radius: 50%;
  top: 20px;
  z-index: 2;
}

.timeline-item.left .timeline-dot {
  right: -47px;
}

.timeline-item.right .timeline-dot {
  left: -47px;
}

.timeline-dot::after {
  content: '';
  position: absolute;
  width: 40px;
  height: 40px;
  background: rgba(124, 58, 237, 0.2);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: pulse 2s infinite;
}

/* 卡片样式 */
.capsule-card {
  background: white;
  border-radius: var(--border-radius-lg);
  padding: 30px;
  box-shadow: var(--shadow-lg);
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
  display: inline-block;
  width: 100%;
  text-align: left;
}

.capsule-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--primary-gradient);
  transform: scaleX(0);
  transition: transform var(--transition-normal);
  transform-origin: left;
}

.capsule-card:hover::before {
  transform: scaleX(1);
}

.capsule-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.capsule-title {
  font-size: 24px;
  font-weight: bold;
  color: var(--text-primary);
  margin: 0;
  flex: 1;
}

.capsule-status {
  padding: 6px 16px;
  border-radius: var(--border-radius-full);
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.status-locked {
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
  color: #f57c00;
}

.status-locked .status-dot {
  background: #f57c00;
  animation: blink 2s infinite;
}

.status-unlocked {
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
  color: #388e3c;
}

.status-unlocked .status-dot {
  background: #388e3c;
}

.status-public {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  color: #1976d2;
}

.status-public .status-dot {
  background: #1976d2;
}

.capsule-content {
  color: var(--text-secondary);
  line-height: 1.8;
  margin-bottom: 20px;
  font-size: 16px;
}

.capsule-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 24px;
  font-size: 14px;
  color: var(--text-tertiary);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.meta-icon {
  font-size: 16px;
}

.capsule-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.btn-sm {
  padding: 10px 20px;
  font-size: 14px;
}

.capsule-decoration {
  position: absolute;
  bottom: -100px;
  right: -100px;
  width: 200px;
  height: 200px;
  background: var(--primary-gradient);
  opacity: 0.05;
  border-radius: 50%;
  transition: all var(--transition-normal);
}

.capsule-card:hover .capsule-decoration {
  transform: scale(1.5) rotate(45deg);
  opacity: 0.1;
}

/* 网格布局（备用） */
.capsules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 30px;
}

/* 响应式 */
@media (max-width: 768px) {
  .timeline-line {
    left: 20px;
  }
  
  .timeline-item {
    width: calc(100% - 40px);
    left: 40px !important;
  }
  
  .timeline-item.left,
  .timeline-item.right {
    text-align: left;
  }
  
  .timeline-item.left .timeline-dot,
  .timeline-item.right .timeline-dot {
    left: -30px;
    right: auto;
  }
  
  .page-header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .capsule-actions {
    flex-direction: column;
  }
  
  .btn-sm {
    width: 100%;
  }
}
</style>