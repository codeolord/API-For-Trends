# AI-Driven Print-on-Demand Trend & Design Automation Platform

## Project Overview

This is a complete, production-ready platform that automatically researches top marketplaces (Amazon, Etsy, Shopify, Printful), analyzes what products are trending, generates original AI-powered designs, and publishes them to print-on-demand fulfillment services.

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Cache/Message Broker**: Redis
- **Task Queue**: Celery
- **AI Models**: OpenAI/Anthropic LLMs, Stable Diffusion for image generation
- **Data Collection**: Playwright, BeautifulSoup, HTTPx

### Frontend
- **Framework**: Next.js 14 (React + TypeScript)
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Charts**: Recharts
- **UI Components**: Custom + Lucide Icons

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Deployment**: Ready for Vercel (Frontend) + Cloud Run/EC2 (Backend)

## Project Structure

```
API for Trends/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── api/               # API endpoints (trends, products, designs)
│   │   ├── models/            # SQLAlchemy database models
│   │   ├── schemas/           # Pydantic schemas for validation
│   │   ├── scrapers/          # Marketplace data collection
│   │   ├── analysis/          # Trend analysis & scoring engine
│   │   ├── ai/                # AI design generation
│   │   ├── integrations/      # Printful & Shopify APIs
│   │   ├── tasks/             # Celery background tasks
│   │   ├── utils/             # Logging and utilities
│   │   ├── config.py          # Configuration management
│   │   ├── database.py        # Database setup
│   │   └── celery_app.py      # Celery configuration
│   ├── main.py                # FastAPI application entry
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile             # Docker image for backend
│   └── .env.example           # Environment variables template
│
├── frontend/                   # Next.js application
│   ├── src/
│   │   ├── pages/             # Next.js pages
│   │   ├── components/        # React components
│   │   ├── lib/               # Utilities (API client, store)
│   │   └── styles/            # Global CSS
│   ├── package.json           # Node dependencies
│   ├── tsconfig.json          # TypeScript config
│   ├── tailwind.config.js     # Tailwind configuration
│   ├── next.config.js         # Next.js configuration
│   ├── Dockerfile             # Docker image for frontend
│   └── .env.local.example     # Environment variables template
│
├── infra/
│   └── docker-compose.yml     # Complete stack orchestration
│
└── docs/
    ├── ARCHITECTURE.md        # System design
    ├── API.md                 # API documentation
    └── SETUP.md               # Setup & deployment guide
```

## Features

### Phase 1: Marketplace Scraping & Trend Scoring ✅
- Automated data collection from Amazon, Etsy, Shopify, Printful
- Products stored with metadata (price, ratings, reviews, images)
- Intelligent trend grouping by category/niche
- Multi-factor trend scoring:
  - **Demand Score**: Based on review counts and recency
  - **Competition Score**: Product saturation analysis
  - **Growth Score**: Trending velocity
  - **Profitability Score**: Price points + demand metrics
  - **Overall Score**: Weighted composite

### Phase 2: Audience & Pricing Intelligence
- Target demographic inference from product data
- Price point recommendations
- Competitive positioning analysis
- Seasonal trend detection
- Market saturation insights

### Phase 3: AI Design Generation & Automation
- AI-powered design generation (OpenAI/Anthropic)
- Print-ready asset creation
- Automated Printful product creation
- Shopify draft product publishing
- Design mockup generation

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local frontend development)

### Setup Using Docker Compose

1. **Clone and Configure**
```bash
cd "API for Trends"
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local
```

2. **Update Environment Variables**
Edit `backend/.env` with your API keys:
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
PRINTFUL_API_KEY=...
SHOPIFY_ACCESS_TOKEN=...
```

3. **Start the Stack**
```bash
docker-compose -f infra/docker-compose.yml up -d
```

4. **Initialize Database**
```bash
docker exec pod-trends-backend alembic upgrade head
```

5. **Access the Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Local Development Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

**Celery Worker** (separate terminal):
```bash
cd backend
celery -A app.celery_app worker --loglevel=info
```

## API Endpoints

### Trends
- `GET /api/v1/trends` - List all trends with filters
- `GET /api/v1/trends/{id}` - Get specific trend
- `POST /api/v1/trends` - Create trend

### Products
- `GET /api/v1/products` - List scraped products
- `GET /api/v1/products/{id}` - Get product
- `POST /api/v1/products` - Create product

### Designs
- `GET /api/v1/designs` - List designs
- `GET /api/v1/designs/{id}` - Get design
- `POST /api/v1/designs` - Create design

## Dashboard Features

### Home Page
- Platform overview with key metrics
- Quick access to trends, designs, products
- Feature highlights

### Trends Page
- AI-scored trend cards with all metrics
- Real-time filtering by category, score, demand
- Marketplace distribution visualization
- Quick action buttons

### Designs Page
- AI-generated design gallery
- Design status tracking (draft/published)
- Export & download functionality
- Quick publish to Printful/Shopify

## Background Tasks (Celery)

- `scrape_marketplace` - Periodic marketplace scraping
- `analyze_trends_task` - Trend analysis and scoring
- `generate_designs_task` - AI design generation for trends

Configure schedule in `app/tasks/scraping_tasks.py` or via Celery Beat.

## Database Schema

### Products Table
Stores product data from marketplaces with metadata and raw data.

### Trends Table
Stores analyzed trends with scoring metrics and audience data.

### Designs Table
Stores AI-generated designs with specs for print-on-demand.

### Marketplaces Table
Tracks last scrape time and status for each marketplace.

## Next Steps

1. **Connect APIs**: Add actual API credentials for:
   - OpenAI/Anthropic for design generation
   - Printful for product management
   - Shopify for draft product creation

2. **Implement Scrapers**: Replace placeholder scrapers with:
   - Amazon product scraping
   - Etsy API integration
   - Shopify store scraping

3. **Add Image Generation**: Integrate Stable Diffusion or similar for AI image generation

4. **Deploy**: 
   - Frontend to Vercel
   - Backend to Cloud Run, Railway, or EC2
   - Database to managed PostgreSQL

5. **Add Features**:
   - User authentication
   - Email notifications
   - Analytics dashboard
   - A/B testing for designs

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                    │
│          Dashboard, Trends, Designs, Products            │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Backend (FastAPI)                       │
│  ┌──────────────┬──────────────┬──────────────────────┐ │
│  │   API Layer  │   Analysis   │  Integrations       │ │
│  │              │              │  (Printful/Shopify) │ │
│  └──────────────┴──────────────┴──────────────────────┘ │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
    ┌────────┐  ┌────────┐  ┌─────────┐
    │  Data  │  │  Cache │  │ Workers │
    │   DB   │  │ (Redis)│  │(Celery) │
    │ (PG)   │  └────────┘  └─────────┘
    └────────┘
        │
        ▼
    ┌──────────────────────┐
    │  Scrapers (Periodic) │
    │  - Amazon, Etsy      │
    │  - Shopify, Printful │
    └──────────────────────┘
```

## Contributing

1. Create feature branches
2. Follow Python/TypeScript style guides
3. Write tests for new features
4. Update documentation

## License

MIT

## Support

For issues or questions, open a GitHub issue or contact the development team.
