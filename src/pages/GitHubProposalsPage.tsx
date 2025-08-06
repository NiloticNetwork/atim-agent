import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import AuthStatusBanner from '../components/AuthStatusBanner';
import Footer from '../components/Footer';

interface IssueProposal {
  id: string;
  title: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  category: string;
  file_path?: string;
  line_number?: number;
  suggested_fix?: string;
  labels: string[];
  created_at: string;
  status: 'pending' | 'approved' | 'rejected' | 'published';
  github_issue_number?: number;
}

interface GitHubStats {
  name: string;
  open_issues: number;
  open_pulls: number;
  stars: number;
  forks: number;
  language: string;
}

const GitHubProposalsPage: React.FC = () => {
  const navigate = useNavigate();
  const [proposals, setProposals] = useState<IssueProposal[]>([]);
  const [stats, setStats] = useState<GitHubStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [processing, setProcessing] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Fetch proposals
      const proposalsResponse = await fetch('http://localhost:5070/api/github/proposals');
      const proposalsData = await proposalsResponse.json();
      
      if (proposalsData.success) {
        setProposals(proposalsData.data);
      } else {
        setError(proposalsData.error || 'Failed to load proposals');
      }
      
      // Fetch GitHub stats
      const statsResponse = await fetch('http://localhost:5070/api/github/stats');
      const statsData = await statsResponse.json();
      
      if (statsData.success) {
        setStats(statsData.data);
      }
      
    } catch (error) {
      setError('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (proposalId: string) => {
    try {
      setProcessing(proposalId);
      
      const response = await fetch(`http://localhost:5070/api/github/proposals/${proposalId}/approve`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      const data = await response.json();
      
      if (data.success) {
        // Update the proposal status
        setProposals(prev => prev.map(p => 
          p.id === proposalId 
            ? { ...p, status: 'published', github_issue_number: data.data.issue_number }
            : p
        ));
        
        alert(`Issue created successfully! GitHub Issue #${data.data.issue_number}`);
      } else {
        alert(`Error: ${data.error}`);
      }
    } catch (error) {
      alert('Failed to approve proposal');
    } finally {
      setProcessing(null);
    }
  };

  const handleReject = async (proposalId: string) => {
    try {
      setProcessing(proposalId);
      
      const response = await fetch(`http://localhost:5070/api/github/proposals/${proposalId}/reject`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      const data = await response.json();
      
      if (data.success) {
        // Update the proposal status
        setProposals(prev => prev.map(p => 
          p.id === proposalId 
            ? { ...p, status: 'rejected' }
            : p
        ));
        
        alert('Proposal rejected successfully');
      } else {
        alert(`Error: ${data.error}`);
      }
    } catch (error) {
      alert('Failed to reject proposal');
    } finally {
      setProcessing(null);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-700 text-red-100';
      case 'high': return 'bg-orange-700 text-orange-100';
      case 'medium': return 'bg-yellow-700 text-yellow-100';
      case 'low': return 'bg-blue-700 text-blue-100';
      default: return 'bg-gray-700 text-gray-100';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'published': return 'bg-green-700 text-green-100';
      case 'rejected': return 'bg-red-700 text-red-100';
      case 'approved': return 'bg-blue-700 text-blue-100';
      case 'pending': return 'bg-yellow-700 text-yellow-100';
      default: return 'bg-gray-700 text-gray-100';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'security': return '🔒';
      case 'performance': return '⚡';
      case 'bug': return '🐛';
      case 'enhancement': return '✨';
      case 'documentation': return '📚';
      default: return '📝';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900">
        <Navbar />
        <AuthStatusBanner />
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-400">Loading GitHub proposals...</p>
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
        <AuthStatusBanner />
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <p className="text-red-400 mb-4">Error: {error}</p>
            <button 
              onClick={fetchData} 
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

  const pendingProposals = proposals.filter(p => p.status === 'pending');
  const publishedProposals = proposals.filter(p => p.status === 'published');
  const rejectedProposals = proposals.filter(p => p.status === 'rejected');

  return (
    <div className="min-h-screen bg-slate-900">
      <Navbar />
      <AuthStatusBanner />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">GitHub Issue Proposals</h1>
          <p className="text-gray-400">Review and manage issue proposals for the NiloticNetwork repository</p>
        </div>

        {/* GitHub Stats */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
            <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
              <h3 className="text-sm font-medium text-gray-400">Repository</h3>
              <p className="text-lg font-semibold text-white">{stats.name}</p>
            </div>
            <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
              <h3 className="text-sm font-medium text-gray-400">Open Issues</h3>
              <p className="text-lg font-semibold text-yellow-400">{stats.open_issues}</p>
            </div>
            <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
              <h3 className="text-sm font-medium text-gray-400">Open PRs</h3>
              <p className="text-lg font-semibold text-blue-400">{stats.open_pulls}</p>
            </div>
            <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
              <h3 className="text-sm font-medium text-gray-400">Stars</h3>
              <p className="text-lg font-semibold text-yellow-400">{stats.stars}</p>
            </div>
            <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
              <h3 className="text-sm font-medium text-gray-400">Language</h3>
              <p className="text-lg font-semibold text-white">{stats.language}</p>
            </div>
          </div>
        )}

        {/* Summary Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-2">Pending Review</h3>
            <p className="text-3xl font-bold text-yellow-400">{pendingProposals.length}</p>
            <p className="text-sm text-gray-400 mt-2">Awaiting approval</p>
          </div>
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-2">Published</h3>
            <p className="text-3xl font-bold text-green-400">{publishedProposals.length}</p>
            <p className="text-sm text-gray-400 mt-2">Created on GitHub</p>
          </div>
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-2">Rejected</h3>
            <p className="text-3xl font-bold text-red-400">{rejectedProposals.length}</p>
            <p className="text-sm text-gray-400 mt-2">Not approved</p>
          </div>
        </div>

        {/* Pending Proposals */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-white mb-4">Pending Proposals</h2>
          {pendingProposals.length === 0 ? (
            <div className="bg-slate-800 rounded-lg p-8 text-center border border-slate-700">
              <p className="text-gray-400">No pending proposals</p>
            </div>
          ) : (
            <div className="space-y-4">
              {pendingProposals.map((proposal) => (
                <div key={proposal.id} className="bg-slate-800 rounded-lg p-6 border border-slate-700">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <span className="text-2xl">{getCategoryIcon(proposal.category)}</span>
                        <h3 className="text-lg font-semibold text-white">{proposal.title}</h3>
                        <span className={`px-2 py-1 rounded text-xs font-medium ${getSeverityColor(proposal.severity)}`}>
                          {proposal.severity.toUpperCase()}
                        </span>
                        <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(proposal.status)}`}>
                          {proposal.status.toUpperCase()}
                        </span>
                      </div>
                      
                      <p className="text-gray-300 mb-3">{proposal.description}</p>
                      
                      <div className="flex items-center gap-6 text-sm text-gray-400 mb-3">
                        <span>Category: {proposal.category}</span>
                        {proposal.file_path && <span>File: {proposal.file_path}</span>}
                        {proposal.line_number && <span>Line: {proposal.line_number}</span>}
                        <span>Created: {new Date(proposal.created_at).toLocaleDateString()}</span>
                      </div>
                      
                      {proposal.labels.length > 0 && (
                        <div className="flex gap-2 mb-3">
                          {proposal.labels.map((label, index) => (
                            <span key={index} className="px-2 py-1 bg-slate-700 text-gray-300 rounded text-xs">
                              {label}
                            </span>
                          ))}
                        </div>
                      )}
                      
                      {proposal.suggested_fix && (
                        <div className="mb-4 p-4 bg-slate-700 rounded border-l-4 border-blue-500">
                          <h4 className="text-sm font-medium text-white mb-2">Suggested Fix:</h4>
                          <pre className="text-sm text-gray-300 whitespace-pre-wrap">{proposal.suggested_fix}</pre>
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex gap-3">
                    <button
                      onClick={() => handleApprove(proposal.id)}
                      disabled={processing === proposal.id}
                      className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      {processing === proposal.id ? 'Creating...' : 'Approve & Create Issue'}
                    </button>
                    <button
                      onClick={() => handleReject(proposal.id)}
                      disabled={processing === proposal.id}
                      className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      {processing === proposal.id ? 'Processing...' : 'Reject'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Published Proposals */}
        {publishedProposals.length > 0 && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-white mb-4">Published Issues</h2>
            <div className="space-y-4">
              {publishedProposals.map((proposal) => (
                <div key={proposal.id} className="bg-slate-800 rounded-lg p-6 border border-slate-700">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <span className="text-2xl">{getCategoryIcon(proposal.category)}</span>
                        <h3 className="text-lg font-semibold text-white">{proposal.title}</h3>
                        <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(proposal.status)}`}>
                          PUBLISHED
                        </span>
                      </div>
                      
                      <p className="text-gray-300 mb-3">{proposal.description}</p>
                      
                      <div className="flex items-center gap-6 text-sm text-gray-400">
                        <span>GitHub Issue: #{proposal.github_issue_number}</span>
                        <span>Published: {new Date(proposal.created_at).toLocaleDateString()}</span>
                      </div>
                    </div>
                    
                    <a
                      href={`https://github.com/NiloticNetwork/NiloticNetworkBlockchain/issues/${proposal.github_issue_number}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                    >
                      View on GitHub
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Rejected Proposals */}
        {rejectedProposals.length > 0 && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-white mb-4">Rejected Proposals</h2>
            <div className="space-y-4">
              {rejectedProposals.map((proposal) => (
                <div key={proposal.id} className="bg-slate-800 rounded-lg p-6 border border-slate-700 opacity-75">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <span className="text-2xl">{getCategoryIcon(proposal.category)}</span>
                        <h3 className="text-lg font-semibold text-white">{proposal.title}</h3>
                        <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(proposal.status)}`}>
                          REJECTED
                        </span>
                      </div>
                      
                      <p className="text-gray-300 mb-3">{proposal.description}</p>
                      
                      <div className="flex items-center gap-6 text-sm text-gray-400">
                        <span>Rejected: {new Date(proposal.created_at).toLocaleDateString()}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
};

export default GitHubProposalsPage; 