<template>
  <Teleport to="body">
    <TransitionGroup name="toast" tag="div" class="toast-container">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="['toast', `toast-${toast.type}`, { 'toast-closing': toast.closing }]"
        @click="removeToast(toast.id)"
      >
        <div class="toast-icon">
          <span v-if="toast.type === 'success'">✓</span>
          <span v-else-if="toast.type === 'error'">✕</span>
          <span v-else-if="toast.type === 'warning'">!</span>
          <span v-else>ℹ</span>
        </div>
        <div class="toast-content">
          <div class="toast-title" v-if="toast.title">{{ toast.title }}</div>
          <div class="toast-message">{{ toast.message }}</div>
        </div>
        <div class="toast-progress">
          <div class="toast-progress-bar" :style="{ animationDuration: `${toast.duration}ms` }"></div>
        </div>
      </div>
    </TransitionGroup>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue'

export interface Toast {
  id: number
  type: 'success' | 'error' | 'warning' | 'info'
  title?: string
  message: string
  duration: number
  closing?: boolean
}

const toasts = ref<Toast[]>([])
let nextId = 1

/**
 * 显示Toast通知
 */
const showToast = (options: Partial<Toast> & { message: string }) => {
  const toast: Toast = {
    id: nextId++,
    type: options.type || 'info',
    title: options.title,
    message: options.message,
    duration: options.duration || 3000,
    closing: false
  }
  
  toasts.value.push(toast)
  
  // 自动移除
  setTimeout(() => {
    removeToast(toast.id)
  }, toast.duration)
  
  return toast.id
}

/**
 * 移除Toast
 */
const removeToast = (id: number) => {
  const index = toasts.value.findIndex(t => t.id === id)
  if (index !== -1) {
    toasts.value[index].closing = true
    setTimeout(() => {
      toasts.value.splice(index, 1)
    }, 300)
  }
}

/**
 * 清除所有Toast
 */
const clearToasts = () => {
  toasts.value = []
}

// 快捷方法
const success = (message: string, title?: string) => {
  return showToast({ type: 'success', message, title })
}

const error = (message: string, title?: string) => {
  return showToast({ type: 'error', message, title, duration: 5000 })
}

const warning = (message: string, title?: string) => {
  return showToast({ type: 'warning', message, title, duration: 4000 })
}

const info = (message: string, title?: string) => {
  return showToast({ type: 'info', message, title })
}

// 导出方法供外部使用
defineExpose({
  showToast,
  removeToast,
  clearToasts,
  success,
  error,
  warning,
  info
})
</script>

<style scoped>
@import '../styles/animations.css';
@import '../styles/variables.css';

.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: var(--z-notification);
  display: flex;
  flex-direction: column;
  gap: 12px;
  pointer-events: none;
}

.toast {
  min-width: 300px;
  max-width: 500px;
  background: white;
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  cursor: pointer;
  pointer-events: auto;
  display: flex;
  align-items: center;
  position: relative;
  animation: slideInRight 0.3s ease-out;
  transition: all 0.3s ease;
}

.toast:hover {
  transform: translateX(-5px);
  box-shadow: var(--shadow-2xl);
}

.toast-closing {
  animation: slideOutRight 0.3s ease-out;
  opacity: 0;
  transform: translateX(100%);
}

.toast-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  color: white;
  flex-shrink: 0;
}

.toast-content {
  flex: 1;
  padding: 12px 16px;
}

.toast-title {
  font-weight: 600;
  margin-bottom: 4px;
  color: var(--text-primary);
}

.toast-message {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.4;
}

.toast-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.toast-progress-bar {
  height: 100%;
  width: 100%;
  transform-origin: left;
  animation: progress linear forwards;
}

@keyframes progress {
  from {
    transform: scaleX(1);
  }
  to {
    transform: scaleX(0);
  }
}

@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slideOutRight {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(100%);
    opacity: 0;
  }
}

/* Toast类型样式 */
.toast-success {
  border-left: 4px solid var(--color-success);
}

.toast-success .toast-icon {
  background: var(--color-success);
}

.toast-success .toast-progress-bar {
  background: var(--color-success);
}

.toast-error {
  border-left: 4px solid var(--color-error);
}

.toast-error .toast-icon {
  background: var(--color-error);
}

.toast-error .toast-progress-bar {
  background: var(--color-error);
}

.toast-warning {
  border-left: 4px solid var(--color-warning);
}

.toast-warning .toast-icon {
  background: var(--color-warning);
}

.toast-warning .toast-progress-bar {
  background: var(--color-warning);
}

.toast-info {
  border-left: 4px solid var(--color-info);
}

.toast-info .toast-icon {
  background: var(--color-info);
}

.toast-info .toast-progress-bar {
  background: var(--color-info);
}

/* 响应式 */
@media (max-width: 480px) {
  .toast-container {
    left: 10px;
    right: 10px;
    top: 10px;
  }
  
  .toast {
    min-width: auto;
    max-width: 100%;
  }
}
</style>