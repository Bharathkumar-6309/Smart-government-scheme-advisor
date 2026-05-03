import { Link } from 'react-router-dom'

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white sm:text-5xl lg:text-6xl">
            Smart Government Scheme Advisor
          </h1>
          <p className="mt-4 max-w-2xl mx-auto text-xl text-blue-100 sm:text-2xl">
            Find and apply for government schemes tailored to your needs
          </p>
          
          <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-white rounded-lg shadow-xl p-6 transform transition-all duration-300 hover:scale-105">
              <div className="text-center">
                <div className="text-6xl font-bold text-blue-600 mb-4">🔍</div>
                <h2 className="text-2xl font-semibold text-gray-900 mb-2">Search Schemes</h2>
                <p className="text-gray-600 mb-6">Find relevant government schemes based on your profile</p>
              </div>
              <div className="mt-4">
                <Link 
                  to="/advisor" 
                  className="w-full bg-blue-600 text-white font-medium py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors duration-200"
                >
                  Start Searching
                </Link>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow-xl p-6 transform transition-all duration-300 hover:scale-105">
              <div className="text-center">
                <div className="text-6xl font-bold text-green-600 mb-4">🤖</div>
                <h2 className="text-2xl font-semibold text-gray-900 mb-2">Get Recommendations</h2>
                <p className="text-gray-600 mb-6">Personalized scheme recommendations based on your profile</p>
              </div>
              <div className="mt-4">
                <Link 
                  to="/advisor" 
                  className="w-full bg-green-600 text-white font-medium py-3 px-6 rounded-lg hover:bg-green-700 transition-colors duration-200"
                >
                  Get Recommendations
                </Link>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow-xl p-6 transform transition-all duration-300 hover:scale-105">
              <div className="text-center">
                <div className="text-6xl font-bold text-purple-600 mb-4">📊</div>
                <h2 className="text-2xl font-semibold text-gray-900 mb-2">Browse Categories</h2>
                <p className="text-gray-600 mb-6">Explore schemes by category</p>
              </div>
              <div className="mt-4">
                <Link 
                  to="/advisor" 
                  className="w-full bg-purple-600 text-white font-medium py-3 px-6 rounded-lg hover:bg-purple-700 transition-colors duration-200"
                >
                  Browse Schemes
                </Link>
              </div>
            </div>
          </div>
          
          <div className="mt-12 text-center">
            <nav className="flex justify-center space-x-8">
              <Link 
                to="/advisor" 
                className="text-blue-600 hover:text-blue-800 font-medium transition-colors duration-200"
              >
                Advisor
              </Link>
              <Link 
                to="/about" 
                className="text-gray-600 hover:text-gray-800 font-medium transition-colors duration-200"
              >
                About
              </Link>
            </nav>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
