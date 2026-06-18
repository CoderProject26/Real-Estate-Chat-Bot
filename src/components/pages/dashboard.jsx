import { useState } from 'react';

function Dashboard() {
  const [activeTab, setActiveTab] = useState('dashboard'); // default tab

  return (
    <div className="flex">
      {/* Sidebar */}
      <div className="w-64 bg-gray-800 text-white p-4">
        <ul>
          <li
            className="cursor-pointer p-2 hover:bg-gray-700"
            onClick={() => setActiveTab('dashboard')}
          >
            Dashboard
          </li>
          <li
            className="cursor-pointer p-2 hover:bg-gray-700"
            onClick={() => setActiveTab('comingSoon')}
          >
            Coming Soon
          </li>
        </ul>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-4">
        {activeTab === 'dashboard' && <h1>Dashboard Home</h1>}
        {activeTab === 'comingSoon' && <ComingSoonGraph />}
      </div>
    </div>
  );
}

export default Dashboard;