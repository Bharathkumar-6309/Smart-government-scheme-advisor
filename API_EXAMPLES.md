# API Examples - Curl and Postman

## 🚀 Quick API Testing

### Base URL
- **Development**: `http://localhost:8000`
- **Production**: `https://api.yourdomain.com`

## 📋 Health Check

### Curl
```bash
curl -X GET http://localhost:8000/api/health \
  -H "Accept: application/json"
```

### Postman
- **Method**: `GET`
- **URL**: `http://localhost:8000/api/health`
- **Headers**: `Accept: application/json`

### Expected Response
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

## 🔍 Scheme Search Examples

### Example 1: Basic Scholarship Search

#### Curl
```bash
curl -X POST http://localhost:8000/api/schemes/search \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
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
      "income_limit": 300000
    }
  }'
```

#### Postman
- **Method**: `POST`
- **URL**: `http://localhost:8000/api/schemes/search`
- **Headers**: 
  - `Content-Type: application/json`
  - `Accept: application/json`
- **Body** (raw JSON):
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
    "income_limit": 300000
  }
}
```

### Example 2: Housing Loan Search

#### Curl
```bash
curl -X POST http://localhost:8000/api/schemes/search \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "query": "housing loan subsidy for first time buyers",
    "user_profile": {
      "age": 35,
      "income": 600000,
      "occupation": "private employee",
      "education": "graduate",
      "state": "Maharashtra"
    },
    "filters": {
      "category": "housing",
      "state": "Maharashtra"
    }
  }'
```

#### Postman
- **Method**: `POST`
- **URL**: `http://localhost:8000/api/schemes/search`
- **Headers**: 
  - `Content-Type: application/json`
  - `Accept: application/json`
- **Body** (raw JSON):
```json
{
  "query": "housing loan subsidy for first time buyers",
  "user_profile": {
    "age": 35,
    "income": 600000,
    "occupation": "private employee",
    "education": "graduate",
    "state": "Maharashtra"
  },
  "filters": {
    "category": "housing",
    "state": "Maharashtra"
  }
}
```

### Example 3: Agriculture Scheme Search

#### Curl
```bash
curl -X POST http://localhost:8000/api/schemes/search \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "query": "financial assistance for farmers",
    "user_profile": {
      "age": 45,
      "income": 180000,
      "occupation": "farmer",
      "education": "high school",
      "state": "Uttar Pradesh"
    },
    "filters": {
      "category": "agriculture",
      "income_limit": 200000
    }
  }'
```

#### Postman
- **Method**: `POST`
- **URL**: `http://localhost:8000/api/schemes/search`
- **Headers**: 
  - `Content-Type: application/json`
  - `Accept: application/json`
- **Body** (raw JSON):
```json
{
  "query": "financial assistance for farmers",
  "user_profile": {
    "age": 45,
    "income": 180000,
    "occupation": "farmer",
    "education": "high school",
    "state": "Uttar Pradesh"
  },
  "filters": {
    "category": "agriculture",
    "income_limit": 200000
  }
}
```

## 🎯 Recommendation Examples

### Example 1: Student Profile

#### Curl
```bash
curl -X POST http://localhost:8000/api/schemes/recommend \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "user_profile": {
      "age": 21,
      "income": 250000,
      "occupation": "student",
      "education": "engineering",
      "state": "Karnataka"
    },
    "max_recommendations": 5
  }'
```

#### Postman
- **Method**: `POST`
- **URL**: `http://localhost:8000/api/schemes/recommend`
- **Headers**: 
  - `Content-Type: application/json`
  - `Accept: application/json`
- **Body** (raw JSON):
```json
{
  "user_profile": {
    "age": 21,
    "income": 250000,
    "occupation": "student",
    "education": "engineering",
    "state": "Karnataka"
  },
  "max_recommendations": 5
}
```

### Example 2: Working Professional

#### Curl
```bash
curl -X POST http://localhost:8000/api/schemes/recommend \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "user_profile": {
      "age": 32,
      "income": 800000,
      "occupation": "software engineer",
      "education": "bachelors",
      "state": "Delhi"
    },
    "max_recommendations": 3
  }'
```

#### Postman
- **Method**: `POST`
- **URL**: `http://localhost:8000/api/schemes/recommend`
- **Headers**: 
  - `Content-Type: application/json`
  - `Accept: application/json`
