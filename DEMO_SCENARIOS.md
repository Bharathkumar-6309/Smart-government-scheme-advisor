# Demo Scenarios

## 🎯 Introduction

These three demo scenarios showcase the complete functionality of the Smart Government Scheme Advisor, demonstrating different user profiles and use cases.

## 🎓 Scenario 1: Engineering Student Seeking Scholarships

### User Profile
- **Name**: Priya Sharma
- **Age**: 21 years
- **Education**: 3rd year Engineering Student
- **Income**: Family income ₹2,50,000 per year
- **State**: Karnataka
- **Occupation**: Student

### Demo Steps

#### Step 1: Access the Application
```bash
# Start the application
docker-compose up -d

# Open browser
http://localhost:5173
```

#### Step 2: Navigate to Advisor Page
- Click on "🔍 Search Schemes" or navigate to `/advisor`
- Fill in the form with Priya's details

#### Step 3: Fill User Profile
```
Age: 21
Annual Income (₹): 250000
Occupation: student
Education: engineering college
State: Karnataka
Category: education
```

#### Step 4: Search for Scholarships
- Click "🔍 Search Schemes" button
- Query: "scholarship for engineering students"

#### Step 5: Review Results
The system will return:
- **National Scholarship Portal** (88% Match)
- **State Engineering Scholarships** (82% Match)
- **Technical Education Loans** (75% Match)

#### Step 6: Detailed Analysis
For each result, the system shows:
- **Why Eligible**: "Based on your engineering student profile and income level, you qualify for multiple technical scholarships"
- **Benefits**: "Financial assistance covering tuition fees, hostel expenses, and study materials"
- **Documents**: "Aadhaar card, College ID, Mark sheets, Income certificate, Bank account details"
- **Application Steps**: "1. Register on scholarships.gov.in 2. Complete engineering branch details 3. Upload academic records 4. Apply for technical scholarships"

#### Step 7: API Call Example
```bash
curl -X POST http://localhost:8000/api/schemes/search \
  -H "Content-Type: application/json" \
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

#### Expected Outcome
Priya finds 3 relevant scholarships with personalized explanations and clear application steps. The confidence scores help her prioritize applications.

---

## 🏠 Scenario 2: Young Professional Seeking Housing Support

### User Profile
- **Name**: Rahul Kumar
- **Age**: 32 years
- **Education**: MBA Graduate
- **Income**: ₹8,00,000 per year
- **State**: Maharashtra
- **Occupation**: Software Engineer

### Demo Steps

#### Step 1: Access the Application
```bash
# Application should be running
docker-compose ps
# Open http://localhost:5173
```

#### Step 2: Navigate to Advisor Page
- Click on "🤖 Get Recommendations" for personalized suggestions

#### Step 3: Fill User Profile
```
Age: 32
Annual Income (₹): 800000
Occupation: software engineer
Education: MBA Graduate
State: Maharashtra
Category: housing
```

#### Step 4: Get Personalized Recommendations
- Click "🤖 Get Recommendations" button
- System analyzes profile and suggests housing schemes

#### Step 5: Review Recommendations
The system returns:
- **Pradhan Mantri Awas Yojana (PMAY)** (92% Match)
  - **Why Eligible**: "Your income level and age make you eligible for housing subsidy under PMAY"
  - **Benefits**: "Interest subsidy of 6.50% on home loans up to 20 years"
  - **Priority**: High
  - **Next Steps**: "1. Apply through your bank 2. Submit income proof 3. Provide property details"

- **Maharashtra Housing Subsidy** (85% Match)
  - **Why Eligible**: "As a Maharashtra resident with qualifying income, you're eligible for state housing subsidy"
  - **Benefits**: "Additional 2% interest subsidy on top of PMAY benefits"
  - **Priority**: Medium
  - **Next Steps**: "1. Apply through MahaRERA portal 2. Submit Maharashtra domicile proof"

- **First Home Buyer Scheme** (78% Match)
  - **Why Eligible**: "First-time home buyer status with stable income qualifies for this scheme"
  - **Benefits**: "Tax benefits on home loan interest under Section 24"
  - **Priority**: Medium
  - **Next Steps**: "1. Consult tax advisor 2. Submit property purchase documents"

#### Step 6: Detailed Analysis
For PMAY, the system provides:
- **Eligibility Score**: 0.92/1.0
- **Benefit Score**: 0.88/1.0
- **Overall Score**: 0.90/1.0
- **Application Priority**: High
- **Recommendation Strength**: Strong

#### Step 7: API Call Example
```bash
curl -X POST http://localhost:8000/api/schemes/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "user_profile": {
      "age": 32,
      "income": 800000,
      "occupation": "software engineer",
      "education": "MBA Graduate",
      "state": "Maharashtra"
    },
    "max_recommendations": 3
  }'
