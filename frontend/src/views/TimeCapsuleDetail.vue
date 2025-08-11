<template>
  <div class="page-container">
    <div class="container">
      <div v-if="loading" class="loading">加载中...</div>
      
      <div v-else-if="!capsule" class="empty-state">
        <div class="empty-state-text">时空信箱不存在</div>
        <router-link to="/time-capsules" class="btn btn-primary">
          返回列表
        </router-link>
      </div>
      
      <div v-else class="detail-card">
        <div class="detail-header">
          <h1 class="detail-title">{{ capsule.title }}</h1>
          <span :class="['capsule-status', `status-${capsule.status}`]">
            {{ getStatusText(capsule.status) }}
          </span>
        </div>
        
        <div class="detail-content">
          <p>{{ capsule.content }}</p>
        </div>
        
        <div class="detail-meta">
          <div class="meta-item" v-if="capsule.unlock_date">
            <span class="meta-label">解锁时间：</span>
            <span class="meta-value">{{ formatDate(capsule.unlock_date) }}</span>
          </div>
          
          <div class="meta-item" v-if="capsule.unlock_condition">
            <span class="meta-label">解锁条件：</span>
            <span class="meta-value">{{ capsule.unlock_condition }}</span>
          </div>
          
          <div class="meta-item">
            <span class="meta-label">创建时间：</span>
            <span class="meta-value">{{ formatDate(capsule.created_at) }}</span>
          </div>
          
          <div class="meta-item">
            <span class="meta-label">更新时间：</span>
            <span class="meta-value">{{ formatDate(capsule.updated_at) }}</span>
          </div>
          
          <div class="meta-item">
            <span class="meta-label">公开设置：</span>
            <span class="meta-value">{{ capsule.is_public ? '允许公开' : '保持私密' }}</span>
          </div>
        </div>
        
        <div class="detail-actions">
          <router-link to="/time-capsules" class="btn btn-secondary">
            返回列表
          </router-link>
          
          <button 
            v-if="capsule.status === 'locked' && canUnlock"
            @click="handleUnlock"
            class="btn btn-primary"
          >
            解锁信箱
          </button>
          
          <button 
            v-if="capsule.status === 'unlocked' && capsule.is_public"
            @click="handlePublish"
            class="btn btn-primary"
          >
            发布到回音廊
          </button>
          
          <button 
            @click="handleDelete"
            class="btn btn-danger"
          >
            删除信箱
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTimeCapsuleStore } from '../stores/timeCapsule'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const timeCapsuleStore = useTimeCapsuleStore()

const capsule = ref<any>(null)
const loading = ref(true)

// 计算是否可以解锁
const canUnlock = computed(() => {
  if (!capsule.value) return false
  return timeCapsuleStore.canUnlock(capsule.value)
})

onMounted(async () => {
  const id = route.params.id as string
  try {
    capsule.value = await timeCapsuleStore.fetchCapsule(id)
  } catch (error) {
    console.error('Failed to fetch capsule:', error)
  } finally {
    loading.value = false
  }
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
 * 格式化日期
 */
const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

/**
 * 解锁信箱
 */
const handleUnlock = async () => {
  try {
    const result = await timeCapsuleStore.unlockCapsule(capsule.value.id)
    if (result.success) {
      alert('解锁成功！')
      capsule.value = await timeCapsuleStore.fetchCapsule(capsule.value.id)
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
const handlePublish = async () => {
  if (confirm('确定要将这个时空信箱发布到公共回音廊吗？')) {
    try {
      const result = await timeCapsuleStore.publishCapsule(capsule.value.id)
      if (result.success) {
        alert('发布成功！')
        capsule.value = await timeCapsuleStore.fetchCapsule(capsule.value.id)
      }
    } catch (error) {
      alert('发布失败')
    }
  }
}

/**
 * 删除信箱
 */
const handleDelete = async () => {
  if (confirm('确定要删除这个时空信箱吗？此操作不可恢复。')) {
    try {
      await timeCapsuleStore.deleteCapsule(capsule.value.id)
      alert('删除成功')
      router.push('/time-capsules')
    } catch (error) {
      alert('删除失败')
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

.detail-card {
  background: white;
  border-radius: 12px;
  padding: 40px;
  max-width: 800px;
  margin: 0 auto;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 2px solid #f0f0f0;
}

.detail-title {
  font-size: 32px;
  font-weight: bold;
  color: #333;
  margin: 0;
  flex: 1;
}

.capsule-status {
  padding: 8px 16px;
  border-radius: 24px;
  font-size: 14px;
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

.detail-content {
  font-size: 18px;
  line-height: 1.8;
  color: #555;
  margin-bottom: 32px;
  padding: 24px;
  background: #f8f9fa;
  border-radius: 8px;
  white-space: pre-wrap;
}

.detail-meta {
  margin-bottom: 32px;
  padding: 24px;
  background: #f8f9fa;
  border-radius: 8px;
}

.meta-item {
  display: flex;
  padding: 8px 0;
  border-bottom: 1px solid #e0e0e0;
}

.meta-item:last-child {
  border-bottom: none;
}

.meta-label {
  font-weight: 500;
  color: #666;
  width: 120px;
  flex-shrink: 0;
}

.meta-value {
  color: #333;
  flex: 1;
}

.detail-actions {
  display: flex;
  gap: 16px;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .detail-header {
    flex-direction: column;
    gap: 16px;
  }
  
  .detail-actions {
    flex-direction: column;
  }
}
</style>