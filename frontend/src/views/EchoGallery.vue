<template>
  <div class="page-container">
    <div class="container">
      <h1 class="page-title">公共回音廊</h1>
      <p class="page-subtitle">这里收藏着已解锁并公开的时空信箱，每一个都是一段珍贵的回忆</p>
      
      <div v-if="loading" class="loading">加载中...</div>
      
      <div v-else-if="publicCapsules.length === 0" class="empty-state">
        <div class="empty-state-icon">🌟</div>
        <div class="empty-state-text">回音廊还空着，等待第一个故事</div>
      </div>
      
      <div v-else class="gallery-grid">
        <div v-for="capsule in publicCapsules" :key="capsule.id" class="gallery-card">
          <h3 class="gallery-card-title">{{ capsule.title }}</h3>
          <p class="gallery-card-content">{{ capsule.content }}</p>
          
          <div class="gallery-card-meta">
            <span v-if="capsule.unlock_condition" class="meta-condition">
              💭 {{ capsule.unlock_condition }}
            </span>
            <span class="meta-date">
              📅 创建于 {{ formatDate(capsule.created_at) }}
            </span>
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
const { publicCapsules, loading } = storeToRefs(timeCapsuleStore)

onMounted(async () => {
  await timeCapsuleStore.fetchPublicCapsules()
})

/**
 * 格式化日期
 */
const formatDate = (date: string) => {
  return dayjs(date).format('YYYY年MM月DD日')
}
</script>

<style scoped>
.page-container {
  min-height: calc(100vh - 70px);
  padding: 40px 0;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.page-title {
  text-align: center;
  margin-bottom: 16px;
}

.page-subtitle {
  text-align: center;
  color: #666;
  font-size: 18px;
  margin-bottom: 40px;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 24px;
}

.gallery-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  position: relative;
  overflow: hidden;
}

.gallery-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.gallery-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
}

.gallery-card-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 16px;
}

.gallery-card-content {
  color: #555;
  line-height: 1.8;
  font-size: 16px;
  margin-bottom: 24px;
  white-space: pre-wrap;
}

.gallery-card-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 16px;
  border-top: 1px solid #eee;
  font-size: 14px;
  color: #999;
}

.meta-condition {
  color: #764ba2;
  font-style: italic;
}

.meta-date {
  color: #999;
}

@media (max-width: 768px) {
  .gallery-grid {
    grid-template-columns: 1fr;
  }
}
</style>