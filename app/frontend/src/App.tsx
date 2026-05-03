import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Advisor from './pages/Advisor'
import About from './pages/About'
import './index.css'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-8">
            <h1 className="text-3xl font-bold text-gray-900 sm:text-4xl">
              Smart Government Scheme Advisor
            </h1>
            <p className="mt-3 max-w-2xl mx-auto text-xl text-gray-500 sm:text-2xl">
              Find and apply for government schemes tailored to your needs
            </p>
          </div>
          
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/advisor" element={<Advisor />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </div>
      </div>
    </Router>
  )
}

export default App