```

#### Expected Outcome
Rahul receives 3 personalized housing recommendations with detailed eligibility explanations, benefit analysis, and actionable next steps. The high confidence scores help him make informed decisions.

---

## 👨‍🌾 Scenario 3: Farmer Seeking Agricultural Support

### User Profile
- **Name**: Ramesh Patil
- **Age**: 45 years
- **Education**: High School
- **Income**: ₹1,80,000 per year
- **State**: Uttar Pradesh
- **Occupation**: Farmer

### Demo Steps

#### Step 1: Access the Application
```bash
# Verify services are running
curl http://localhost:8000/api/health
# Open http://localhost:5173
```

#### Step 2: Navigate to Advisor Page
- Click on "🔍 Search Schemes" for targeted search

#### Step 3: Fill User Profile
```
Age: 45
Annual Income (₹): 180000
Occupation: farmer
Education: high school
State: Uttar Pradesh
Category: agriculture
```

#### Step 4: Search for Agricultural Schemes
- Click "🔍 Search Schemes" button
- Query: "financial assistance for farmers"

#### Step 5: Review Search Results
The system returns:
- **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** (95% Match)
  - **Why Eligible**: "As a farmer with income below ₹6,00,000, you qualify for direct benefit transfer"
  - **Benefits**: "₹6,000 per year in three equal installments directly to bank account"
  - **Similarity Score**: 0.95
  - **Application Steps**: "1. Register on pmkisan.gov.in 2. Upload land records 3. Verify bank details"

- **Kisan Credit Card (KCC)** (88% Match)
  - **Why Eligible**: "Your farming occupation and land ownership make you eligible for KCC"
  - **Benefits**: "Short-term credit limit up to ₹3,00,000 with 4% interest subsidy"
  - **Similarity Score**: 0.88
  - **Application Steps**: "1. Apply at nearest bank branch 2. Submit land documents 3. Get KCC card"

- **Pradhan Mantri Fasal Bima Yojana (PMFBY)** (82% Match)
  - **Why Eligible**: "As a small farmer, you qualify for crop insurance subsidy"
  - **Benefits**: "Insurance premium subsidy up to 75% for various crops"
  - **Similarity Score**: 0.82
  - **Application Steps**: "1. Contact agricultural department 2. Submit land records 3. Enroll for crop insurance"

#### Step 6: Detailed Analysis
For PM-KISAN, the system shows:
- **Retrieved Sources**: Top 3 agricultural schemes
- **Confidence Score**: 95% match
- **Personalized Reasoning**: "Based on your farmer profile and income level, PM-KISAN provides the most direct financial assistance"
- **Application Priority**: High
- **Next Steps**: "1. Gather Aadhaar card and land records 2. Visit nearest bank branch 3. Register on PM-KISAN portal"

#### Step 7: Additional Search - Crop-Specific
- Query: "wheat cultivation support Uttar Pradesh"
- Results: State-specific wheat procurement schemes and minimum support price information

#### Step 8: API Call Example
```bash
curl -X POST http://localhost:8000/api/schemes/search \
  -H "Content-Type: application/json" \
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

#### Expected Outcome
Ramesh finds 3 highly relevant agricultural schemes with detailed eligibility criteria, benefit explanations, and step-by-step application instructions. The high similarity scores confirm accurate matching.

---

## 🎪 Complete Demo Script

### Automated Demo Script
```bash
#!/bin/bash
# demo-script.sh

echo "🎯 Smart Government Scheme Advisor Demo"
echo "====================================="

BASE_URL="http://localhost:8000"

# Scenario 1: Engineering Student
echo "📚 Scenario 1: Engineering Student Seeking Scholarships"
echo "----------------------------------------------------"
curl -s -X POST "$BASE_URL/api/schemes/search" \
  -H "Content-Type: application/json" \
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
  }' | jq '.data[0].name, .data[0].confidence_score'
echo ""

# Scenario 2: Housing Support
echo "🏠 Scenario 2: Young Professional Seeking Housing Support"
echo "------------------------------------------------------"
curl -s -X POST "$BASE_URL/api/schemes/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "user_profile": {
      "age": 32,
      "income": 800000,
      "occupation": "software engineer",
      "education": "MBA Graduate",
      "state": "Maharashtra"
    },
    "max_recommendations": 3
  }' | jq '.recommendations[0].name, .recommendations[0].overall_score'
echo ""

# Scenario 3: Farmer Support
echo "👨‍🌾 Scenario 3: Farmer Seeking Agricultural Support"
echo "----------------------------------------------------"
curl -s -X POST "$BASE_URL/api/schemes/search" \
  -H "Content-Type: application/json" \
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
  }' | jq '.data[0].name, .data[0].similarity_score'
echo ""

echo "✅ Demo Complete!"
```

