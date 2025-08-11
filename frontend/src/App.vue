<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <!-- 顶部导航栏 -->
  <nav class="navbar" v-if="$route.name !== 'Login' && $route.name !== 'Register'">
    <div class="container">
      <div class="navbar-content">
        <router-link to="/" class="navbar-brand">Echo</router-link>
        
        <ul class="navbar-nav" v-if="authStore.isAuthenticated">
          <li><router-link to="/">首页</router-link></li>
          <li><router-link to="/time-capsules">时空信箱</router-link></li>
          <li><router-link to="/echo-wall">回音壁</router-link></li>
          <li><router-link to="/echo-gallery">公共回音廊</router-link></li>
          <li><router-link to="/profile">个人中心</router-link></li>
          <li><button class="btn btn-secondary" @click="authStore.logout">退出</button></li>
        </ul>
        
        <ul class="navbar-nav" v-else>
          <li><router-link to="/login">登录</router-link></li>
          <li><router-link to="/register">注册</router-link></li>
          <li><router-link to="/echo-gallery">公共回音廊</router-link></li>
        </ul>
      </div>
    </div>
  </nav>

  <!-- 主要内容区域 -->
  <main>
    <RouterView />
  </main>
</template>

<style scoped>
/* 导航栏按钮样式调整 */
.navbar-nav button {
  background: none;
  border: none;
  color: #555;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.3s;
  font-size: 16px;
  padding: 8px 16px;
  border-radius: 8px;
}

.navbar-nav button:hover {
  color: #667eea;
  background: #f5f5f5;
}
</style>
