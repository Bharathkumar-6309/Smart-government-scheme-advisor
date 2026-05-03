# API Documentation

## Overview

The Smart Government Scheme Advisor provides RESTful APIs for searching and recommending government schemes based on user profiles and preferences.

## Base URL

```
Development: http://localhost:8000
Production: https://your-domain.com
```

## Authentication

Currently, the API does not require authentication. In production, API keys or JWT tokens may be implemented.

## Common Headers

```http
Content-Type: application/json
Accept: application/json
Access-Control-Allow-Origin: *
```

## Error Handling

All API endpoints return consistent error responses:

```json
{
  "message": "Error description",
  "details": {
    "field": "specific error details"
  }
}
```

### HTTP Status Codes

- `200` - Success
- `400` - Bad Request (validation errors)
- `404` - Not Found
- `500` - Internal Server Error

## Endpoints

### Health Check

Check the health status of the API and its services.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-05-02T23:30:00.000Z",
  "app": "Smart Government Scheme Advisor",
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "rag_system": "operational",
    "llm_service": "mock_mode"
  }
}
```

### Scheme Search

Search for government schemes based on query, user profile, and filters.

**Endpoint:** `POST /api/schemes/search`

**Request Body:**
```json
{
  "query": "scholarship for engineering students",
  "user_profile": {
    "age": 21,
    "income": 250000,
    "occupation": "student",
    "education": "engineering college",
    "state": "Karnataka"
  },
  "filters": {
    "category": "education",
    "state": "Karnataka",
    "income_limit": 300000
  }
}
```

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | Search query for schemes |
| user_profile | object | No | User demographic information |
| filters | object | No | Filtering criteria |

#### User Profile Fields

| Field | Type | Description |
|-------|------|-------------|
| age | integer | User age (1-100) |
| income | integer | Annual income in INR |
| occupation | string | User occupation |
| education | string | Education level |
| state | string | User state |

#### Filter Fields

| Field | Type | Description |
|-------|------|-------------|
| category | string | Scheme category |
| state | string | Scheme availability state |
| income_limit | integer | Maximum income eligibility |

#### Response

```json
{
  "success": true,
  "message": "Found 3 relevant schemes",
  "data": [
    {
      "id": "scheme_001",
      "name": "National Scholarship Portal",
      "category": "education",
      "description": "Centralized platform for various scholarship schemes",
      "benefits": "Financial assistance for education covering tuition fees and maintenance allowances",
      "documents_required": ["Aadhaar card", "Mark sheets", "Income certificate", "Bank account details"],
      "eligibility_criteria": ["Students from class 1 to post-graduation", "Minimum 50 marks in previous examination"],
      "state": "All India",
      "income_limit": 250000,
      "official_link": "https://scholarships.gov.in",
      "similarity_score": 0.92,
      "confidence_score": 0.88,
      "why_eligible": "Based on your student profile and income level, you meet the eligibility criteria...",
      "application_steps": ["Register on scholarships.gov.in", "Complete your profile", "Upload documents"]
    }
  ],
  "total_results": 3,
  "search_time": 0.001,
  "search_method": "rag_llm",
  "filters_applied": {
    "category": "education",
    "state": "Karnataka",
    "income_limit": 300000
  }
}
```

### Scheme Recommendations

Get personalized scheme recommendations based on user profile.

**Endpoint:** `POST /api/schemes/recommend`

**Request Body:**
```json
{
  "user_profile": {
    "age": 25,
    "income": 400000,
    "occupation": "private employee",
    "education": "graduate",
    "state": "Delhi"
  },
  "max_recommendations": 5
}
```

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_profile | object | Yes | User demographic information |
| max_recommendations | integer | No | Maximum recommendations (default: 5) |

#### Response

```json
{
  "success": true,
  "message": "Generated 5 personalized recommendations",
  "recommendations": [
    {
      "id": "scheme_001",
      "name": "National Scholarship Portal",
      "category": "education",
      "description": "Centralized platform for various scholarship schemes",
      "benefits": "Financial assistance for education covering tuition fees and maintenance allowances",
      "documents_required": ["Aadhaar card", "Mark sheets", "Income certificate", "Bank account details"],
      "eligibility_criteria": ["Students from class 1 to post-graduation", "Minimum 50 marks in previous examination"],
      "state": "All India",
      "income_limit": 250000,
      "official_link": "https://scholarships.gov.in",
      "eligibility_score": 0.92,
      "benefit_score": 0.85,
      "overall_score": 0.88,
      "personalized_reasoning": "Based on your age and education level, this scholarship portal offers multiple schemes...",
      "application_priority": "high",
      "next_steps": ["Gather required documents", "Visit official website", "Check deadlines"],
      "recommendation_strength": "strong"
    }
  ],
  "total_recommendations": 5,
  "response_time": 0.002,
  "recommendation_method": "personalized"
}
```

## Scheme Categories

Available scheme categories for filtering:

- `agriculture` - Farming and rural development schemes
- `education` - Scholarships and educational support
- `energy` - Energy and fuel subsidies
- `financial_inclusion` - Banking and financial services
- `healthcare` - Medical and health insurance schemes
- `housing` - Housing and construction assistance
- `skill_development` - Training and skill programs
- `women_empowerment` - Women-focused schemes

## States

All Indian states and union territories are supported for filtering:

- `All India` - Nationwide schemes
- Individual states: `Andhra Pradesh`, `Arunachal Pradesh`, `Assam`, `Bihar`, `Chhattisgarh`, `Goa`, `Gujarat`, `Haryana`, `Himachal Pradesh`, `Jharkhand`, `Karnataka`, `Kerala`, `Madhya Pradesh`, `Maharashtra`, `Manipur`, `Meghalaya`, `Mizoram`, `Nagaland`, `Odisha`, `Punjab`, `Rajasthan`, `Sikkim`, `Tamil Nadu`, `Telangana`, `Tripura`, `Uttar Pradesh`, `Uttarakhand`, `West Bengal`

## Response Fields

### Common Scheme Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique scheme identifier |
| name | string | Scheme name |
| category | string | Scheme category |
| description | string | Detailed description |
| benefits | string | Benefits description |
| documents_required | array | List of required documents |
| eligibility_criteria | array | Eligibility requirements |
| state | string | Scheme availability |
| income_limit | integer | Maximum income eligibility |
| official_link | string | Official website URL |

### Search-Specific Fields

| Field | Type | Description |
|-------|------|-------------|
| similarity_score | float | Vector similarity score (0-1) |
| confidence_score | float | LLM confidence score (0-1) |
| why_eligible | string | Personalized eligibility explanation |
| application_steps | array | Step-by-step application process |

### Recommendation-Specific Fields

| Field | Type | Description |
|-------|------|-------------|
| eligibility_score | float | Eligibility match score (0-1) |
| benefit_score | float | Benefit alignment score (0-1) |
| overall_score | float | Combined recommendation score (0-1) |
| personalized_reasoning | string | Custom recommendation explanation |
| application_priority | string | Priority level (high/medium/low) |
| next_steps | array | Actionable next steps |
| recommendation_strength | string | Strength level (strong/moderate/weak) |

## Rate Limiting

Currently, no rate limiting is implemented. In production, rate limiting may be added:
- 100 requests per minute per IP
- 1000 requests per hour per user

## SDKs and Libraries

### JavaScript/TypeScript

```typescript
interface SchemeSearchRequest {
  query: string;
  user_profile?: UserProfile;
  filters?: Filters;
}

