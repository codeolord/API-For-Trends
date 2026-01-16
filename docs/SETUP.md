# Setup & Deployment Guide

## Prerequisites

- Docker Desktop (for containerized development)
- Python 3.11+ (for local backend development)
- Node.js 18+ (for local frontend development)
- Git
- Text editor/IDE (VS Code recommended)

## Local Development Setup

### Option 1: Docker Compose (Recommended)

**1. Clone the repository**
```bash
git clone <repo>
cd "API for Trends"
```

**2. Configure environment variables**
```bash
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local
```

**3. Edit `backend/.env` with your API keys**
```env
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
PRINTFUL_API_KEY=your-printful-key
SHOPIFY_ACCESS_TOKEN=your-shopify-token
SHOPIFY_STORE_NAME=your-store-name
```

**4. Start the stack**
```bash
docker-compose -f infra/docker-compose.yml up -d
```

Wait for all services to be healthy:
```bash
docker-compose -f infra/docker-compose.yml ps
```

**5. Initialize the database**
```bash
# Run migrations (when alembic is set up)
docker exec pod-trends-backend alembic upgrade head

# Or create tables directly
docker exec pod-trends-backend python -c "
from app.database import engine
from app.models import Base
Base.metadata.create_all(bind=engine)
"
```

**6. Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Swagger UI: http://localhost:8000/docs

### Option 2: Local Development (Manual Setup)

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment
cp .env.example .env

# Edit .env with your configuration
```

**Start PostgreSQL and Redis locally**
```bash
# Using Docker for just the services
docker run -d -p 5432:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=pod_trends postgres:16-alpine
docker run -d -p 6379:6379 redis:7-alpine
```

**Run migrations (optional)**
```bash
# When Alembic is set up
alembic upgrade head
```

**Start backend server**
```bash
uvicorn main:app --reload
```

**Start Celery worker** (separate terminal)
```bash
celery -A app.celery_app worker --loglevel=info
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Copy environment
cp .env.local.example .env.local

# Start dev server
npm run dev
```

Access at http://localhost:3000

## Database Setup

### Create Tables
```sql
-- PostgreSQL
CREATE DATABASE pod_trends;

-- Then the app will create tables on startup via SQLAlchemy
```

### Or manually with psql
```bash
psql -U user -h localhost -d pod_trends < schema.sql
```

## Environment Variables

### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/pod_trends
REDIS_URL=redis://localhost:6379/0

# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Third Party APIs
PRINTFUL_API_KEY=...
SHOPIFY_ACCESS_TOKEN=...
SHOPIFY_STORE_NAME=your-store

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# App
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=your-secret-key
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Testing API Endpoints

### Using cURL
```bash
# List trends
curl http://localhost:8000/api/v1/trends

# Get specific trend
curl http://localhost:8000/api/v1/trends/1

# Create trend
curl -X POST http://localhost:8000/api/v1/trends \
  -H "Content-Type: application/json" \
  -d '{
    "niche": "minimalist decor",
    "category": "home",
    "demand_score": 75,
    "competition_score": 50,
    "growth_score": 80,
    "profitability_score": 70,
    "overall_score": 73,
    "marketplace_counts": {"amazon": 100},
    "avg_price": 24.99,
    "price_range": {"min": 10, "max": 50},
    "total_reviews": 1000,
    "avg_rating": 4.5
  }'
```

### Using Postman
Import the API documentation from http://localhost:8000/docs and use Swagger UI to test.

### Using Python Requests
```python
import requests

base_url = "http://localhost:8000/api/v1"

# Get trends
response = requests.get(f"{base_url}/trends")
print(response.json())

# Create trend
trend_data = {
    "niche": "gaming",
    "category": "merchandise",
    "demand_score": 85,
    "competition_score": 60,
    "growth_score": 82,
    "profitability_score": 75,
    "overall_score": 77.5,
    "marketplace_counts": {"amazon": 200, "etsy": 150},
    "avg_price": 29.99,
    "price_range": {"min": 15, "max": 60},
    "total_reviews": 2000,
    "avg_rating": 4.7
}
response = requests.post(f"{base_url}/trends", json=trend_data)
print(response.json())
```

## Deployment to Production

### Frontend Deployment (Vercel)

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <github-repo>
git push -u origin main
```

