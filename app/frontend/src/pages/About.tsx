import { Link } from 'react-router-dom'

const About = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 sm:text-4xl">
            About Smart Government Scheme Advisor
          </h1>
          <p className="mt-4 max-w-2xl mx-auto text-xl text-gray-500 sm:text-2xl">
            An intelligent platform that helps Indian citizens find and apply for relevant government schemes
          </p>
        </div>

        <div className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white rounded-lg shadow-xl p-6">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">🎯 Our Mission</h2>
            <p className="text-gray-600 mb-4">
              To make government schemes accessible to every Indian citizen through intelligent search and personalized recommendations powered by AI.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-xl p-6">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">🔍 How It Works</h2>
            <ol className="list-decimal list-inside space-y-3 text-gray-600">
              <li className="mb-2">
                <strong className="text-gray-900">Personalized Search:</strong> Enter your details and get scheme recommendations tailored to your profile
              </li>
              <li className="mb-2">
                <strong className="text-gray-900">AI-Powered Matching:</strong> Our RAG system analyzes your query and finds the most relevant schemes
              </li>
              <li className="mb-2">
                <strong className="text-gray-900">Smart Filtering:</strong> Filter schemes by state, category, and income criteria
              </li>
              <li className="mb-2">
                <strong className="text-gray-900">Detailed Information:</strong> Get comprehensive details about eligibility, benefits, and application process
              </li>
            </ol>
          </div>

          <div className="bg-white rounded-lg shadow-xl p-6">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">🚀 Technology Stack</h2>
            <div className="space-y-3 text-gray-600">
              <p className="mb-2">
                <strong className="text-gray-900">Frontend:</strong> React + TypeScript + Tailwind CSS
              </p>
              <p className="mb-2">
                <strong className="text-gray-900">Backend:</strong> Python + FastAPI + FAISS + OpenAI
              </p>
              <p className="mb-2">
                <strong className="text-gray-900">AI/ML:</strong> Sentence Transformers + Vector Search + LLM
              </p>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-xl p-6">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">📊 Features</h2>
            <ul className="list-disc list-inside space-y-2 text-gray-600">
              <li>Intelligent scheme search with semantic understanding</li>
              <li>Personalized recommendations based on user profile</li>
              <li>Multi-criteria filtering (state, category, income)</li>
              <li>Real-time eligibility assessment</li>
              <li>Comprehensive scheme information</li>
            </ul>
          </div>
        </div>

        <div className="mt-12 text-center">
          <nav className="flex justify-center space-x-8">
            <Link 
              to="/" 
              className="text-blue-600 hover:text-blue-800 font-medium transition-colors duration-200"
            >
              Home
            </Link>
            <Link 
              to="/advisor" 
              className="text-blue-600 hover:text-blue-800 font-medium transition-colors duration-200"
            >
              Advisor
            </Link>
          </nav>
        </div>
      </div>
    </div>
  );
};

export default About;
