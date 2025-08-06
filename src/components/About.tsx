import React from 'react';

const About: React.FC = () => {
  return (
    <div className="py-16 bg-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-white">About the Nilotic Network & SLW Token</h2>
          <p className="mt-4 text-xl text-gray-300 max-w-3xl mx-auto">
            A lightweight C++ blockchain designed with focus on simplicity, performance, and scalability
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <h3 className="text-2xl font-semibold text-white mb-4">Nilotic Network</h3>
            <div className="space-y-4 text-gray-300">
              <p>
                The Nilotic Network is a lightweight Proof-of-Stake (PoS) blockchain built in C++.
                It powers the SLW token and serves as the Web3 backend for the Nilotic Wallet.
              </p>
              <p>
                The core components include a Crow-based HTTP API for interacting with the blockchain,
                a consensus mechanism for validating transactions, and a token management system.
              </p>
              <div className="mt-6">
                <a
                  href="https://github.com/Emmanuel-Odero/nilotic-network"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center text-blue-400 hover:text-blue-300"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                  </svg>
                  View on GitHub
                </a>
              </div>
            </div>
          </div>

          <div className="bg-slate-700 rounded-lg p-6 shadow-lg">
            <h3 className="text-2xl font-semibold text-white mb-4">SLW Token</h3>
            <div className="space-y-4">
              <div className="flex items-center border-b border-slate-600 pb-3">
                <div className="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold">
                  SLW
                </div>
                <div className="ml-4">
                  <h4 className="text-white font-medium">Nilotic SLW</h4>
                  <p className="text-gray-400 text-sm">Standard Web3 Token</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 mt-4">
                <div>
                  <h5 className="text-gray-400 text-sm">Total Supply</h5>
                  <p className="text-white font-mono">555,000,000 SLW</p>
                </div>
                <div>
                  <h5 className="text-gray-400 text-sm">Premined</h5>
                  <p className="text-white font-mono">35% (194,250,000 SLW)</p>
                </div>
                <div>
                  <h5 className="text-gray-400 text-sm">Block Reward</h5>
                  <p className="text-white font-mono">5 SLW</p>
                </div>
                <div>
                  <h5 className="text-gray-400 text-sm">Consensus</h5>
                  <p className="text-white font-mono">Proof of Stake (PoS)</p>
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-slate-600">
                <h5 className="text-white font-medium mb-2">Token Distribution</h5>
                <div className="w-full bg-slate-800 rounded-full h-4">
                  <div className="bg-blue-600 h-4 rounded-full" style={{ width: '35%' }}></div>
                </div>
                <div className="flex justify-between text-xs text-gray-400 mt-1">
                  <span>Premined (35%)</span>
                  <span>Mining Rewards (65%)</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
