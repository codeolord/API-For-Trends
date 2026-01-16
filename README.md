# README

A complete, production-ready **AI-Driven Print-on-Demand Trend & Design Automation Platform**.

## 🚀 What It Does

- **Scrapes** Amazon, Etsy, Shopify, and Printful for trending products
- **Analyzes** demand, competition, growth, and profitability metrics
- **Generates** original AI-powered designs ready for print-on-demand
- **Publishes** automatically to Printful and Shopify

## 🛠️ Tech Stack

**Backend**: Python, FastAPI, PostgreSQL, Redis, Celery
**Frontend**: Next.js, TypeScript, Tailwind CSS
**AI**: OpenAI/Anthropic, Stable Diffusion, embeddings
**Infrastructure**: Docker, Docker Compose

## 📁 Project Structure

```
API for Trends/
├── backend/          # FastAPI application
├── frontend/         # Next.js dashboard
├── infra/           # Docker Compose configuration
└── docs/            # Documentation
```

## ⚡ Quick Start

### Using Docker Compose
```bash
cd "API for Trends"
cp backend/.env.example backend/.env
# Edit backend/.env with API keys
docker-compose -f infra/docker-compose.yml up -d
```

Access:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Local Development
```bash
# Backend
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt && uvicorn main:app --reload

# Frontend (separate terminal)
cd frontend && npm install && npm run dev

# Celery worker (separate terminal)
cd backend && celery -A app.celery_app worker --loglevel=info
```

## 📊 Key Features

### Trend Analysis
- AI scoring: demand, competition, growth, profitability
- Target audience inference
- Price point analysis
- Marketplace distribution tracking

### Design Generation
- AI-powered design creation
- Multiple design variants per trend
- Print specifications
- Product mockups

### Automation
- Scheduled marketplace scraping
- Background trend analysis
- Automatic design generation
- One-click publishing to Printful/Shopify

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design
- [API Documentation](docs/API.md) - Endpoint reference
- [Setup Guide](docs/SETUP.md) - Deployment & configuration

## 🎯 Roadmap

- [x] Phase 1: Marketplace scraping + trend scoring
- [ ] Phase 2: Audience + pricing intelligence
- [ ] Phase 3: AI design generation + automation
- [ ] Phase 4: User accounts & analytics

## 🔑 Environment Variables

### Backend
```env
DATABASE_URL=postgresql://user:password@localhost:5432/pod_trends
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
PRINTFUL_API_KEY=...
SHOPIFY_ACCESS_TOKEN=...
SHOPIFY_STORE_NAME=...
```

### Frontend
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## 📝 API Examples

### Get Trends
```bash
curl http://localhost:8000/api/v1/trends?limit=10
```

### Create Trend
```bash
curl -X POST http://localhost:8000/api/v1/trends \
  -H "Content-Type: application/json" \
  -d '{
    "niche": "minimalist decor",
    "category": "home",
    "demand_score": 75,
    ...
  }'
```

See [API.md](docs/API.md) for complete documentation.

## 🚢 Deployment

### Frontend → Vercel
```bash
vercel deploy --prod
```

### Backend → Cloud Run
```bash
docker build -t pod-trends-backend .
gcloud run deploy pod-trends-backend --image pod-trends-backend
```

See [SETUP.md](docs/SETUP.md) for detailed deployment steps.

## 📊 Database

### Tables
- **products**: Scraped marketplace products
- **trends**: AI-analyzed trends with scores
- **designs**: AI-generated designs
- **marketplaces**: Marketplace tracking

## 🔧 Configuration

### Scaling Workers
```bash
celery -A app.celery_app worker --loglevel=info -c 8
```

### Database Indexes
Already configured in models for optimal query performance.

## 🐛 Troubleshooting

**Port in use?**
```bash
docker-compose -f infra/docker-compose.yml down
```

**Database error?**
```bash
docker logs pod-trends-postgres
```

**API not responding?**
```bash
curl http://localhost:8000/health
```

## 📄 License

MIT

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

Open a GitHub issue for bugs or feature requests.

---

**Built with ❤️ for print-on-demand entrepreneurs**
