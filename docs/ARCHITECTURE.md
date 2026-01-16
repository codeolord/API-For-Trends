# System Architecture

## Overview

The POD Trends Platform is built as a modern, scalable system with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│              User Interface Layer (Frontend)                 │
│         Next.js Dashboard, Analytics, Publishing            │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API (JSON)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              API Layer (FastAPI Backend)                    │
│  Trends │ Products │ Designs │ Jobs │ Health Check        │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
    ┌────────┐      ┌──────────┐    ┌──────────┐
    │Database│      │Cache/Job │    │Workers   │
    │(PG)    │      │Broker    │    │(Celery)  │
    │        │      │(Redis)   │    │          │
    └────────┘      └──────────┘    └──────────┘
        │                │                │
        │                │                │
    Tables:         Key-Value Store:    Tasks:
    - Products      - User Sessions     - Scrape
    - Trends        - Job Queues        - Analyze
    - Designs       - Caches            - Generate
    - Marketplaces                      - Publish
```

## Layer Breakdown

### 1. Data Collection Layer (Scrapers)

**Purpose**: Continuously collect product data from marketplaces

**Components**:
- `BaseScraper`: Abstract base class for all scrapers
- `AmazonScraper`: Amazon product scraper
- `EtsyScraper`: Etsy product scraper
- `ShopifyScraper`: Shopify store scraper

**Process**:
1. Scheduled task triggers periodically (e.g., every 6 hours)
2. Scraper fetches product listings from marketplace
3. Data normalized to standard Product schema
4. Stored in PostgreSQL with metadata
5. Raw JSON preserved for future analysis

### 2. Analysis Layer

**Purpose**: Extract insights and score trends from raw product data

**Components**:
- `calculate_trend_scores()`: Multi-factor scoring algorithm
- `infer_audience()`: Demographic inference
- `analyze_trends()`: Grouping and trend creation

**Scoring Formula**:
```
Overall Score = 
  (Demand × 0.25) + 
  (Growth × 0.25) + 
  ((100 - Competition) × 0.25) + 
  (Profitability × 0.25)
