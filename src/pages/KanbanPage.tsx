import React, { useEffect, useState } from 'react';
import { getKanbanItems } from '../services/api';
import { KanbanItem } from '../types';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const KanbanCard: React.FC<{ item: KanbanItem }> = ({ item }) => {
  const getBadgeColor = (type: string, status: string) => {
    if (type === 'pr') {
      if (status === 'done') return 'bg-green-700 text-green-100';
      return 'bg-purple-700 text-purple-100';
    } else {
      if (status === 'todo') return 'bg-blue-700 text-blue-100';
      if (status === 'in-progress') return 'bg-yellow-700 text-yellow-100';
      return 'bg-green-700 text-green-100';
    }
  };

  const getTypeLabel = (type: string) => {
    return type === 'pr' ? 'Pull Request' : 'Issue';
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  return (
    <div className="bg-slate-800 rounded-lg p-4 shadow-md border border-slate-700 hover:border-slate-600 transition-colors">
      <div className="flex justify-between items-start mb-2">
        <span className={`text-xs px-2 py-1 rounded-full ${getBadgeColor(item.type, item.status)}`}>
          {getTypeLabel(item.type)} #{item.number}
        </span>
        <span className="text-xs text-gray-400">{formatDate(item.created_at)}</span>
      </div>
      <h3 className="font-medium text-white mb-2">{item.title}</h3>
      <p className="text-sm text-gray-300 mb-3 line-clamp-2">{item.description}</p>
      <a
        href={item.url}
        target="_blank"
        rel="noopener noreferrer"
        className="text-xs text-blue-400 hover:text-blue-300 flex items-center"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
        </svg>
        View on GitHub
      </a>
    </div>
  );
};

const KanbanColumn: React.FC<{ title: string; items: KanbanItem[]; status: string }> = ({ title, items, status }) => {
  return (
    <div className="flex flex-col bg-slate-900 rounded-lg p-4 shadow-md">
      <div className="flex items-center mb-4">
        <h2 className="text-lg font-semibold text-white">{title}</h2>
        <span className="ml-2 bg-slate-800 text-gray-300 px-2 py-1 rounded-full text-xs">
          {items.length}
        </span>
      </div>
      <div className="flex-1 overflow-y-auto space-y-3">
        {items.length > 0 ? (
          items.map((item) => <KanbanCard key={item.id} item={item} />)
        ) : (
          <div className="text-center text-gray-500 py-8">No items</div>
        )}
      </div>
    </div>
  );
};

const KanbanPage: React.FC = () => {
  const [items, setItems] = useState<KanbanItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await getKanbanItems();
        if (response.success && response.data) {
          setItems(response.data);
        } else {
          setError(response.error || 'Failed to load kanban items');
        }
      } catch (error) {
        setError('Failed to load kanban items');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Filter items by status
  const todoItems = items.filter(item => item.status === 'todo');
  const inProgressItems = items.filter(item => item.status === 'in-progress');
  const doneItems = items.filter(item => item.status === 'done');

  // Fallback sample data for development
  const sampleItems: KanbanItem[] = [
    {
      id: '1',
      title: 'Fix supply calculation bug in /chain endpoint',
      description: 'Currently using chain.size() * 10.0 instead of currentSupply',
      status: 'todo',
      type: 'issue',
      url: 'https://github.com/Emmanuel-Odero/nilotic-network/issues/1',
      number: 1,
      created_at: '2023-12-15T12:00:00Z',
      updated_at: '2023-12-15T12:00:00Z'
    },
    {
      id: '2',
      title: 'Add getCurrentSupply() method to Blockchain class',
      description: 'Needed to accurately report the circulating supply of SLW tokens',
      status: 'in-progress',
      type: 'pr',
      url: 'https://github.com/Emmanuel-Odero/nilotic-network/pull/2',
      number: 2,
      created_at: '2023-12-16T12:00:00Z',
      updated_at: '2023-12-16T14:00:00Z'
    },
    {
      id: '3',
      title: 'Fix race condition in multi-threaded staking',
      description: 'Adding a mutex to prevent concurrent modifications',
      status: 'done',
      type: 'pr',
      url: 'https://github.com/Emmanuel-Odero/nilotic-network/pull/3',
      number: 3,
      created_at: '2023-12-10T10:00:00Z',
      updated_at: '2023-12-11T16:00:00Z'
    },
    {
      id: '4',
      title: 'Improve validation for staking amounts',
      description: 'Add minimum stake amount and better error messages',
      status: 'in-progress',
      type: 'issue',
      url: 'https://github.com/Emmanuel-Odero/nilotic-network/issues/4',
      number: 4,
      created_at: '2023-12-17T09:00:00Z',
      updated_at: '2023-12-17T09:00:00Z'
    }
  ];

  // Use sample data if no items were loaded from API
  const displayTodoItems = todoItems.length > 0 ? todoItems : sampleItems.filter(item => item.status === 'todo');
  const displayInProgressItems = inProgressItems.length > 0 ? inProgressItems : sampleItems.filter(item => item.status === 'in-progress');
  const displayDoneItems = doneItems.length > 0 ? doneItems : sampleItems.filter(item => item.status === 'done');

  return (
    <div className="min-h-screen bg-slate-900 flex flex-col">
      <Navbar />
      <div className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">Nilotic Network Project Board</h1>
          <p className="mt-2 text-gray-400">
            Track issues and pull requests for the SLW blockchain.
          </p>
        </div>

        {error && (
          <div className="bg-red-900 border border-red-800 rounded-md p-4 mb-8">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-300">{error}</p>
              </div>
            </div>
          </div>
        )}

        {loading ? (
          <div className="flex justify-center items-center py-16">
            <svg className="animate-spin h-10 w-10 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <KanbanColumn
              title="To Do"
              items={displayTodoItems}
              status="todo"
            />
            <KanbanColumn
              title="In Progress"
              items={displayInProgressItems}
              status="in-progress"
            />
            <KanbanColumn
              title="Done"
              items={displayDoneItems}
              status="done"
            />
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default KanbanPage;
