<template>
  <div class="loading-wrapper" v-if="visible">
    <div class="loading-overlay" v-if="overlay"></div>
    <div class="loading-container" :class="{ 'loading-fullscreen': fullscreen }">
      <div class="loading-spinner">
        <div class="spinner-ring"></div>
        <div class="spinner-ring"></div>
        <div class="spinner-ring"></div>
      </div>
      <div class="loading-text" v-if="text">{{ text }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  visible?: boolean
  text?: string
  fullscreen?: boolean
  overlay?: boolean
}

withDefaults(defineProps<Props>(), {
  visible: true,
  text: '加载中...',
  fullscreen: false,
  overlay: true
})
</script>

<style scoped>
@import '../styles/animations.css';
@import '../styles/variables.css';

.loading-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: var(--z-modal);
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(5px);
}

.loading-container {
  position: relative;
  padding: 40px;
  background: white;
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-2xl);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  animation: scaleIn 0.3s ease-out;
}

.loading-fullscreen {
  background: transparent;
  box-shadow: none;
}

.loading-fullscreen .loading-spinner {
  width: 80px;
  height: 80px;
}

.loading-spinner {
  position: relative;
  width: 60px;
  height: 60px;
}

.spinner-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 3px solid transparent;
  border-radius: 50%;
  animation: loading 1.5s linear infinite;
}

.spinner-ring:nth-child(1) {
  border-top-color: var(--color-primary);
  animation-delay: 0s;
}

.spinner-ring:nth-child(2) {
  border-right-color: var(--color-secondary);
  animation-delay: 0.5s;
  width: 80%;
  height: 80%;
  top: 10%;
  left: 10%;
}

.spinner-ring:nth-child(3) {
  border-bottom-color: var(--color-accent);
  animation-delay: 1s;
  width: 60%;
  height: 60%;
  top: 20%;
  left: 20%;
}

.loading-text {
  font-size: 16px;
  color: var(--text-secondary);
  font-weight: 500;
  animation: pulse 2s ease-in-out infinite;
}

.loading-fullscreen .loading-text {
  color: white;
  font-size: 18px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}
</style>