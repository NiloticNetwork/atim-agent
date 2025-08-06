import React from 'react';
import { useAuth } from '../utils/AuthContext';
import { Link } from 'react-router-dom';

const AuthStatusBanner: React.FC = () => {
  const { isAuthenticated, user, loading } = useAuth();

  if (loading) {
    return (
      <div className="bg-blue-900 border-b border-blue-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2">
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-300 mr-2"></div>
            <span className="text-blue-200 text-sm">Checking authentication...</span>
          </div>
        </div>
      </div>
    );
  }

  if (isAuthenticated) {
    return (
      <div className="bg-green-900 border-b border-green-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-400 rounded-full"></div>
              <span className="text-green-200 text-sm">
                Signed in as <span className="font-medium">{user?.email}</span>
              </span>
            </div>
            <div className="flex items-center space-x-4 text-sm">
              <Link 
                to="/dashboard" 
                className="text-green-300 hover:text-green-200 transition-colors"
              >
                Dashboard
              </Link>
              <Link 
                to="/github-proposals" 
                className="text-green-300 hover:text-green-200 transition-colors"
              >
                GitHub Proposals
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-yellow-900 border-b border-yellow-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-yellow-400 rounded-full"></div>
            <span className="text-yellow-200 text-sm">
              You are not signed in. Some features may be limited.
            </span>
          </div>
          <div className="flex items-center space-x-4 text-sm">
            <Link 
              to="/login" 
              className="text-yellow-300 hover:text-yellow-200 transition-colors"
            >
              Sign In
            </Link>
            <Link 
              to="/register" 
              className="text-yellow-300 hover:text-yellow-200 transition-colors"
            >
              Register
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthStatusBanner; 