- **Body** (raw JSON):
```json
{
  "user_profile": {
    "age": 32,
    "income": 800000,
    "occupation": "software engineer",
    "education": "bachelors",
    "state": "Delhi"
  },
  "max_recommendations": 3
}
```

### Example 3: Senior Citizen

#### Curl
```bash
curl -X POST http://localhost:8000/api/schemes/recommend \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "user_profile": {
      "age": 65,
      "income": 300000,
      "occupation": "retired",
      "education": "graduate",
      "state": "Gujarat"
    },
    "max_recommendations": 4
  }'
```

#### Postman
- **Method**: `POST`
- **URL**: `http://localhost:8000/api/schemes/recommend`
- **Headers**: 
  - `Content-Type: application/json`
  - `Accept: application/json`
- **Body** (raw JSON):
```json
{
  "user_profile": {
    "age": 65,
    "income": 300000,
    "occupation": "retired",
    "education": "graduate",
    "state": "Gujarat"
  },
  "max_recommendations": 4
}
```

## ❌ Error Handling Examples

### Missing Query Error

#### Curl
```bash
curl -X POST http://localhost:8000/api/schemes/search \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "user_profile": {
      "age": 21,
      "income": 250000
    }
  }'
```

#### Expected Response
```json
{
  "message": "Validation error",
  "details": {
    "query": "Query is required"
  }
}
```

### Missing User Profile Error

#### Curl
```bash
curl -X POST http://localhost:8000/api/schemes/recommend \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "max_recommendations": 5
  }'
```

#### Expected Response
```json
{
  "message": "Validation error",
  "details": {
    "user_profile": "User profile is required"
  }
}
```

### Invalid Endpoint

#### Curl
```bash
curl -X GET http://localhost:8000/api/invalid \
  -H "Accept: application/json"
```

#### Expected Response
```json
{
  "message": "Endpoint not found",
  "details": {
    "path": "/api/invalid"
  }
}
```

## 📊 Postman Collection

### Import Collection

Create a new collection in Postman and import this JSON:

