# 多阶段构建 - 前端构建阶段
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# 安装pnpm
RUN npm install -g pnpm

# 复制前端依赖文件
COPY frontend/package.json frontend/pnpm-lock.yaml ./

# 安装依赖
RUN pnpm install --frozen-lockfile

# 复制前端源代码
COPY frontend/ ./

# 构建前端
RUN pnpm build

# 后端运行阶段
FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖和nginx
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# 安装uv
RUN pip install uv

# 复制后端代码和依赖
COPY backend/pyproject.toml backend/.env ./backend/
COPY backend/app ./backend/app
COPY backend/main.py ./backend/
COPY backend/static ./backend/static

# 安装后端依赖
WORKDIR /app/backend
RUN uv sync

# 复制前端构建产物到nginx目录
COPY --from=frontend-builder /app/frontend/dist /usr/share/nginx/html

# 配置nginx
RUN echo 'server { \n\
    listen 80; \n\
    server_name localhost; \n\
    \n\
    # 前端静态文件 \n\
    location / { \n\
        root /usr/share/nginx/html; \n\
        try_files $uri $uri/ /index.html; \n\
    } \n\
    \n\
    # API代理 \n\
    location /api { \n\
        proxy_pass http://127.0.0.1:8000; \n\
        proxy_http_version 1.1; \n\
        proxy_set_header Upgrade $http_upgrade; \n\
        proxy_set_header Connection "upgrade"; \n\
        proxy_set_header Host $host; \n\
        proxy_set_header X-Real-IP $remote_addr; \n\
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \n\
        proxy_set_header X-Forwarded-Proto $scheme; \n\
    } \n\
}' > /etc/nginx/sites-available/default

# 配置supervisor
RUN echo '[supervisord] \n\
nodaemon=true \n\
\n\
[program:nginx] \n\
command=nginx -g "daemon off;" \n\
autostart=true \n\
autorestart=true \n\
stdout_logfile=/dev/stdout \n\
stdout_logfile_maxbytes=0 \n\
stderr_logfile=/dev/stderr \n\
stderr_logfile_maxbytes=0 \n\
\n\
[program:fastapi] \n\
command=uv run uvicorn main:app --host 0.0.0.0 --port 8000 \n\
directory=/app/backend \n\
autostart=true \n\
autorestart=true \n\
stdout_logfile=/dev/stdout \n\
stdout_logfile_maxbytes=0 \n\
stderr_logfile=/dev/stderr \n\
stderr_logfile_maxbytes=0' > /etc/supervisor/conf.d/supervisord.conf

# 暴露端口
EXPOSE 80

# 启动supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]