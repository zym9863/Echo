<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'
import { ref } from 'vue'

const authStore = useAuthStore()
const mobileMenuOpen = ref(false)

/**
 * 切换移动端菜单
 */
const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}
</script>

<template>
  <!-- 顶部导航栏 -->
  <nav class="navbar glass-effect" v-if="$route.name !== 'Login' && $route.name !== 'Register'">
    <div class="container">
      <div class="navbar-content">
        <router-link to="/" class="navbar-brand animate-pulse">Echo</router-link>
        
        <!-- 移动端菜单按钮 -->
        <button class="navbar-toggle" :class="{ active: mobileMenuOpen }" @click="toggleMobileMenu">
          <span></span>
          <span></span>
          <span></span>
        </button>
        
        <!-- 桌面端菜单 -->
        <ul class="navbar-nav desktop-nav" v-if="authStore.isAuthenticated">
          <li><router-link to="/" @click="mobileMenuOpen = false">首页</router-link></li>
          <li><router-link to="/time-capsules" @click="mobileMenuOpen = false">时空信箱</router-link></li>
          <li><router-link to="/echo-wall" @click="mobileMenuOpen = false">回音壁</router-link></li>
          <li><router-link to="/echo-gallery" @click="mobileMenuOpen = false">公共回音廊</router-link></li>
          <li><router-link to="/profile" @click="mobileMenuOpen = false">个人中心</router-link></li>
          <li><button class="btn btn-glass btn-sm" @click="authStore.logout">退出</button></li>
        </ul>
        
        <ul class="navbar-nav desktop-nav" v-else>
          <li><router-link to="/login">登录</router-link></li>
          <li><router-link to="/register">注册</router-link></li>
          <li><router-link to="/echo-gallery">公共回音廊</router-link></li>
        </ul>
      </div>
      
      <!-- 移动端菜单 -->
      <Transition name="slide">
        <div class="mobile-menu" v-if="mobileMenuOpen">
          <ul class="navbar-nav" v-if="authStore.isAuthenticated">
            <li><router-link to="/" @click="mobileMenuOpen = false">首页</router-link></li>
            <li><router-link to="/time-capsules" @click="mobileMenuOpen = false">时空信箱</router-link></li>
            <li><router-link to="/echo-wall" @click="mobileMenuOpen = false">回音壁</router-link></li>
            <li><router-link to="/echo-gallery" @click="mobileMenuOpen = false">公共回音廊</router-link></li>
            <li><router-link to="/profile" @click="mobileMenuOpen = false">个人中心</router-link></li>
            <li><button class="btn btn-glass btn-sm" @click="authStore.logout; mobileMenuOpen = false">退出</button></li>
          </ul>
          
          <ul class="navbar-nav" v-else>
            <li><router-link to="/login" @click="mobileMenuOpen = false">登录</router-link></li>
            <li><router-link to="/register" @click="mobileMenuOpen = false">注册</router-link></li>
            <li><router-link to="/echo-gallery" @click="mobileMenuOpen = false">公共回音廊</router-link></li>
          </ul>
        </div>
      </Transition>
    </div>
  </nav>

  <!-- 主要内容区域 -->
  <main>
    <RouterView />
  </main>
</template>

<style scoped>
@import './styles/animations.css';
@import './styles/variables.css';

/* 移动端菜单按钮 */
.navbar-toggle {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--spacing-sm);
  position: relative;
  z-index: 100;
}

.navbar-toggle span {
  display: block;
  width: 25px;
  height: 3px;
  background: var(--text-primary);
  margin: 5px 0;
  transition: all var(--transition-fast);
  border-radius: var(--border-radius-sm);
}

.navbar-toggle.active span:nth-child(1) {
  transform: rotate(45deg) translate(5px, 5px);
}

.navbar-toggle.active span:nth-child(2) {
  opacity: 0;
}

.navbar-toggle.active span:nth-child(3) {
  transform: rotate(-45deg) translate(7px, -6px);
}

/* 桌面端菜单 */
.desktop-nav {
  display: flex;
}

/* 移动端菜单 */
.mobile-menu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
  border-top: 1px solid var(--border-color);
  box-shadow: var(--shadow-xl);
  padding: var(--spacing-lg);
}

.mobile-menu .navbar-nav {
  flex-direction: column;
  gap: var(--spacing-md);
}

.mobile-menu .navbar-nav li {
  width: 100%;
}

.mobile-menu .navbar-nav a,
.mobile-menu .navbar-nav button {
  display: block;
  width: 100%;
  padding: var(--spacing-md);
  text-align: left;
  border-radius: var(--border-radius-md);
  transition: all var(--transition-fast);
}

.mobile-menu .navbar-nav a:hover,
.mobile-menu .navbar-nav button:hover {
  background: var(--bg-secondary);
  transform: translateX(5px);
}

/* 导航栏按钮样式调整 */
.navbar-nav button {
  background: none;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  font-weight: var(--font-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: var(--font-md);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-md);
}

.navbar-nav button:hover {
  color: var(--color-primary);
  background: var(--bg-secondary);
  border-color: var(--color-primary);
  transform: translateY(-2px);
}

/* 动画 */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from {
  transform: translateY(-20px);
  opacity: 0;
}

.slide-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}

/* 响应式 */
@media (max-width: 768px) {
  .navbar-toggle {
    display: block;
  }
  
  .desktop-nav {
    display: none;
  }
  
  .mobile-menu {
    display: block;
  }
  
  .navbar-content {
    justify-content: space-between;
  }
}
</style>
