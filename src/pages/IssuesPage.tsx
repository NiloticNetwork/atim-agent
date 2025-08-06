import React, { useEffect, useState } from 'react';
import { getIssues } from '../services/api';
import { Issue } from '../types';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const IssuesPage: React.FC = () => {
  const [issues, setIssues] = useState<Issue[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchIssues = async () => {
      try {
        setLoading(true);
        const response = await getIssues();
        if (response.success && response.data) {
          setIssues(response.data);
        } else {
          setError(response.error || 'Failed to load issues');
        }
      } catch (error) {
        setError('Failed to load issues');
      } finally {
        setLoading(false);
      }
    };

    fetchIssues();
  }, []);

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return 'bg-red-700 text-red-100';
      case 'medium': return 'bg-yellow-700 text-yellow-100';
      case 'low': return 'bg-blue-700 text-blue-100';
      default: return 'bg-gray-700 text-gray-100';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'fixed': return 'bg-green-700 text-green-100';
      case 'rejected': return 'bg-red-700 text-red-100';
      case 'open': return 'bg-yellow-700 text-yellow-100';
      default: return 'bg-gray-700 text-gray-100';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900">
        <Navbar />
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-400">Loading issues...</p>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-900">
        <Navbar />
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <p className="text-red-400 mb-4">Error: {error}</p>
            <button 
              onClick={() => window.location.reload()} 
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Retry
            </button>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Issue Tracker</h1>
          <p className="text-gray-400">Monitor and manage detected issues in the Nilotic Network codebase</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-2">Total Issues</h3>
            <p className="text-3xl font-bold text-blue-400">{issues.length}</p>
          </div>
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-2">Open Issues</h3>
            <p className="text-3xl font-bold text-yellow-400">
              {issues.filter(issue => issue.status === 'open').length}
            </p>
          </div>
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-2">Fixed Issues</h3>
            <p className="text-3xl font-bold text-green-400">
              {issues.filter(issue => issue.status === 'fixed').length}
            </p>
          </div>
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-2">High Priority</h3>
            <p className="text-3xl font-bold text-red-400">
              {issues.filter(issue => issue.severity === 'high').length}
            </p>
          </div>
        </div>

        {/* Issues List */}
        <div className="bg-slate-800 rounded-lg border border-slate-700">
          <div className="px-6 py-4 border-b border-slate-700">
            <h2 className="text-xl font-semibold text-white">All Issues</h2>
          </div>
          
          {issues.length === 0 ? (
            <div className="p-8 text-center">
              <p className="text-gray-400">No issues found. Great job!</p>
            </div>
          ) : (
            <div className="divide-y divide-slate-700">
              {issues.map((issue) => (
                <div key={issue.id} className="p-6 hover:bg-slate-750 transition-colors">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-medium text-white">{issue.title}</h3>
                        <span className={`px-2 py-1 rounded text-xs font-medium ${getSeverityColor(issue.severity)}`}>
                          {issue.severity.toUpperCase()}
                        </span>
                        <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(issue.status)}`}>
                          {issue.status.toUpperCase()}
                        </span>
                      </div>
                      
                      <p className="text-gray-300 mb-3">{issue.description}</p>
                      
                      <div className="flex items-center gap-6 text-sm text-gray-400">
                        <span>File: {issue.file_path}</span>
                        <span>Line: {issue.line_number}</span>
                        <span>Created: {new Date(issue.created_at).toLocaleDateString()}</span>
                      </div>
                      
                      {issue.suggested_fix && (
                        <div className="mt-4 p-4 bg-slate-700 rounded border-l-4 border-blue-500">
                          <h4 className="text-sm font-medium text-white mb-2">Suggested Fix:</h4>
                          <pre className="text-sm text-gray-300 whitespace-pre-wrap">{issue.suggested_fix}</pre>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default IssuesPage; 