import React from 'react';
import { Link } from 'react-router-dom';
import AuthStatusBanner from './AuthStatusBanner';

const Hero: React.FC = () => {
  return (
    <div className="bg-gradient-to-b from-slate-900 to-slate-800 text-white">
      <AuthStatusBanner />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32">
        <div className="lg:grid lg:grid-cols-12 lg:gap-8">
          <div className="lg:col-span-7 xl:col-span-6">
            <h1 className="text-4xl tracking-tight font-extrabold sm:text-5xl md:text-6xl">
              <span className="block">Meet Atim,</span>
              <span className="block text-blue-400 mt-2">Your AI Blockchain Assistant</span>
            </h1>
            <p className="mt-6 text-xl text-gray-300">
              Enhancing the Nilotic Network blockchain with AI-powered code analysis,
              automated testing, and collaborative development through a hybrid approach
              that keeps humans in control.
            </p>
            <div className="mt-10 flex flex-col sm:flex-row gap-4">
              <Link
                to="/register"
                className="rounded-md shadow px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium text-center"
              >
                Get Started
              </Link>
              <Link
                to="/kanban"
                className="rounded-md px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white font-medium text-center"
              >
                View Project Board
              </Link>
            </div>
          </div>
          <div className="mt-12 lg:mt-0 lg:col-span-5 xl:col-span-6">
            <div className="bg-slate-700 rounded-xl shadow-xl overflow-hidden">
              <div className="px-6 py-8">
                <div className="flex items-center pb-3 border-b border-slate-600">
                  <div className="flex space-x-2">
                    <div className="w-3 h-3 rounded-full bg-red-500"></div>
                    <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                    <div className="w-3 h-3 rounded-full bg-green-500"></div>
                  </div>
                  <div className="flex-1 text-center text-sm font-mono text-gray-300">src/main.cpp</div>
                </div>
                <pre className="mt-4 text-sm text-gray-300 font-mono">
                  <code>
{`// Supply calculation bug fix
- totalSupply = blockchain.getChain().size() * 10.0;
+ totalSupply = blockchain.getCurrentSupply();

// Fixed by Atim AI Assistant
// Accurately reports circulating SLW tokens
// including premined supply and block rewards`}
                  </code>
                </pre>
                <div className="mt-4 flex justify-end">
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-800 text-green-100">
                    Pull Request #5: Approved ✓
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;