```json
{
  "info": {
    "name": "Smart Government Scheme Advisor API",
    "description": "API collection for testing government scheme search and recommendations",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "header": [
          {
            "key": "Accept",
            "value": "application/json"
          }
        ],
        "url": {
          "raw": "http://localhost:8000/api/health",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "health"]
        }
      }
    },
    {
      "name": "Scheme Search - Scholarship",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          },
          {
            "key": "Accept",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"query\": \"scholarship for engineering students\",\n  \"user_profile\": {\n    \"age\": 21,\n    \"income\": 250000,\n    \"occupation\": \"student\",\n    \"education\": \"engineering college\",\n    \"state\": \"Karnataka\"\n  },\n  \"filters\": {\n    \"category\": \"education\",\n    \"income_limit\": 300000\n  }\n}"
        },
        "url": {
          "raw": "http://localhost:8000/api/schemes/search",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "schemes", "search"]
        }
      }
    },
    {
      "name": "Scheme Search - Housing",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          },
          {
            "key": "Accept",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"query\": \"housing loan subsidy for first time buyers\",\n  \"user_profile\": {\n    \"age\": 35,\n    \"income\": 600000,\n    \"occupation\": \"private employee\",\n    \"education\": \"graduate\",\n    \"state\": \"Maharashtra\"\n  },\n  \"filters\": {\n    \"category\": \"housing\",\n    \"state\": \"Maharashtra\"\n  }\n}"
        },
        "url": {
          "raw": "http://localhost:8000/api/schemes/search",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "schemes", "search"]
        }
      }
    },
    {
      "name": "Scheme Search - Agriculture",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          },
          {
            "key": "Accept",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"query\": \"financial assistance for farmers\",\n  \"user_profile\": {\n    \"age\": 45,\n    \"income\": 180000,\n    \"occupation\": \"farmer\",\n    \"education\": \"high school\",\n    \"state\": \"Uttar Pradesh\"\n  },\n  \"filters\": {\n    \"category\": \"agriculture\",\n    \"income_limit\": 200000\n  }\n}"
        },
        "url": {
          "raw": "http://localhost:8000/api/schemes/search",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "schemes", "search"]
        }
      }
    },
    {
      "name": "Recommendations - Student",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          },
          {
            "key": "Accept",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"user_profile\": {\n    \"age\": 21,\n    \"income\": 250000,\n    \"occupation\": \"student\",\n    \"education\": \"engineering\",\n    \"state\": \"Karnataka\"\n  },\n  \"max_recommendations\": 5\n}"
        },
        "url": {
          "raw": "http://localhost:8000/api/schemes/recommend",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "schemes", "recommend"]
        }
      }
    },
    {
      "name": "Recommendations - Professional",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          },
          {
            "key": "Accept",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"user_profile\": {\n    \"age\": 32,\n    \"income\": 800000,\n    \"occupation\": \"software engineer\",\n    \"education\": \"bachelors\",\n    \"state\": \"Delhi\"\n  },\n  \"max_recommendations\": 3\n}"
        },
        "url": {
          "raw": "http://localhost:8000/api/schemes/recommend",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "schemes", "recommend"]
        }
      }
    },
    {
      "name": "Error Test - Missing Query",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          },
          {
            "key": "Accept",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"user_profile\": {\n    \"age\": 21,\n    \"income\": 250000\n  }\n}"
        },
        "url": {
          "raw": "http://localhost:8000/api/schemes/search",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "schemes", "search"]
        }
      }
    }
  ],
  "event": [
    {
      "listen": "prerequest",
      "script": {
        "type": "text/javascript",
        "exec": [
          "// Add timestamp to requests for debugging",
          "console.log('Request sent at: ' + new Date().toISOString());"
        ]
      }
    },
    {
      "listen": "test",
      "script": {
        "type": "text/javascript",
        "exec": [
          "// Basic response validation",
          "pm.test('Status code is 200', function () {",
          "    pm.response.to.have.status(200);",
          "});",
          "",
          "pm.test('Response has success field', function () {",
          "    const jsonData = pm.response.json();",
          "    pm.expect(jsonData).to.have.property('success');",
          "});",
          "",
          "pm.test('Response time is less than 2000ms', function () {",
          "    pm.expect(pm.response.responseTime).to.be.below(2000);",
          "});"
        ]
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000",
      "type": "string"
    }
  ]
}
```

## 🔧 Environment Variables

### Development
```bash
# Backend
export PORT=8000
export CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Frontend
export VITE_API_URL=http://localhost:8000
```

### Production
```bash
# Backend
export PORT=8000
export CORS_ORIGINS=https://yourdomain.com
export OPENAI_API_KEY=your_api_key_here

# Frontend
export VITE_API_URL=https://api.yourdomain.com
```

## 📝 Testing Script

### Bash Script for API Testing

```bash
#!/bin/bash
# api-test.sh

BASE_URL="http://localhost:8000"

echo "🚀 Testing Smart Government Scheme Advisor API"
echo "=============================================="

# Health Check
echo "1. Health Check"
curl -s -X GET "$BASE_URL/api/health" | jq '.'
echo ""

# Search Test
echo "2. Scheme Search - Scholarship"
curl -s -X POST "$BASE_URL/api/schemes/search" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "query": "scholarship for students",
    "user_profile": {
      "age": 21,
      "income": 250000,
      "occupation": "student",
      "state": "Karnataka"
    }
  }' | jq '.'
echo ""

# Recommendation Test
echo "3. Scheme Recommendations - Student"
curl -s -X POST "$BASE_URL/api/schemes/recommend" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "user_profile": {
      "age": 21,
      "income": 250000,
      "occupation": "student",
      "state": "Karnataka"
    },
    "max_recommendations": 3
  }' | jq '.'
echo ""

echo "✅ API Testing Complete!"
```

### PowerShell Script for API Testing

```powershell
# api-test.ps1

$BaseUrl = "http://localhost:8000"

Write-Host "🚀 Testing Smart Government Scheme Advisor API"
Write-Host "=============================================="

# Health Check
Write-Host "1. Health Check"
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/api/health" -Method Get
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Health check failed: $_"
}
Write-Host ""

# Search Test
Write-Host "2. Scheme Search - Scholarship"
try {
    $body = @{
        query = "scholarship for students"
        user_profile = @{
            age = 21
            income = 250000
            occupation = "student"
            state = "Karnataka"
        }
    } | ConvertTo-Json -Depth 10
    
    $response = Invoke-RestMethod -Uri "$BaseUrl/api/schemes/search" -Method Post -ContentType "application/json" -Body $body
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Search test failed: $_"
}
Write-Host ""

Write-Host "✅ API Testing Complete!"
```

