import React, { useState } from 'react';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-lg sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">CN</span>
            </div>
            <span className="text-xl font-bold text-gray-800">Coding Ninjas</span>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            {['Courses', 'Practice', 'Events', 'Campus Ninjas', 'Blog'].map((item) => (
              <a key={item} href="#" className="text-gray-600 hover:text-blue-500 font-medium transition-colors">
                {item}
              </a>
            ))}
          </nav>

          {/* Auth Buttons */}
          <div className="hidden md:flex space-x-4">
            <button className="px-4 py-2 text-gray-600 font-medium hover:text-blue-500 transition-colors">
              Login
            </button>
            <button className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors font-medium">
              Sign Up
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button 
            className="md:hidden"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t">
            <nav className="flex flex-col space-y-4">
              {['Courses', 'Practice', 'Events', 'Campus Ninjas', 'Blog'].map((item) => (
                <a key={item} href="#" className="text-gray-600 hover:text-blue-500 font-medium">
                  {item}
                </a>
              ))}
              <div className="flex space-x-4 pt-4">
                <button className="flex-1 py-2 text-gray-600 font-medium border border-gray-300 rounded-lg">
                  Login
                </button>
                <button className="flex-1 py-2 bg-blue-500 text-white rounded-lg font-medium">
                  Sign Up
                </button>
              </div>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;