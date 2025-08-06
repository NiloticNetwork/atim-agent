import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getKanbanItems } from '../services/api';
import { KanbanItem } from '../types';
import Navbar from '../components/Navbar';
import AuthStatusBanner from '../components/AuthStatusBanner';
import Footer from '../components/Footer';

interface BlockchainStats {
  totalBlocks: number;
  currentSupply: number;
  totalStakers: number;
  networkStatus: 'online' | 'offline' | 'syncing';
  lastBlockTime: string;
}

interface AtimActivity {
  issuesDetected: number;
  prsCreated: number;
  fixesApplied: number;
  lastActivity: string;
}

const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const [kanbanItems, setKanbanItems] = useState<KanbanItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Mock blockchain stats (in a real app, this would come from the blockchain API)
  const blockchainStats: BlockchainStats = {
    totalBlocks: 1247,
    currentSupply: 194250000 + (1247 * 5), // Premined + block rewards
    totalStakers: 23,
    networkStatus: 'online',
    lastBlockTime: new Date().toLocaleString()
  };

  // Mock Atim activity stats
  const atimActivity: AtimActivity = {
    issuesDetected: 8,
    prsCreated: 5,
    fixesApplied: 3,
    lastActivity: new Date().toLocaleString()
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await getKanbanItems();
        if (response.success && response.data) {
          setKanbanItems(response.data);
        } else {
          setError(response.error || 'Failed to load dashboard data');
        }
      } catch (error) {
        setError('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online': return 'text-green-400';
      case 'offline': return 'text-red-400';
      case 'syncing': return 'text-yellow-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'online': return '🟢';
      case 'offline': return '🔴';
      case 'syncing': return '🟡';
      default: return '⚪';
    }
  };

  const formatSLW = (amount: number) => {
    return new Intl.NumberFormat('en-US').format(amount);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900">
        <Navbar />
        <AuthStatusBanner />
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-400">Loading dashboard...</p>
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
      <AuthStatusBanner />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Dashboard</h1>
          <p className="text-gray-400">Monitor the Nilotic Network and Atim's activity</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Blockchain Stats */}
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white">Blockchain Status</h3>
              <span className={`text-sm ${getStatusColor(blockchainStats.networkStatus)}`}>
                {getStatusIcon(blockchainStats.networkStatus)} {blockchainStats.networkStatus}
              </span>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-400">Total Blocks:</span>
                <span className="text-white font-mono">{blockchainStats.totalBlocks.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Current Supply:</span>
                <span className="text-white font-mono">{formatSLW(blockchainStats.currentSupply)} SLW</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Active Stakers:</span>
                <span className="text-white font-mono">{blockchainStats.totalStakers}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Last Block:</span>
                <span className="text-white text-sm">{blockchainStats.lastBlockTime}</span>
              </div>
            </div>
          </div>

          {/* Atim Activity */}
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-4">Atim Activity</h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-400">Issues Detected:</span>
                <span className="text-yellow-400 font-mono">{atimActivity.issuesDetected}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">PRs Created:</span>
                <span className="text-blue-400 font-mono">{atimActivity.prsCreated}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Fixes Applied:</span>
                <span className="text-green-400 font-mono">{atimActivity.fixesApplied}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Last Activity:</span>
                <span className="text-white text-sm">{atimActivity.lastActivity}</span>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-4">Quick Actions</h3>
            <div className="space-y-3">
              <button 
                onClick={() => navigate('/kanban')}
                className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
              >
                View Kanban Board
              </button>
              <button 
                onClick={() => navigate('/github-proposals')}
                className="w-full px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition-colors"
              >
                GitHub Proposals
              </button>
              <button 
                onClick={() => navigate('/issues')}
                className="w-full px-4 py-2 bg-slate-700 text-white rounded hover:bg-slate-600 transition-colors"
              >
                Check Issues
              </button>
              <button 
                onClick={() => navigate('/chat')}
                className="w-full px-4 py-2 bg-slate-700 text-white rounded hover:bg-slate-600 transition-colors"
              >
                Chat with Atim
              </button>
            </div>
          </div>

          {/* Network Health */}
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-4">Network Health</h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-400">API Status:</span>
                <span className="text-green-400">✅ Online</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Database:</span>
                <span className="text-green-400">✅ Connected</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">GitHub Integration:</span>
                <span className="text-yellow-400">⚠️ Configure</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Email Service:</span>
                <span className="text-yellow-400">⚠️ Configure</span>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Recent Issues */}
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-4">Recent Issues</h3>
            <div className="space-y-3">
              {kanbanItems
                .filter(item => item.type === 'issue')
                .slice(0, 3)
                .map((item) => (
                  <div key={item.id} className="flex items-center justify-between p-3 bg-slate-700 rounded">
                    <div className="flex-1">
                      <h4 className="text-white font-medium text-sm">{item.title}</h4>
                      <p className="text-gray-400 text-xs">{item.description}</p>
                    </div>
                    <span className={`px-2 py-1 rounded text-xs ${
                      item.status === 'done' ? 'bg-green-700 text-green-100' :
                      item.status === 'in-progress' ? 'bg-yellow-700 text-yellow-100' :
                      'bg-blue-700 text-blue-100'
                    }`}>
                      {item.status}
                    </span>
                  </div>
                ))}
            </div>
          </div>

          {/* Recent PRs */}
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-4">Recent Pull Requests</h3>
            <div className="space-y-3">
              {kanbanItems
                .filter(item => item.type === 'pr')
                .slice(0, 3)
                .map((item) => (
                  <div key={item.id} className="flex items-center justify-between p-3 bg-slate-700 rounded">
                    <div className="flex-1">
                      <h4 className="text-white font-medium text-sm">{item.title}</h4>
                      <p className="text-gray-400 text-xs">{item.description}</p>
                    </div>
                    <span className={`px-2 py-1 rounded text-xs ${
                      item.status === 'done' ? 'bg-green-700 text-green-100' :
                      item.status === 'in-progress' ? 'bg-yellow-700 text-yellow-100' :
                      'bg-purple-700 text-purple-100'
                    }`}>
                      {item.status}
                    </span>
                  </div>
                ))}
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default DashboardPage; 