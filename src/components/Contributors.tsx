import React from 'react';

interface ContributorProps {
  name: string;
  role: string;
  github: string;
  image?: string;
}

const Contributor: React.FC<ContributorProps> = ({ name, role, github, image }) => {
  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 flex flex-col items-center text-center">
      <div className="w-24 h-24 rounded-full bg-blue-700 mb-4 overflow-hidden">
        {image ? (
          <img src={image} alt={name} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-white text-2xl font-bold">
            {name.split(' ').map(n => n[0]).join('')}
          </div>
        )}
      </div>
      <h3 className="text-white font-medium text-lg">{name}</h3>
      <p className="text-gray-400 text-sm mb-4">{role}</p>
      <a
        href={`https://github.com/${github}`}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-400 hover:text-blue-300 inline-flex items-center text-sm"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
        </svg>
        @{github}
      </a>
    </div>
  );
};

const Contributors: React.FC = () => {
  return (
    <div className="py-16 bg-slate-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-white">Contributors</h2>
          <p className="mt-4 text-xl text-gray-300 max-w-3xl mx-auto">
            The talented team behind the Nilotic Network and Atim Assistant
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <Contributor
            name="Emmanuel Odero"
            role="Lead Developer - Nilotic Network"
            github="Emmanuel-Odero"
          />

          <Contributor
            name="Atim"
            role="AI Assistant"
            github="nilotic-network/atim"
          />

          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 flex flex-col items-center text-center">
            <div className="w-24 h-24 rounded-full bg-slate-700 mb-4 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
              </svg>
            </div>
            <h3 className="text-white font-medium text-lg">Join The Team</h3>
            <p className="text-gray-400 text-sm mb-4">Contribute to the Nilotic Network</p>
            <div className="mt-2">
              <a
                href="https://github.com/Emmanuel-Odero/nilotic-network"
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm"
              >
                Fork on GitHub
              </a>
            </div>
          </div>
        </div>

        <div className="mt-16 text-center">
          <h3 className="text-xl font-semibold text-white mb-4">Support the Project</h3>
          <p className="text-gray-300 mb-6 max-w-2xl mx-auto">
            The Nilotic Network is an open-source project maintained by volunteers.
            Consider supporting us to help sustain development.
          </p>
          <div className="inline-flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="#"
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-md text-white font-medium"
            >
              Donate SLW Tokens
            </a>
            <a
              href="https://github.com/sponsors/"
              target="_blank"
              rel="noopener noreferrer"
              className="px-6 py-3 bg-pink-600 hover:bg-pink-700 rounded-md text-white font-medium"
            >
              GitHub Sponsors
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Contributors;
