<template>
  <div class="page-container">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">创建时空信箱</h1>
      </div>
      
      <div class="create-form-card">
        <form @submit.prevent="handleCreate">
          <div class="form-group">
            <label class="form-label">标题</label>
            <input
              v-model="form.title"
              type="text"
              class="form-control"
              placeholder="给你的时空信箱起个名字"
              required
              maxlength="100"
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">内容</label>
            <textarea
              v-model="form.content"
              class="form-control"
              placeholder="写下你的遗憾、期盼，或想对未来说的话..."
              rows="8"
              required
            ></textarea>
          </div>
          
          <div class="form-group">
            <label class="form-label">解锁时间（可选）</label>
            <input
              v-model="form.unlock_date"
              type="datetime-local"
              class="form-control"
              :min="minDate"
            />
            <small class="form-hint">设置一个未来的时间点，到时候才能打开这个信箱</small>
          </div>
          
          <div class="form-group">
            <label class="form-label">解锁条件（可选）</label>
            <input
              v-model="form.unlock_condition"
              type="text"
              class="form-control"
              placeholder="例如：当我实现了某个目标时"
              maxlength="200"
            />
            <small class="form-hint">描述一个特殊的条件或时刻</small>
          </div>
          
          <div class="form-group">
            <label class="checkbox-label">
              <input
                v-model="form.is_public"
                type="checkbox"
              />
              <span>解锁后允许发布到公共回音廊</span>
            </label>
          </div>
          
          <div v-if="error" class="error">{{ error }}</div>
          
          <div class="form-actions">
            <router-link to="/time-capsules" class="btn btn-secondary">
              取消
            </router-link>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? '创建中...' : '创建信箱' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useTimeCapsuleStore } from '../stores/timeCapsule'
import dayjs from 'dayjs'

const router = useRouter()
const timeCapsuleStore = useTimeCapsuleStore()

const form = ref({
  title: '',
  content: '',
  unlock_date: '',
  unlock_condition: '',
  is_public: false
})

const loading = ref(false)
const error = ref('')

// 计算最小日期（明天）
const minDate = computed(() => {
  return dayjs().add(1, 'day').format('YYYY-MM-DDTHH:mm')
})

/**
 * 处理创建
 */
const handleCreate = async () => {
  error.value = ''
  
  // 验证
  if (!form.value.title.trim() || !form.value.content.trim()) {
    error.value = '请填写标题和内容'
    return
  }
  
  if (form.value.unlock_date && dayjs(form.value.unlock_date).isBefore(dayjs())) {
    error.value = '解锁时间必须是未来的时间'
    return
  }
  
  loading.value = true
  
  try {
    const data = {
      title: form.value.title.trim(),
      content: form.value.content.trim(),
      unlock_date: form.value.unlock_date || undefined,
      unlock_condition: form.value.unlock_condition.trim() || undefined,
      is_public: form.value.is_public
    }
    
    await timeCapsuleStore.createCapsule(data)
    router.push('/time-capsules')
  } catch (err: any) {
    error.value = err.response?.data?.detail || '创建失败，请稍后重试'
  } finally {
    loading.value = false
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
  margin-bottom: 32px;
}

.create-form-card {
  background: white;
  border-radius: 12px;
  padding: 40px;
  max-width: 700px;
  margin: 0 auto;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.form-hint {
  display: block;
  margin-top: 8px;
  font-size: 14px;
  color: #999;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.checkbox-label input {
  margin-right: 8px;
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.checkbox-label span {
  font-size: 16px;
  color: #555;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 32px;
}
</style>