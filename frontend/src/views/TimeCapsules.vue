<template>
  <div class="page-container">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">我的时空信箱</h1>
        <router-link to="/time-capsules/create" class="btn btn-primary">
          创建新信箱
        </router-link>
      </div>
      
      <div v-if="loading" class="loading">加载中...</div>
      
      <div v-else-if="capsules.length === 0" class="empty-state">
        <div class="empty-state-icon">📮</div>
        <div class="empty-state-text">还没有时空信箱</div>
        <router-link to="/time-capsules/create" class="btn btn-primary">
          创建第一个时空信箱
        </router-link>
      </div>
      
      <div v-else class="capsules-grid">
        <div v-for="capsule in capsules" :key="capsule.id" class="capsule-card">
          <div class="capsule-header">
            <h3 class="capsule-title">{{ capsule.title }}</h3>
            <span :class="['capsule-status', `status-${capsule.status}`]">
              {{ getStatusText(capsule.status) }}
            </span>
          </div>
          
          <p class="capsule-content">{{ truncateText(capsule.content, 100) }}</p>
          
          <div class="capsule-meta">
            <span v-if="capsule.unlock_date" class="meta-item">
              🔓 {{ formatUnlockDate(capsule.unlock_date) }}
            </span>
            <span v-if="capsule.unlock_condition" class="meta-item">
              📝 {{ capsule.unlock_condition }}
            </span>
            <span class="meta-item">
              📅 {{ formatDate(capsule.created_at) }}
            </span>
          </div>
          
          <div class="capsule-actions">
            <router-link 
              :to="`/time-capsules/${capsule.id}`" 
              class="btn btn-secondary btn-sm"
            >
              查看详情
            </router-link>
            
            <button 
              v-if="capsule.status === 'locked' && canUnlock(capsule)"
              @click="handleUnlock(capsule.id)"
              class="btn btn-primary btn-sm"
            >
              解锁
            </button>
            
            <button 
              v-if="capsule.status === 'unlocked'"
              @click="handlePublish(capsule.id)"
              class="btn btn-secondary btn-sm"
            >
              发布到回音廊
            </button>
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
.page-container {
  min-height: calc(100vh - 70px);
  padding: 40px 0;
  background: #f8f9fa;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
}

.capsules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.capsule-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s, box-shadow 0.3s;
}

.capsule-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.capsule-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.capsule-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin: 0;
  flex: 1;
}

.capsule-status {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
}

.status-locked {
  background: #fff3e0;
  color: #f57c00;
}

.status-unlocked {
  background: #e8f5e9;
  color: #388e3c;
}

.status-public {
  background: #e3f2fd;
  color: #1976d2;
}

.capsule-content {
  color: #666;
  line-height: 1.6;
  margin-bottom: 16px;
}

.capsule-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
  font-size: 14px;
  color: #999;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.capsule-actions {
  display: flex;
  gap: 8px;
}

.btn-sm {
  padding: 8px 16px;
  font-size: 14px;
}
</style>