```

**Demand** = (review_count / 10) + (rating × 5)
**Growth** = (avg_rating × 20) + 10
**Competition** = min(product_count, 100)
**Profitability** = (avg_price / 50 × 50) + (avg_rating × 10)

### 3. Design Generation Layer

**Purpose**: Create original, print-ready designs from trend insights

**Components**:
- `DesignGenerator`: Orchestrates design creation
- `_create_design_prompt()`: Generates AI prompts
- `generate_image()`: Calls image generation API
- `create_mockups()`: Creates product mockups

**Process**:
1. Trend data and insights fed to LLM
2. AI generates 3 design variants per trend
3. Image generation creates visual assets
4. Mockups created for different products
5. Designs stored with print specifications

### 4. Integration Layer

**Purpose**: Connect to external print-on-demand platforms

**Components**:
- `PrintfulClient`: Printful API integration
- `ShopifyClient`: Shopify store integration

**Features**:
- Create products in Printful
- Publish drafts to Shopify
- Sync variants and pricing
- Manage product fulfillment

### 5. API Layer

**Purpose**: RESTful interface for frontend and external integrations

**Endpoints**:
- `/api/v1/trends` - Trend management
- `/api/v1/products` - Product management
- `/api/v1/designs` - Design management

**Features**:
- Input validation with Pydantic
- Error handling and logging
- Pagination and filtering
- CORS support

### 6. Frontend Layer

**Purpose**: User interface for exploration and decision-making

**Pages**:
- **Home**: Platform overview and CTA
- **Trends**: Interactive trend exploration
- **Designs**: Design gallery and publishing
- **Products**: Scraped product browser

**State Management**:
- Zustand for global state
- React hooks for component state
- API client for backend communication

## Data Flow

### Marketplace Data Collection
```
1. Scheduled Task (Celery Beat)
2. → Trigger scrape_marketplace task
3. → Scraper fetches marketplace data
4. → Normalize to Product schema
5. → Store in PostgreSQL
6. → Cache in Redis
```

### Trend Analysis
```
1. Scheduled Task (Celery Beat)
2. → Trigger analyze_trends_task
3. → Group products by category
4. → Calculate scores
5. → Infer target audience
6. → Create/update Trend records
7. → Invalidate cache
```

### Design Generation
```
1. User clicks "Generate Designs"
2. → Frontend sends trend_id
3. → API triggers generate_designs_task
4. → AI generates 3 design variants
5. → Create image assets
6. → Generate mockups
7. → Store designs in DB
8. → Frontend polls for completion
```

### Product Publishing
```
1. User selects design for publishing
2. → API calls Printful integration
3. → Creates product with variants
4. → Calls Shopify integration
5. → Creates draft product
6. → Updates design status
7. → Returns URLs to user
```

## Database Schema

### Products Table
```
products
├── id (PK)
├── marketplace (STRING, INDEX)
├── external_id (STRING, UNIQUE)
├── title, description, category
├── price, rating, reviews_count
├── image_url, product_url
├── tags, keywords (JSON)
├── raw_data (JSON)
├── trend_id (FK)
├── created_at (INDEX)
└── updated_at
```

### Trends Table
```
trends
├── id (PK)
├── niche, category (INDEX)
├── demand_score, competition_score
├── growth_score, profitability_score
├── overall_score (INDEX)
├── marketplace_counts (JSON)
├── avg_price, price_range (JSON)
├── target_audience (JSON)
├── style_patterns (JSON)
├── created_at (INDEX)
└── updated_at
```

### Designs Table
```
designs
├── id (PK)
├── trend_id (FK, INDEX)
├── title, description
├── design_prompt
├── design_metadata (JSON)
├── image_url
├── mockup_urls (JSON)
├── print_specifications (JSON)
├── status (draft/ready/published)
├── printful_template_id
├── created_at (INDEX)
└── updated_at
```

### Marketplaces Table
```
marketplaces
├── id (PK)
├── name (STRING, UNIQUE)
├── last_scraped
├── next_scrape
├── status
├── error_message
├── created_at
└── updated_at
```

## Deployment Architecture

### Development
- Docker Compose for local full-stack
- Hot reloading for frontend and backend
- PostgreSQL and Redis in containers

### Production
```
Frontend:        Next.js → Vercel (auto-deploy from main)
Backend:         FastAPI → Cloud Run / Railway
Database:        PostgreSQL → Cloud SQL / RDS
Cache:           Redis → Cloud Memorystore / Elasticache
Task Queue:      Celery Workers → Cloud Run / ECS
Storage:         Cloud Storage for images
```

## Performance Considerations

1. **Database Indexing**
   - Index on marketplace + category
   - Index on overall_score for quick sorting
   - Index on created_at for time-based queries

2. **Caching Strategy**
   - Redis for session data
   - Redis for job queue
   - ETags for API responses

3. **Async Processing**
   - Scraping in background
   - Analysis in background
   - Design generation in background

4. **Rate Limiting**
   - Per-IP rate limits (to be implemented)
   - API key limits for integrations

## Security Considerations

1. **API Security**
   - Input validation on all endpoints
   - SQL injection prevention (ORM)
   - CORS configuration
   - API key management for external services

2. **Data Protection**
   - Environment variables for secrets
   - Database encryption at rest
   - HTTPS in production

3. **Authentication** (Phase 4)
   - JWT tokens
   - User role-based access
   - API key management

## Scaling Strategy

1. **Horizontal Scaling**
   - Stateless API servers
   - Load balancer in front
   - Multiple Celery workers

2. **Database Scaling**
   - Read replicas for analytics
   - Connection pooling
   - Partitioning for large tables

3. **Caching Layer**
   - Redis cluster for high availability
   - Cache warming strategies

## Monitoring & Logging

1. **Application Metrics**
   - Request latency
   - Error rates
   - Task completion times

2. **System Metrics**
   - CPU, Memory usage
   - Database connection pool
   - Redis memory usage

3. **Logging**
   - Structured JSON logs
   - Log aggregation (ELK, Datadog, etc.)
   - Error tracking (Sentry)