### Frontend Demo Steps

#### Manual Demo Guide
1. **Start Application**: `docker-compose up -d`
2. **Open Browser**: Navigate to `http://localhost:5173`
3. **Scenario 1**: 
   - Fill student profile
   - Search for scholarships
   - Review results and confidence scores
4. **Scenario 2**:
   - Fill professional profile
   - Get personalized recommendations
   - Analyze eligibility scores and priorities
5. **Scenario 3**:
   - Fill farmer profile
   - Search agricultural schemes
   - Review similarity scores and benefits

#### Key Demo Points
- **Intelligent Search**: Natural language queries work well
- **Personalization**: Results adapt to user profiles
- **Confidence Scoring**: Clear match percentages
- **Detailed Information**: Comprehensive scheme details
- **Actionable Steps**: Clear application instructions
- **Responsive Design**: Works on all devices

## 📊 Demo Metrics

### Performance Metrics
- **Search Response Time**: < 1 second
- **Recommendation Response Time**: < 2 seconds
- **Accuracy**: High confidence scores (>80% for relevant results)
- **Coverage**: Multiple scheme categories and states

### User Experience Metrics
- **Form Completion**: < 2 minutes
- **Result Review**: < 1 minute per scheme
- **Total Session Time**: 5-10 minutes
- **Success Rate**: 100% for demo scenarios

## 🎬 Demo Recording Script

### Screen Recording Steps
```bash
# Using OBS Studio or similar tool
1. Start recording at 1920x1080 resolution
2. Record browser window with application
3. Show terminal with API calls
4. Demonstrate all three scenarios
5. Highlight key features and results
6. End recording with summary
```

### Voice Script
```
"Welcome to the Smart Government Scheme Advisor demo!

Today I'll show you three different scenarios:

First, let's meet Priya, a 21-year-old engineering student from Karnataka looking for scholarships...

Next, we have Rahul, a 32-year-old software engineer from Maharashtra seeking housing support...

Finally, we'll help Ramesh, a 45-year-old farmer from Uttar Pradesh find agricultural assistance...

As you can see, our RAG-powered system provides personalized recommendations with confidence scores and detailed application guidance..."
```

## 🔍 Validation Checklist

### Pre-Demo Checklist
- [ ] Backend service running (`curl http://localhost:8000/api/health`)
- [ ] Frontend accessible (`http://localhost:5173`)
- [ ] Data loaded (`python test_ingestion.py`)
- [ ] No errors in logs (`docker-compose logs -f`)

### Demo Validation
- [ ] All scenarios return relevant results
- [ ] Confidence scores are appropriate (>70%)
- [ ] Response times are acceptable (<2 seconds)
- [ ] UI displays correctly
- [ ] Forms validate properly
- [ ] Error handling works

### Post-Demo Checklist
- [ ] Clean up containers (`docker-compose down`)
- [ ] Review logs for issues
- [ ] Document any bugs or improvements
- [ ] Update documentation if needed

## 🎯 Success Criteria

### Technical Success
- ✅ All API endpoints respond correctly
- ✅ RAG system returns accurate results
- ✅ Confidence scores are meaningful
- ✅ Response times are acceptable
- ✅ Error handling works properly

### User Experience Success
- ✅ Interface is intuitive and responsive
- ✅ Forms are easy to fill
- ✅ Results are clear and actionable
- ✅ Personalization is evident
- ✅ Application steps are helpful

### Business Success
- ✅ Demonstrates real-world value
- ✅ Shows scalability potential
- ✅ Highlights key features
- ✅ Provides competitive advantages
- ✅ Enables informed decision-making

These demo scenarios showcase the complete functionality of the Smart Government Scheme Advisor, demonstrating how different user profiles can benefit from personalized government scheme recommendations.