interface SchemeSearchResponse {
  success: boolean;
  data: Scheme[];
  total_results: number;
  search_time: number;
}

// Example usage
const searchSchemes = async (request: SchemeSearchRequest): Promise<SchemeSearchResponse> => {
  const response = await fetch('http://localhost:8000/api/schemes/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request)
  });
  
  return response.json();
};
```

### Python

```python
import requests

def search_schemes(query: str, user_profile: dict = None, filters: dict = None) -> dict:
    """Search for government schemes"""
    url = "http://localhost:8000/api/schemes/search"
    payload = {
        "query": query,
        "user_profile": user_profile,
        "filters": filters
    }
    
    response = requests.post(url, json=payload)
    return response.json()

# Example usage
result = search_schemes(
    query="scholarship for students",
    user_profile={"age": 21, "income": 250000, "state": "Karnataka"},
    filters={"category": "education"}
)
```

## Error Examples

### Validation Error (400)

```json
{
  "message": "Validation error",
  "details": {
    "query": "Query is required"
  }
}
```

### Not Found Error (404)

```json
{
  "message": "Endpoint not found",
  "details": {
    "path": "/api/invalid"
  }
}
```

### Server Error (500)

```json
{
  "message": "Internal server error",
  "details": {
    "error": "Failed to process request"
  }
}
```

## Testing

### cURL Examples

```bash
# Health check
curl -X GET http://localhost:8000/api/health

# Search schemes
curl -X POST http://localhost:8000/api/schemes/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "scholarship for students",
    "user_profile": {"age": 21, "income": 250000},
    "filters": {"category": "education"}
  }'

# Get recommendations
curl -X POST http://localhost:8000/api/schemes/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "user_profile": {"age": 25, "income": 400000, "state": "Delhi"},
    "max_recommendations": 3
  }'
```

### Postman Collection

Import the following collection for Postman testing:

```json
{
  "info": {
    "name": "Smart Government Scheme Advisor API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "url": "http://localhost:8000/api/health"
      }
    },
    {
      "name": "Search Schemes",
      "request": {
        "method": "POST",
        "url": "http://localhost:8000/api/schemes/search",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"query\": \"scholarship for students\",\n  \"user_profile\": {\n    \"age\": 21,\n    \"income\": 250000\n  },\n  \"filters\": {\n    \"category\": \"education\"\n  }\n}"
        }
      }
    }
  ]
}
```
