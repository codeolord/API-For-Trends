# API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Trends Endpoints

### List Trends
```
GET /trends
```

**Query Parameters:**
- `skip` (int, default: 0) - Pagination offset
- `limit` (int, default: 10, max: 100) - Results per page
- `niche` (string) - Filter by niche
- `category` (string) - Filter by category
- `min_score` (float) - Minimum overall score (0-100)

**Response:**
```json
[
  {
    "id": 1,
    "niche": "minimalist home decor",
    "category": "home-decor",
    "demand_score": 78.5,
    "competition_score": 45.2,
    "growth_score": 82.1,
    "profitability_score": 73.9,
    "overall_score": 74.93,
    "marketplace_counts": {
      "amazon": 150,
      "etsy": 200,
      "shopify": 50
    },
    "avg_price": 34.99,
    "price_range": {
      "min": 14.99,
      "max": 99.99
    },
    "total_reviews": 5430,
    "avg_rating": 4.6,
    "target_audience": {
      "primary_categories": [
        ["home-decor", 400],
        ["gifts", 150],
        ["art", 100]
      ],
      "price_sensitivity": "mid",
      "avg_price": 34.99
    },
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-16T14:20:00Z"
  }
]
```

### Get Trend Details
```
GET /trends/{trend_id}
```

**Response:** Single trend object (same structure as list)

### Create Trend
```
POST /trends
Content-Type: application/json

{
  "niche": "vintage band t-shirts",
  "category": "apparel",
  "demand_score": 85.0,
  "competition_score": 65.0,
  "growth_score": 78.0,
  "profitability_score": 70.0,
  "overall_score": 74.5,
  "marketplace_counts": {"amazon": 100, "etsy": 150},
  "avg_price": 24.99,
  "price_range": {"min": 12.99, "max": 49.99},
  "total_reviews": 3000,
  "avg_rating": 4.5,
  "target_audience": {...},
  "style_patterns": [...],
  "summary": "Trend description"
}
```

## Products Endpoints

### List Products
```
GET /products
```

**Query Parameters:**
- `skip` (int, default: 0)
- `limit` (int, default: 20, max: 100)
- `marketplace` (string) - Filter by amazon/etsy/shopify
- `category` (string) - Filter by category
- `min_rating` (float) - Minimum rating

**Response:**
```json
[
  {
    "id": 1,
    "marketplace": "amazon",
    "external_id": "B123ABC456",
    "title": "Product Title",
    "description": "Product description",
    "category": "Home Decor",
    "price": 29.99,
    "rating": 4.6,
    "reviews_count": 245,
    "sales_count": 1200,
    "image_url": "https://...",
    "product_url": "https://...",
    "tags": ["tag1", "tag2"],
    "keywords": ["keyword1", "keyword2"],
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z",
    "trend_id": 1
  }
]
```

### Get Product
```
GET /products/{product_id}
```

### Create Product
```
POST /products
Content-Type: application/json

{
  "marketplace": "etsy",
  "external_id": "123456789",
  "title": "Product Title",
  "description": "Description",
  "category": "Home Decor",
  "price": 24.99,
  "rating": 4.8,
  "reviews_count": 150,
  "image_url": "https://...",
  "product_url": "https://...",
  "tags": ["tag1", "tag2"],
  "keywords": ["keyword1"]
}
```

## Designs Endpoints

### List Designs
```
GET /designs
```

**Query Parameters:**
- `skip` (int, default: 0)
- `limit` (int, default: 20, max: 100)
- `trend_id` (int) - Filter by trend
- `status` (string) - Filter by draft/ready/published

**Response:**
```json
[
  {
    "id": 1,
    "trend_id": 1,
    "title": "Design Title",
    "description": "Design description",
    "design_prompt": "Modern minimalist design with clean lines",
    "design_metadata": {
      "colors": ["#FF6B6B", "#4ECDC4"],
      "style": "modern",
      "elements": ["geometric", "minimalist"]
    },
    "image_url": "https://...",
    "mockup_urls": ["https://...", "https://..."],
    "print_specifications": {
      "size": "A4",
      "colors": "4C",
      "material": "100% cotton"
    },
    "status": "draft",
    "printful_template_id": null,
    "created_at": "2024-01-16T10:00:00Z",
    "updated_at": "2024-01-16T10:00:00Z"
  }
]
```

### Get Design
```
GET /designs/{design_id}
```

### Create Design
```
POST /designs
Content-Type: application/json

{
  "trend_id": 1,
  "title": "Design Title",
  "description": "Description",
  "design_prompt": "Design prompt for AI generation",
  "design_metadata": {
    "colors": ["#FF6B6B"],
    "style": "modern"
  },
  "image_url": "https://...",
  "mockup_urls": ["https://..."],
  "print_specifications": {
    "size": "A4",
    "colors": "4C",
    "material": "100% cotton"
  }
}
```

## Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "environment": "development"
}
```

## Error Responses

### 404 Not Found
```json
{
  "detail": "Trend not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "niche"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Rate Limiting
Currently no rate limiting. Will be implemented in production.

## Authentication
Currently no authentication required. Will be added in Phase 4.