## 📊 Response Analysis

### Successful Search Response Structure
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
      "benefits": "Financial assistance for education covering tuition fees",
      "documents_required": ["Aadhaar card", "Mark sheets"],
      "eligibility_criteria": ["Students from class 1 to post-graduation"],
      "state": "All India",
      "income_limit": 250000,
      "official_link": "https://scholarships.gov.in",
      "similarity_score": 0.92,
      "confidence_score": 0.88,
      "why_eligible": "Based on your student profile and income level",
      "application_steps": ["Register on scholarships.gov.in"]
    }
  ],
  "total_results": 3,
  "search_time": 0.001,
  "search_method": "rag_llm"
}
```

### Successful Recommendation Response Structure
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
      "benefits": "Financial assistance for education covering tuition fees",
      "documents_required": ["Aadhaar card", "Mark sheets"],
      "eligibility_criteria": ["Students from class 1 to post-graduation"],
      "state": "All India",
      "income_limit": 250000,
      "official_link": "https://scholarships.gov.in",
      "eligibility_score": 0.92,
      "benefit_score": 0.85,
      "overall_score": 0.88,
      "personalized_reasoning": "Based on your age and education level",
      "application_priority": "high",
      "next_steps": ["Gather required documents"],
      "recommendation_strength": "strong"
    }
  ],
  "total_recommendations": 5,
  "response_time": 0.002,
  "recommendation_method": "personalized"
}
```

## 🎯 Performance Testing

### Load Testing with Apache Bench
```bash
# Test search endpoint
ab -n 100 -c 10 -H "Content-Type: application/json" -p search.json http://localhost:8000/api/schemes/search

# Test recommendation endpoint
ab -n 50 -c 5 -H "Content-Type: application/json" -p recommend.json http://localhost:8000/api/schemes/recommend
```

### Stress Testing with Siege
```bash
# Create test data file
echo '{"query":"test","user_profile":{"age":25,"income":500000}}' > test.json

# Run stress test
siege -c 10 -r 100 -f test.json http://localhost:8000/api/schemes/search POST Content-Type:application/json
```

## 🔍 Debugging Tips

### Enable Verbose Logging
```bash
# Backend debug mode
curl -v -X POST http://localhost:8000/api/schemes/search \
  -H "Content-Type: application/json" \
  -d '{"query":"test"}'

# Include response headers
curl -i -X POST http://localhost:8000/api/schemes/search \
  -H "Content-Type: application/json" \
  -d '{"query":"test"}'
```

### Test Different Content Types
```bash
# Test with different content types
curl -X POST http://localhost:8000/api/schemes/search \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"query":"test"}'
```

## 📱 Mobile Testing

### Using Mobile Apps
- Use **Postman** mobile app
- Use **Insomnia** REST client
- Use **HTTPie** command-line tool

### HTTPie Examples
```bash
# Health check
http GET localhost:8000/api/health

# Search
http POST localhost:8000/api/schemes/search query="scholarship" user_profile:='{"age":21}'

# Recommendations
http POST localhost:8000/api/schemes/recommend user_profile:='{"age":21,"income":250000}'
```

## 🚨 Common Issues

### CORS Issues
```bash
# Add CORS headers
curl -X POST http://localhost:8000/api/schemes/search \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Origin: http://localhost:5173" \
  -d '{"query":"test"}'
```

### Timeout Issues
```bash
# Set timeout
curl --max-time 30 -X POST http://localhost:8000/api/schemes/search \
  -H "Content-Type: application/json" \
  -d '{"query":"test"}'
```

### Large Payload Issues
```bash
# Compress request
curl -X POST http://localhost:8000/api/schemes/search \
  -H "Content-Type: application/json" \
  -H "Content-Encoding: gzip" \
  --data-binary @request.json.gz
```

This comprehensive API testing guide provides everything needed to test and debug the Smart Government Scheme Advisor API endpoints.