2. **Connect to Vercel**
- Go to https://vercel.com
- Import your GitHub repository
- Configure build settings:
  - Framework: Next.js
  - Root Directory: frontend
  - Build Command: `npm run build`
  - Start Command: `npm start`

3. **Set Environment Variables**
```env
NEXT_PUBLIC_API_URL=https://your-api-domain.com/api/v1
```

### Backend Deployment (Cloud Run)

**1. Create Docker image**
```bash
cd backend
docker build -t pod-trends-backend:latest .
```

**2. Push to Container Registry**
```bash
docker tag pod-trends-backend gcr.io/your-project/pod-trends-backend:latest
docker push gcr.io/your-project/pod-trends-backend:latest
```

**3. Deploy to Cloud Run**
```bash
gcloud run deploy pod-trends-backend \
  --image gcr.io/your-project/pod-trends-backend:latest \
  --platform managed \
  --region us-central1 \
  --set-env-vars DATABASE_URL=<cloud-sql-url>,REDIS_URL=<redis-url> \
  --allow-unauthenticated
```

### Database Deployment (Cloud SQL)

1. Create Cloud SQL instance
2. Set up CloudSQL Proxy
3. Update DATABASE_URL in Cloud Run environment

### Redis Deployment (Cloud Memorystore)

1. Create Memorystore Redis instance
2. Update REDIS_URL with instance connection string

## Monitoring & Logs

### Docker Compose Logs
```bash
# All services
docker-compose -f infra/docker-compose.yml logs -f

# Specific service
docker-compose -f infra/docker-compose.yml logs -f backend
```

### Application Logs
```bash
# Check FastAPI startup
curl http://localhost:8000/health

# Check Celery worker
# Window should show task execution logs
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :8000
# Kill it
kill -9 <PID>

# Or change ports in docker-compose.yml
```

### Database Connection Error
```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Test connection
psql -h localhost -U user -d pod_trends

# Check logs
docker logs pod-trends-postgres
```

### Redis Connection Error
```bash
# Check Redis is running
docker ps | grep redis

# Test connection
redis-cli -h localhost ping

# Should return PONG
```

### Frontend API Connection Error
1. Verify backend is running: http://localhost:8000/health
2. Check NEXT_PUBLIC_API_URL in .env.local
3. Clear browser cache and restart frontend
4. Check browser console for CORS errors

## Performance Tuning

### Database
```sql
-- Create indexes
CREATE INDEX idx_products_marketplace_category ON products(marketplace, category);
CREATE INDEX idx_trends_overall_score ON trends(overall_score DESC);
CREATE INDEX idx_designs_trend_id ON designs(trend_id);
```

### Caching
- Redis TTL for trends: 1 hour
- Redis TTL for products: 6 hours
- Browser cache for images: 24 hours

### Worker Scaling
```bash
# Start multiple Celery workers
celery -A app.celery_app worker --loglevel=info -c 4  # 4 concurrent tasks
```

## CI/CD Pipeline

### GitHub Actions Example (.github/workflows/deploy.yml)
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Vercel
        uses: vercel/action@master
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          scope: your-vercel-team
      
      - name: Deploy Backend
        run: |
          # Cloud Run deployment
          gcloud run deploy pod-trends-backend \
            --image gcr.io/your-project/pod-trends-backend:latest
```

## Scaling Considerations

1. **Database**: Add read replicas, optimize queries
2. **Cache**: Migrate to Redis cluster
3. **Workers**: Add more Celery workers, use task routing
4. **CDN**: Use CloudFlare for image caching

## Support

For issues:
1. Check logs: `docker-compose logs`
2. Review API documentation: http://localhost:8000/docs
3. Open GitHub issue with error details
