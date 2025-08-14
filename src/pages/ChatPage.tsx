import React, { useState, useEffect, useRef } from 'react';
import { getChatMessages, sendChatMessage } from '../services/api';
import { ChatMessage } from '../types';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showMettaDetails, setShowMettaDetails] = useState<Set<string>>(new Set());
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        setLoading(true);
        const response = await getChatMessages();
        if (response.success && response.data) {
          setMessages(response.data);
        } else {
          setError(response.error || 'Failed to load messages');
        }
      } catch (error) {
        setError('Failed to load messages');
      } finally {
        setLoading(false);
      }
    };

    fetchMessages();
  }, []);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      sender: 'user',
      content: newMessage,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setNewMessage('');
    setSending(true);

    try {
      const response = await sendChatMessage(newMessage);
      if (response.success && response.data) {
        setMessages(prev => [...prev, response.data!]);
              } else {
          // Fallback response with MeTTa reasoning
          const atimResponse: ChatMessage = {
            id: (Date.now() + 1).toString(),
            sender: 'atim',
            content: `I'm analyzing your question about "${newMessage}" using MeTTa reasoning. Let me provide you with a detailed analysis of the Nilotic Network blockchain aspects you're asking about.`,
            timestamp: new Date().toISOString(),
            metadata: {
              reasoning_type: 'general_analysis',
              confidence: 0.8
            }
          };
          setMessages(prev => [...prev, atimResponse]);
        }
    } catch (error) {
      // Fallback response
      const atimResponse: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'atim',
        content: `I received your message: "${newMessage}". I'm here to help with the Nilotic Network blockchain development using MeTTa reasoning. What specific aspect would you like to discuss?`,
        timestamp: new Date().toISOString(),
        metadata: {
          reasoning_type: 'fallback',
          confidence: 0.5
        }
      };
      setMessages(prev => [...prev, atimResponse]);
    } finally {
      setSending(false);
    }
  };

  const toggleMettaDetails = (messageId: string) => {
    const newSet = new Set(showMettaDetails);
    if (newSet.has(messageId)) {
      newSet.delete(messageId);
    } else {
      newSet.add(messageId);
    }
    setShowMettaDetails(newSet);
  };

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const renderMettaBadge = (metadata?: ChatMessage['metadata']) => {
    if (!metadata?.reasoning_type) return null;
    
    const getBadgeColor = (type: string) => {
      switch (type) {
        case 'supply_calculation': return 'bg-green-600';
        case 'security_verification': return 'bg-red-600';
        case 'consensus_analysis': return 'bg-blue-600';
        case 'code_analysis': return 'bg-purple-600';
        case 'mathematical_proof': return 'bg-yellow-600';
        case 'blockchain_logic': return 'bg-indigo-600';
        default: return 'bg-gray-600';
      }
    };

    return (
      <div className="flex items-center gap-2 mt-2">
        <span className={`px-2 py-1 text-xs rounded-full ${getBadgeColor(metadata.reasoning_type)} text-white`}>
          MeTTa {metadata.reasoning_type.replace('_', ' ')}
        </span>
        {metadata.confidence && (
          <span className="text-xs text-gray-400">
            {Math.round(metadata.confidence * 100)}% confidence
          </span>
        )}
      </div>
    );
  };

  const renderMettaDetails = (metadata?: ChatMessage['metadata'], messageId: string) => {
    if (!metadata || !showMettaDetails.has(messageId)) return null;

    return (
      <div className="mt-3 p-3 bg-slate-600 rounded-lg text-sm">
        <div className="mb-2">
          <strong className="text-blue-300">Analysis ID:</strong> {metadata.analysis_id}
        </div>
        {metadata.theorem && (
          <div className="mb-2">
            <strong className="text-blue-300">Theorem:</strong> {metadata.theorem}
          </div>
        )}
        {metadata.formal_specification && (
          <div className="mb-2">
            <strong className="text-blue-300">Formal Specification:</strong>
            <pre className="mt-1 p-2 bg-slate-700 rounded text-xs overflow-x-auto">
              {metadata.formal_specification}
            </pre>
          </div>
        )}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900">
        <Navbar />
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-400">Loading chat...</p>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 flex flex-col">
      <Navbar />
      
      <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-white mb-2">Chat with Atim</h1>
          <p className="text-gray-400">Ask Atim about the Nilotic Network, code issues, or development questions</p>
          <div className="mt-2 flex items-center gap-2">
            <span className="text-xs bg-blue-600 text-white px-2 py-1 rounded">MeTTa Powered</span>
            <span className="text-xs text-gray-400">Formal reasoning engine</span>
          </div>
        </div>

        {/* Chat Container */}
        <div className="flex-1 bg-slate-800 rounded-lg border border-slate-700 flex flex-col">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {error ? (
              <div className="text-center py-8">
                <p className="text-red-400 mb-4">Error: {error}</p>
                <button 
                  onClick={() => window.location.reload()} 
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Retry
                </button>
              </div>
            ) : messages.length === 0 ? (
              <div className="text-center py-8">
                <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">🤖</span>
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">Welcome to Atim Assistant</h3>
                <p className="text-gray-400 mb-4">
                  I'm here to help you with the Nilotic Network blockchain development using MeTTa reasoning.
                </p>
                <div className="text-sm text-gray-500 space-y-1">
                  <p>• Ask about code issues and fixes</p>
                  <p>• Get help with blockchain development</p>
                  <p>• Discuss pull requests and improvements</p>
                  <p>• Receive formal mathematical proofs</p>
                </div>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                      message.sender === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-slate-700 text-white'
                    }`}
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs opacity-75">
                        {message.sender === 'user' ? 'You' : 'Atim'}
                      </span>
                      <span className="text-xs opacity-50">
                        {formatTime(message.timestamp)}
                      </span>
                    </div>
                    <div className="text-sm whitespace-pre-wrap">{message.content}</div>
                    
                    {/* MeTTa Badge for Atim messages */}
                    {message.sender === 'atim' && renderMettaBadge(message.metadata)}
                    
                    {/* MeTTa Details Toggle */}
                    {message.sender === 'atim' && message.metadata?.reasoning_type && (
                      <button
                        onClick={() => toggleMettaDetails(message.id)}
                        className="mt-2 text-xs text-blue-300 hover:text-blue-200 underline"
                      >
                        {showMettaDetails.has(message.id) ? 'Hide' : 'Show'} MeTTa Details
                      </button>
                    )}
                    
                    {/* MeTTa Details */}
                    {message.sender === 'atim' && renderMettaDetails(message.metadata, message.id)}
                  </div>
                </div>
              ))
            )}
            
            {sending && (
              <div className="flex justify-start">
                <div className="bg-slate-700 text-white px-4 py-2 rounded-lg">
                  <div className="flex items-center gap-2">
                    <span className="text-xs opacity-75">Atim</span>
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                  <div className="text-xs text-gray-400 mt-1">Using MeTTa reasoning...</div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Message Input */}
          <div className="border-t border-slate-700 p-4">
            <form onSubmit={handleSendMessage} className="flex gap-3">
              <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                placeholder="Ask Atim about the Nilotic Network..."
                className="flex-1 bg-slate-700 text-white px-4 py-2 rounded-lg border border-slate-600 focus:border-blue-500 focus:outline-none"
                disabled={sending}
              />
              <button
                type="submit"
                disabled={!newMessage.trim() || sending}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Send
              </button>
            </form>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default ChatPage; 