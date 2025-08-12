[English](README-EN.md) | [中文](README.md)

# 回响 Echo - 时空信箱与情感回音壁

一个温暖的Web应用，让用户将遗憾封存于时光，让期盼穿越时空，每一声呼喊都能找到它的回音。

## 功能特性

### 🎯 时空信箱
- 创建数字信件，记录遗憾与期盼
- 设置未来解锁时间或特定触发条件
- 解锁后可选择发布到公共回音廊
- 私密保存或公开分享

### 🌊 情感回音壁
- 向世界发出匿名的情感呼喊
- 智能情感匹配系统
- 延迟的心灵连接体验
- 跨越时空的温暖回应

## 技术栈

- **后端**: FastAPI + Python 3.12 + uv包管理器
- **前端**: Vue 3 + Vite + TypeScript + pnpm
- **数据库**: Supabase (PostgreSQL)
- **部署**: Docker容器化

## 快速开始

### 环境要求
- Python 3.12+
- Node.js 20+
- Docker & Docker Compose (可选)

### 本地开发

1. **启动后端**
```bash
cd backend
uv sync
uv run uvicorn main:app --reload
```

2. **启动前端**
```bash
cd frontend
pnpm install
pnpm dev
```

3. **访问应用**
- 前端: http://localhost:5173
- 后端API文档: http://localhost:8000/api/docs

### Docker部署

```bash
# 构建并启动
docker-compose up -d

# 访问应用
# http://localhost:3000
```

## 环境配置

创建 `backend/.env` 文件：
```env
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
# optional but recommended for backend service access under RLS
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
SECRET_KEY=your_secret_key
```

## 项目结构

```
Echo/
├── backend/          # FastAPI后端
│   ├── app/         # 应用代码
│   │   ├── api/     # API端点
│   │   ├── core/    # 核心功能
│   │   └── schemas/ # 数据模型
│   └── main.py      # 入口文件
├── frontend/         # Vue前端
│   ├── src/
│   │   ├── api/     # API调用
│   │   ├── router/  # 路由配置
│   │   ├── stores/  # Pinia状态管理
│   │   └── views/   # 页面组件
│   └── index.html
├── Dockerfile       # Docker配置
└── docker-compose.yml
```

## API端点

- `/api/auth/*` - 用户认证
- `/api/time-capsules/*` - 时空信箱管理
- `/api/echo-wall/*` - 回音壁功能

## 数据库架构

- `time_capsules` - 时空信箱表
- `echo_wall` - 回音壁消息表
- `echo_matches` - 情感匹配记录表

## License

MIT