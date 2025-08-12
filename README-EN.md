[English](README-EN.md) | [中文](README.md)

# Echo - Time Capsules and Emotional Echo Wall

A warm web application that lets users seal regrets in time, let hopes travel across time, and ensure every call finds its echo.

## Features

### 🎯 Time Capsules
- Create digital letters to capture regrets and hopes
- Set a future unlock time or specific trigger conditions
- After unlocking, optionally publish to the public Echo Gallery
- Keep private or share publicly

### 🌊 Emotional Echo Wall
- Send anonymous emotional shouts to the world
- Intelligent emotion matching system
- Delayed, mindful connection experience
- Warm responses that transcend time

## Tech Stack

- Backend: FastAPI + Python 3.12 + uv package manager
- Frontend: Vue 3 + Vite + TypeScript + pnpm
- Database: Supabase (PostgreSQL)
- Deployment: Docker containerization

## Quick Start

### Requirements
- Python 3.12+
- Node.js 20+
- Docker & Docker Compose (optional)

### Local Development

1. Backend
```bash
cd backend
uv sync
uv run uvicorn main:app --reload
```

2. Frontend
```bash
cd frontend
pnpm install
pnpm dev
```

3. Access the App
- Frontend: http://localhost:5173
- Backend API Docs: http://localhost:8000/api/docs

### Docker Deployment

```bash
# Build and start
docker-compose up -d

# Access the app
# http://localhost:3000
```

## Environment Variables

Create `backend/.env`:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
# optional but recommended for backend service access under RLS
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
SECRET_KEY=your_secret_key
```

## Project Structure

```
Echo/
├── backend/          # FastAPI backend
│   ├── app/          # Application code
│   │   ├── api/      # API endpoints
│   │   ├── core/     # Core functionality
│   │   └── schemas/  # Data models
│   └── main.py       # Entry point
├── frontend/         # Vue frontend
│   ├── src/
│   │   ├── api/      # API calls
│   │   ├── router/   # Route configuration
│   │   ├── stores/   # Pinia stores
│   │   └── views/    # Pages/components
│   └── index.html
├── Dockerfile        # Docker config
└── docker-compose.yml
```

## API Endpoints

- `/api/auth/*` - Authentication
- `/api/time-capsules/*` - Time Capsule management
- `/api/echo-wall/*` - Echo Wall features

## Database Schema

- `time_capsules` - Time capsule table
- `echo_wall` - Echo wall messages table
- `echo_matches` - Emotional match records table

## License

MIT
