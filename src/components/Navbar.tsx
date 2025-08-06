import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../utils/AuthContext';

const Navbar: React.FC = () => {
  const { isAuthenticated, user, logout, loading } = useAuth();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-slate-900 text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex-shrink-0 flex items-center">
              <span className="text-xl font-bold">Atim</span>
              <span className="ml-2 text-blue-400 font-light">Nilotic Network Assistant</span>
            </Link>
          </div>

          {/* Desktop menu */}
          <div className="hidden md:flex items-center space-x-4">
            <Link to="/" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-800">
              Home
            </Link>
            <Link to="/kanban" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-800">
              Kanban
            </Link>

            {loading ? (
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
                <span className="text-sm text-gray-400">Loading...</span>
              </div>
            ) : isAuthenticated ? (
              <>
                <Link to="/dashboard" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-800">
                  Dashboard
                </Link>
                <Link to="/github-proposals" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-800">
                  GitHub Proposals
                </Link>
                <Link to="/issues" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-800">
                  Issues
                </Link>
                <Link to="/chat" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-800">
                  Chat
                </Link>
                
                {/* User info */}
                <div className="flex items-center space-x-3 ml-4 pl-4 border-l border-slate-700">
                  <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                      <span className="text-sm font-medium text-white">
                        {user?.email?.charAt(0).toUpperCase() || 'U'}
                      </span>
                    </div>
                    <div className="text-sm">
                      <div className="text-white font-medium">{user?.email || 'User'}</div>
                      <div className="text-xs text-green-400 flex items-center">
                        <div className="w-2 h-2 bg-green-400 rounded-full mr-1"></div>
                        Signed In
                      </div>
                    </div>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="px-3 py-1 rounded text-xs font-medium bg-red-700 hover:bg-red-800 transition-colors"
                  >
                    Logout
                  </button>
                </div>
              </>
            ) : (
              <>
                <div className="flex items-center space-x-2 text-sm text-gray-400">
                  <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                  <span>Not signed in</span>
                </div>
                <Link
                  to="/login"
                  className="px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-800"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="ml-2 px-3 py-2 rounded-md text-sm font-medium bg-blue-600 hover:bg-blue-700"
                >
                  Register
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={toggleMenu}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-slate-800 focus:outline-none"
              aria-expanded="false"
            >
              <span className="sr-only">Open main menu</span>
              {!isMenuOpen ? (
                <svg className="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              ) : (
                <svg className="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu, toggle based on menu state */}
      {isMenuOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            <Link
              to="/"
              className="block px-3 py-2 rounded-md text-base font-medium hover:bg-slate-800"
              onClick={() => setIsMenuOpen(false)}
            >
              Home
            </Link>
            <Link
              to="/kanban"
              className="block px-3 py-2 rounded-md text-base font-medium hover:bg-slate-800"
              onClick={() => setIsMenuOpen(false)}
            >
              Kanban
            </Link>

            {loading ? (
              <div className="flex items-center space-x-2 px-3 py-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
                <span className="text-sm text-gray-400">Loading...</span>
              </div>
            ) : isAuthenticated ? (
              <>
                {/* User info for mobile */}
                <div className="px-3 py-2 border-b border-slate-700 mb-2">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
                      <span className="text-sm font-medium text-white">
                        {user?.email?.charAt(0).toUpperCase() || 'U'}
                      </span>
                    </div>
                    <div className="flex-1">
                      <div className="text-white font-medium text-sm">{user?.email || 'User'}</div>
                      <div className="text-xs text-green-400 flex items-center">
                        <div className="w-2 h-2 bg-green-400 rounded-full mr-1"></div>
                        Signed In
                      </div>
                    </div>
                  </div>
                </div>
                
                <Link
                  to="/dashboard"
                  className="block px-3 py-2 rounded-md text-base font-medium hover:bg-slate-800"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Dashboard
                </Link>
                <Link
                  to="/github-proposals"
                  className="block px-3 py-2 rounded-md text-base font-medium hover:bg-slate-800"
                  onClick={() => setIsMenuOpen(false)}
                >
                  GitHub Proposals
                </Link>
                <Link
                  to="/issues"
                  className="block px-3 py-2 rounded-md text-base font-medium hover:bg-slate-800"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Issues
                </Link>
                <Link
                  to="/chat"
                  className="block px-3 py-2 rounded-md text-base font-medium hover:bg-slate-800"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Chat
                </Link>
                <button
                  onClick={() => {
                    handleLogout();
                    setIsMenuOpen(false);
                  }}
                  className="mt-2 w-full px-3 py-2 rounded-md text-base font-medium bg-red-700 hover:bg-red-800"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <div className="px-3 py-2 text-sm text-gray-400 flex items-center">
                  <div className="w-2 h-2 bg-gray-400 rounded-full mr-2"></div>
                  <span>Not signed in</span>
                </div>
                <Link
                  to="/login"
                  className="block px-3 py-2 rounded-md text-base font-medium hover:bg-slate-800"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="block mt-2 px-3 py-2 rounded-md text-base font-medium bg-blue-600 hover:bg-blue-700"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
