// API配置
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

// 网络配置
export const NETWORK_CONFIG = {
  // API请求超时时间（毫秒）
  API_TIMEOUT: 30000, // 30秒，适应远程数据库访问
  // 重试次数
  RETRY_COUNT: 3,
  // 重试间隔（毫秒）
  RETRY_DELAY: 1000
}

// Supabase配置
export const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || 'https://fdtsurarzauisduaxmev.supabase.co'
export const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZkdHN1cmFyemF1aXNkdWF4bWV2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ5Mjk2ODgsImV4cCI6MjA3MDUwNTY4OH0.dgAFfUkFq9vOYIdufQH2XV29mFc9c-qrvER2hyoMgOA'