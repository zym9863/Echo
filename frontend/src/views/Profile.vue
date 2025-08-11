<template>
  <div class="page-container">
    <div class="container">
      <h1 class="page-title">个人中心</h1>
      
      <div class="profile-card">
        <div class="profile-header">
          <div class="profile-avatar">👤</div>
          <div class="profile-info">
            <h2>{{ currentUser?.email }}</h2>
            <p class="profile-date">加入于 {{ formatDate(currentUser?.created_at) }}</p>
          </div>
        </div>
        
        <div class="profile-stats">
          <div class="stat-item">
            <div class="stat-value">{{ capsuleCount }}</div>
            <div class="stat-label">时空信箱</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ echoCount }}</div>
            <div class="stat-label">呼喊</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ matchCount }}</div>
            <div class="stat-label">回音</div>
          </div>
        </div>
      </div>
      
      <div class="profile-section">
        <h3 class="section-title">修改密码</h3>
        <form @submit.prevent="handleChangePassword" class="password-form">
          <div class="form-group">
            <label class="form-label">原密码</label>
            <input
              v-model="passwordForm.oldPassword"
              type="password"
              class="form-control"
              required
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">新密码</label>
            <input
              v-model="passwordForm.newPassword"
              type="password"
              class="form-control"
              minlength="6"
              required
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">确认新密码</label>
            <input
              v-model="passwordForm.confirmPassword"
              type="password"
              class="form-control"
              required
            />
          </div>
          
          <div v-if="passwordError" class="error">{{ passwordError }}</div>
          <div v-if="passwordSuccess" class="success">{{ passwordSuccess }}</div>
          
          <button type="submit" class="btn btn-primary" :disabled="changingPassword">
            {{ changingPassword ? '修改中...' : '修改密码' }}
          </button>
        </form>
      </div>
      
      <div class="profile-section">
        <h3 class="section-title">账号操作</h3>
        <button @click="handleLogout" class="btn btn-danger">
          退出登录
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useTimeCapsuleStore } from '../stores/timeCapsule'
import { useEchoWallStore } from '../stores/echoWall'
import { storeToRefs } from 'pinia'
import dayjs from 'dayjs'

const router = useRouter()
const authStore = useAuthStore()
const timeCapsuleStore = useTimeCapsuleStore()
const echoWallStore = useEchoWallStore()

const { currentUser } = storeToRefs(authStore)
const { myCapsuleCount } = storeToRefs(timeCapsuleStore)
const { myEchoes, matchCount } = storeToRefs(echoWallStore)

const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const changingPassword = ref(false)
const passwordError = ref('')
const passwordSuccess = ref('')

// 计算统计数据
const capsuleCount = computed(() => myCapsuleCount.value || 0)
const echoCount = computed(() => myEchoes.value.length)

onMounted(async () => {
  // 加载统计数据
  await Promise.all([
    timeCapsuleStore.fetchMyCapsules(),
    echoWallStore.fetchMyEchoes(),
    echoWallStore.fetchMyMatches()
  ])
})

/**
 * 格式化日期
 */
const formatDate = (date: string | undefined) => {
  if (!date) return '未知'
  return dayjs(date).format('YYYY年MM月DD日')
}

/**
 * 修改密码
 */
const handleChangePassword = async () => {
  passwordError.value = ''
  passwordSuccess.value = ''
  
  // 验证
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    passwordError.value = '两次输入的新密码不一致'
    return
  }
  
  if (passwordForm.value.newPassword.length < 6) {
    passwordError.value = '新密码长度至少为6位'
    return
  }
  
  changingPassword.value = true
  
  try {
    await authStore.changePassword(
      passwordForm.value.oldPassword,
      passwordForm.value.newPassword
    )
    passwordSuccess.value = '密码修改成功'
    passwordForm.value = {
      oldPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  } catch (error: any) {
    passwordError.value = error.response?.data?.detail || '密码修改失败'
  } finally {
    changingPassword.value = false
  }
}

/**
 * 退出登录
 */
const handleLogout = async () => {
  if (confirm('确定要退出登录吗？')) {
    await authStore.logout()
    router.push('/login')
  }
}
</script>

<style scoped>
.page-container {
  min-height: calc(100vh - 70px);
  padding: 40px 0;
  background: #f8f9fa;
}

.profile-card {
  background: white;
  border-radius: 12px;
  padding: 32px;
  margin-bottom: 32px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 32px;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  color: white;
}

.profile-info h2 {
  font-size: 24px;
  margin-bottom: 8px;
  color: #333;
}

.profile-date {
  color: #999;
}

.profile-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  padding: 24px;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #999;
}

.profile-section {
  background: white;
  border-radius: 12px;
  padding: 32px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.section-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 24px;
  color: #333;
}

.password-form {
  max-width: 400px;
}

@media (max-width: 768px) {
  .profile-stats {
    grid-template-columns: 1fr;
  }
}
</style>