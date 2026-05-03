import { useState } from 'react'

interface FormData {
  age: string;
  income: string;
  occupation: string;
  education: string;
  state: string;
  category: string;
}

interface Scheme {
  id: string;
  name: string;
  category: string;
  description: string;
  benefits: string;
  documents_required: string[];
  eligibility_criteria: string[];
  state: string;
  income_limit: number | null;
  official_link: string;
  similarity_score?: number;
  why_eligible?: string;
  application_steps?: string[];
  confidence_score?: number;
}

const Advisor = () => {
  const [formData, setFormData] = useState<FormData>({
    age: '',
    income: '',
    occupation: '',
    education: '',
    state: '',
    category: ''
  });

  const [schemes, setSchemes] = useState<Scheme[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchMode, setSearchMode] = useState<'search' | 'recommend'>('search');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSearch = async () => {
    if (!formData.age || !formData.income) {
      alert('Please fill in at least age and income for personalized recommendations');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8002/api/schemes/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          query: searchMode === 'search' ? 'government schemes' : 'personalized recommendations',
          user_profile: {
            age: parseInt(formData.age),
            income: parseInt(formData.income),
            occupation: formData.occupation,
            education: formData.education,
            state: formData.state
          },
          filters: {
            category: formData.category,
            state: formData.state,
            income_limit: formData.income ? parseInt(formData.income) : null
          }
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        setSchemes(data.data || []);
      } else {
        throw new Error(data.message || 'Search failed');
      }
    } catch (error) {
      console.error('Search error:', error);
      alert('Failed to search schemes. Please try again.');
      setSchemes([]);
    } finally {
      setLoading(false);
    }
  };

  const handleRecommend = async () => {
    if (!formData.age || !formData.income) {
      alert('Please fill in age and income for personalized recommendations');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8002/api/schemes/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          user_profile: {
            age: parseInt(formData.age),
            income: parseInt(formData.income),
            occupation: formData.occupation,
            education: formData.education,
            state: formData.state
          },
          max_recommendations: 5
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        setSchemes(data.recommendations || []);
      } else {
        throw new Error(data.message || 'Recommendation failed');
      }
    } catch (error) {
      console.error('Recommendation error:', error);
      alert('Failed to get recommendations. Please try again.');
      setSchemes([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 sm:text-4xl">
            Scheme Advisor
          </h1>
          <p className="mt-3 max-w-2xl mx-auto text-xl text-gray-500 sm:text-2xl">
            Search and get personalized government scheme recommendations
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Form Section */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-xl p-6">
              <h2 className="text-2xl font-semibold text-gray-900 mb-6">Tell us about yourself</h2>
              
              <form className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Age *</label>
                  <input
                    type="number"
                    name="age"
                    value={formData.age}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 sm:text-sm"
                    placeholder="Enter your age"
                    min="1"
                    max="100"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Annual Income (₹) *</label>
                  <input
                    type="number"
                    name="income"
                    value={formData.income}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 sm:text-sm"
                    placeholder="Enter your annual income"
                    min="0"
                    step="10000"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Occupation</label>
                  <input
                    type="text"
                    name="occupation"
                    value={formData.occupation}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 sm:text-sm"
                    placeholder="e.g., Student, Farmer, Business Owner"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Education</label>
                  <input
                    type="text"
                    name="education"
                    value={formData.education}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 sm:text-sm"
                    placeholder="e.g., High School, Graduate, MBA"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">State</label>
                  <select
                    name="state"
                    value={formData.state}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 sm:text-sm"
                  >
                    <option value="">Select your state</option>
                    <option value="All India">All India</option>
                    <option value="Andhra Pradesh">Andhra Pradesh</option>
                    <option value="Arunachal Pradesh">Arunachal Pradesh</option>
                    <option value="Assam">Assam</option>
                    <option value="Bihar">Bihar</option>
                    <option value="Chhattisgarh">Chhattisgarh</option>
                    <option value="Goa">Goa</option>
                    <option value="Gujarat">Gujarat</option>
                    <option value="Haryana">Haryana</option>
                    <option value="Himachal Pradesh">Himachal Pradesh</option>
                    <option value="Jharkhand">Jharkhand</option>
                    <option value="Karnataka">Karnataka</option>
                    <option value="Kerala">Kerala</option>
                    <option value="Madhya Pradesh">Madhya Pradesh</option>
                    <option value="Maharashtra">Maharashtra</option>
                    <option value="Manipur">Manipur</option>
                    <option value="Meghalaya">Meghalaya</option>
                    <option value="Mizoram">Mizoram</option>
                    <option value="Nagaland">Nagaland</option>
                    <option value="Odisha">Odisha</option>
                    <option value="Punjab">Punjab</option>
                    <option value="Rajasthan">Rajasthan</option>
                    <option value="Sikkim">Sikkim</option>
                    <option value="Tamil Nadu">Tamil Nadu</option>
                    <option value="Telangana">Telangana</option>
                    <option value="Tripura">Tripura</option>
                    <option value="Uttar Pradesh">Uttar Pradesh</option>
                    <option value="Uttarakhand">Uttarakhand</option>
                    <option value="West Bengal">West Bengal</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
                  <select
                    name="category"
                    value={formData.category}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 sm:text-sm"
                  >
                    <option value="">All Categories</option>
                    <option value="agriculture">Agriculture</option>
                    <option value="education">Education</option>
                    <option value="energy">Energy</option>
                    <option value="financial_inclusion">Financial Inclusion</option>
                    <option value="healthcare">Healthcare</option>
                    <option value="housing">Housing</option>
                    <option value="skill_development">Skill Development</option>
                    <option value="women_empowerment">Women Empowerment</option>
                  </select>
                </div>

                <div className="flex space-x-4">
                  <button
                    type="button"
                    onClick={() => {
                      setSearchMode('search');
                      handleSearch();
                    }}
                    className={`flex-1 py-2 px-4 rounded-md font-medium transition-colors duration-200 ${
                      searchMode === 'search' 
                        ? 'bg-blue-600 text-white hover:bg-blue-700' 
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    🔍 Search Schemes
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setSearchMode('recommend');
                      handleRecommend();
                    }}
                    className={`flex-1 py-2 px-4 rounded-md font-medium transition-colors duration-200 ${
                      searchMode === 'recommend' 
                        ? 'bg-green-600 text-white hover:bg-green-700' 
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    🤖 Get Recommendations
                  </button>
                </div>
              </form>
            </div>
          </div>

          {/* Results Section */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-xl p-6">
              <h2 className="text-2xl font-semibold text-gray-900 mb-6">
                {searchMode === 'search' ? 'Search Results' : 'Personalized Recommendations'}
              </h2>

              {loading ? (
                <div className="text-center py-8">
                  <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
                  <p className="mt-2 text-gray-600">Searching...</p>
                </div>
              ) : schemes.length > 0 ? (
                <div className="space-y-6">
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                    <h3 className="text-lg font-semibold text-blue-900 mb-2">
                      📊 Retrieved Sources (Top {schemes.length})
                    </h3>
                    <p className="text-blue-700 text-sm">
                      Found {schemes.length} relevant schemes based on your profile and search criteria
                    </p>
                  </div>
                  
                  {schemes.map((scheme, index) => (
                    <div key={scheme.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow duration-200">
                      <div className="flex justify-between items-start mb-4">
                        <div>
                          <span className="inline-block px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 rounded-full mr-2">
                            #{index + 1}
                          </span>
                          <h3 className="text-lg font-semibold text-gray-900 inline">{scheme.name}</h3>
                        </div>
                        <div className="flex items-center space-x-2">
                          {scheme.confidence_score && (
                            <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                              {Math.round(scheme.confidence_score * 100)}% Match
                            </span>
                          )}
                          {scheme.similarity_score && (
                            <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                              {Math.round(scheme.similarity_score * 100)}% Similar
                            </span>
                          )}
                        </div>
                      </div>

                      <div className="text-gray-600 mb-4">
                        <p className="font-medium text-gray-900 mb-2">Description:</p>
                        <p>{scheme.description}</p>
                      </div>

                      {scheme.why_eligible && (
                        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
                          <p className="font-medium text-blue-900 mb-2">💡 Why you're eligible:</p>
                          <p>{scheme.why_eligible}</p>
                        </div>
                      )}

                      <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                        <p className="font-medium text-green-900 mb-2">💰 Benefits:</p>
                        <p>{scheme.benefits}</p>
                      </div>

                      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
                        <p className="font-medium text-yellow-900 mb-2">📋 Required Documents:</p>
                        <ul className="list-disc list-inside space-y-1">
                          {scheme.documents_required.map((doc, idx) => (
                            <li key={idx} className="text-sm">{doc}</li>
                          ))}
                        </ul>
                      </div>

                      {scheme.application_steps && (
                        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-4">
                          <p className="font-medium text-purple-900 mb-2">📝 How to Apply:</p>
                          <ol className="list-decimal list-inside space-y-1 text-sm">
                            {scheme.application_steps.map((step, idx) => (
                              <li key={idx}>{step}</li>
                            ))}
                          </ol>
                        </div>
                      )}

                      <div className="flex justify-between items-center mt-6">
                        <div className="text-sm text-gray-500">
                          Category: <span className="font-medium text-gray-900">{scheme.category}</span> | 
                          State: <span className="font-medium text-gray-900">{scheme.state}</span>
                          {scheme.income_limit && (
                            <> | Income Limit: ₹{scheme.income_limit.toLocaleString()}</>
                          )}
                        </div>
                        <a
                          href={scheme.official_link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 transition-colors duration-200"
                        >
                          Visit Official Website
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <div className="text-gray-500">
                    <div className="text-6xl mb-4">🔍</div>
                    <p>No schemes found</p>
                    <p className="text-sm mt-2">Try adjusting your search criteria or filters</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Advisor;
