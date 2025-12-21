# 🐳 Docker Deployment Guide

Complete guide for running AI Code Explainer backend in Docker containers.

---

## 📋 Prerequisites

1. **Docker Desktop** installed and running

   - Download: https://www.docker.com/products/docker-desktop
   - Verify: `docker --version` and `docker-compose --version`

2. **Groq API Key** configured
   - Make sure `backend/.env` exists with `GROQ_API_KEY=your_key_here`

---

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

```powershell
# From project root directory
docker-compose up -d
```

This single command will:

- ✅ Build the Docker image
- ✅ Download the embedding model
- ✅ Start the backend server
- ✅ Create persistent volumes for data
- ✅ Set up health checks

**Access the API**: http://localhost:8000

### Option 2: Using Docker CLI

```powershell
# Build the image
cd backend
docker build -t ai-code-explainer-backend .

# Run the container
docker run -d `
  --name ai-code-explainer `
  -p 8000:8000 `
  --env-file .env `
  -v ai-code-explainer-chroma:/app/chroma_db `
  -v ai-code-explainer-models:/app/.cache/huggingface `
  ai-code-explainer-backend
```

---

## 📖 Step-by-Step Instructions

### Step 1: Prepare Environment

```powershell
# Navigate to project root
cd "C:\Users\ehtes\work\Nazish Project\JanZ Code Explainer"

# Verify .env file exists in backend/
Get-Content backend\.env
# Should show: GROQ_API_KEY=gsk_...
```

### Step 2: Build the Docker Image

```powershell
# Using docker-compose (builds automatically)
docker-compose build

# Or using Docker CLI
cd backend
docker build -t ai-code-explainer-backend .
```

**Build time**: 5-10 minutes (downloads ~500MB of dependencies)

**What happens during build:**

- ✅ Python 3.13 base image pulled
- ✅ System dependencies installed
- ✅ Python packages installed (FastAPI, ChromaDB, etc.)
- ✅ Embedding model downloaded (~90MB)
- ✅ Application code copied

### Step 3: Populate the Database (First Time Only)

```powershell
# Start the container
docker-compose up -d

# Run ingestion script inside container
docker-compose exec backend python ingest_documents.py --reset

# You should see:
# Successfully ingested 10 documents into ChromaDB
```

### Step 4: Verify Container is Running

```powershell
# Check container status
docker-compose ps

# Should show:
# NAME                          STATUS    PORTS
# ai-code-explainer-backend     Up        0.0.0.0:8000->8000/tcp

# Check logs
docker-compose logs backend

# Should show Phase 3 startup messages
```

### Step 5: Test the API

**Browser:**

- Health Check: http://localhost:8000/health
- API Docs: http://localhost:8000/docs
- Metrics: http://localhost:8000/api/metrics/performance

**PowerShell:**

```powershell
# Test health endpoint
Invoke-WebRequest http://localhost:8000/health | Select-Object -Expand Content

# Test explanation endpoint
$body = @{
    code = "def hello(): print('world')"
    language = "python"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/explain -Body $body -ContentType "application/json"
```

### Step 6: Use with Frontend

```powershell
# Frontend still runs locally, just point it to Docker backend
start frontend/index_phase3.html

# Backend URL is already http://localhost:8000
# No changes needed!
```

---

## 🛠️ Common Commands

### Container Management

```powershell
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View logs (live)
docker-compose logs -f backend

# View logs (last 100 lines)
docker-compose logs --tail=100 backend

# Execute command in running container
docker-compose exec backend python view_database.py

# Open bash shell in container
docker-compose exec backend bash
```

### Maintenance

```powershell
# Rebuild after code changes
docker-compose up -d --build

# Remove everything (including volumes)
docker-compose down -v

# View resource usage
docker stats ai-code-explainer-backend

# Inspect container
docker inspect ai-code-explainer-backend
```

### Database Management

```powershell
# View database contents
docker-compose exec backend python view_database.py

# Reset and repopulate database
docker-compose exec backend python ingest_documents.py --reset

# Run tests
docker-compose exec backend python run_tests.py
```

---

## 📊 Data Persistence

Docker volumes ensure your data survives container restarts:

| Volume        | Purpose                    | Location in Container     |
| ------------- | -------------------------- | ------------------------- |
| `chroma-data` | Vector database (ChromaDB) | `/app/chroma_db`          |
| `model-cache` | Downloaded embedding model | `/app/.cache/huggingface` |

