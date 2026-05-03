// Test script to verify frontend-backend connection
// Run this in browser console or as a separate test

async function testBackendConnection() {
  console.log('Testing backend connection...');
  
  try {
    // Test health endpoint
    const healthResponse = await fetch('http://localhost:8000/api/health');
    const healthData = await healthResponse.json();
    console.log('Health check:', healthData);
    
    // Test search endpoint with sample data
    const searchResponse = await fetch('http://localhost:8000/api/schemes/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        query: 'scholarship for students',
        user_profile: {
          age: 21,
          income: 250000,
          occupation: 'student',
          education: 'engineering',
          state: 'Karnataka'
        },
        filters: {
          category: 'education',
          income_limit: 300000
        }
      })
    });
    
    const searchData = await searchResponse.json();
    console.log('Search response:', searchData);
    
    // Test recommendation endpoint
    const recommendResponse = await fetch('http://localhost:8000/api/schemes/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        user_profile: {
          age: 25,
          income: 400000,
          occupation: 'private employee',
          education: 'graduate',
          state: 'Delhi'
        },
        max_recommendations: 3
      })
    });
    
    const recommendData = await recommendResponse.json();
    console.log('Recommendation response:', recommendData);
    
    console.log('✅ All tests completed successfully!');
    
  } catch (error) {
    console.error('❌ Connection test failed:', error);
  }
}

// Auto-run if in browser
if (typeof window !== 'undefined') {
  testBackendConnection();
}

export default testBackendConnection;