**View volumes:**

```powershell
docker volume ls
docker volume inspect ai-code-explainer_chroma-data
```

**Backup data:**

```powershell
# Create backup directory
mkdir backups

# Backup ChromaDB
docker cp ai-code-explainer-backend:/app/chroma_db ./backups/chroma_db_backup
```

**Restore data:**

```powershell
# Copy backup into container
docker cp ./backups/chroma_db_backup/. ai-code-explainer-backend:/app/chroma_db
```

---

## 🔧 Troubleshooting

### Issue 1: Container won't start

```powershell
# Check logs for errors
docker-compose logs backend

# Common causes:
# - Missing .env file
# - Invalid GROQ_API_KEY
# - Port 8000 already in use
```

**Solution:**

```powershell
# Check if port is in use
netstat -ano | findstr :8000

# Kill process using port (replace PID)
Stop-Process -Id <PID> -Force

# Or change port in docker-compose.yaml
# ports:
#   - "8001:8000"  # Use port 8001 instead
```

### Issue 2: "Unhealthy" status

```powershell
# Check health status
docker inspect ai-code-explainer-backend | Select-String -Pattern "Health"

# View health check logs
docker inspect ai-code-explainer-backend --format='{{json .State.Health}}' | ConvertFrom-Json
```

**Solution:**

```powershell
# Wait 40 seconds after startup (healthcheck start-period)
# If still unhealthy, check logs for startup errors
docker-compose logs backend
```

### Issue 3: Model download fails during build

**Solution:**

```powershell
# Build without model download
# Comment out line in Dockerfile:
# RUN python download_model.py

# Then download after container starts
docker-compose up -d
docker-compose exec backend python download_model.py
```

### Issue 4: Database empty after restart

```powershell
# Verify volume is mounted
docker inspect ai-code-explainer-backend | Select-String -Pattern "Mounts"

# Re-ingest documents
docker-compose exec backend python ingest_documents.py --reset
```

### Issue 5: Out of memory

```powershell
# Check Docker Desktop settings:
# Settings → Resources → Memory
# Increase to at least 4GB

# Or add memory limit in docker-compose.yaml:
# services:
#   backend:
#     deploy:
#       resources:
#         limits:
#           memory: 4G
```

---

## 🚀 Production Deployment

### Security Hardening

1. **Remove development volume mount** in docker-compose.yaml:

   ```yaml
   # Comment out this line:
   # - ./backend:/app
   ```

2. **Use secrets for API key**:

   ```yaml
   secrets:
     groq_api_key:
       file: ./backend/.env.secret
   ```

3. **Run as non-root user** in Dockerfile:
   ```dockerfile
   RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
   USER appuser
   ```

### Performance Optimization

1. **Multi-stage build** (reduce image size):

   ```dockerfile
   # Build stage
   FROM python:3.13-slim as builder
   # ... install dependencies ...

   # Runtime stage
   FROM python:3.13-slim
   COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13
   ```

2. **Use gunicorn** instead of uvicorn:
   ```yaml
   command:
     [
       "gunicorn",
       "main:app",
       "-w",
       "4",
       "-k",
       "uvicorn.workers.UvicornWorker",
       "--bind",
       "0.0.0.0:8000",
     ]
   ```

### Monitoring

1. **Add Prometheus metrics**:

   ```yaml
   services:
     prometheus:
       image: prom/prometheus
       volumes:
         - ./prometheus.yml:/etc/prometheus/prometheus.yml
   ```

2. **View logs in production**:
   ```powershell
   docker-compose logs -f --tail=1000 backend > logs.txt
   ```

---

## 📚 Additional Resources

- **Docker Documentation**: https://docs.docker.com/
- **Docker Compose Reference**: https://docs.docker.com/compose/
- **FastAPI Docker Guide**: https://fastapi.tiangolo.com/deployment/docker/
- **Project README**: [README.md](README.md)
- **Testing Guide**: [PHASE3_TESTING.md](PHASE3_TESTING.md)

---

## 🎯 Next Steps

1. ✅ Run `docker-compose up -d`
2. ✅ Verify at http://localhost:8000/health
3. ✅ Populate database with `docker-compose exec backend python ingest_documents.py --reset`
4. ✅ Test frontend with [frontend/index_phase3.html](frontend/index_phase3.html)
5. ✅ Run tests with `docker-compose exec backend python run_tests.py`

**Need help?** Check logs with `docker-compose logs -f backend`
