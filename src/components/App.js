// App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from "react-router-dom";
import ComingSoonGraph from "./components/ComingSoonGraph";
import PropertyTrends from "./components/PropertyTrends";
import AccountSettings from "./components/AccountSettings";

function DashboardHome() {
  return <h1 className="text-2xl font-bold">Welcome to Dashboard</h1>;
}

function App() {
  return (
    <Router>
      <div className="flex h-screen">
        {/* Sidebar */}
        <div className="w-64 bg-gray-800 text-white p-4">
          <h2 className="text-xl font-bold mb-4">Real Estate Dashboard</h2>
          <ul>
            <li className="mb-2">
              <Link className="block p-2 rounded hover:bg-gray-700" to="/dashboard">
                Dashboard
              </Link>
            </li>
            <li className="mb-2">
              <Link className="block p-2 rounded hover:bg-gray-700" to="/dashboard/coming-soon">
                Coming Soon
              </Link>
            </li>
            <li className="mb-2">
              <Link className="block p-2 rounded hover:bg-gray-700" to="/dashboard/property-trends">
                Property Trends
              </Link>
            </li>
            <li className="mb-2">
              <Link className="block p-2 rounded hover:bg-gray-700" to="/dashboard/account-settings">
                Account Settings
              </Link>
            </li>
          </ul>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-6 bg-gray-100 dark:bg-gray-900 overflow-auto">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" />} />
            <Route path="/dashboard" element={<DashboardHome />} />
            <Route path="/dashboard/coming-soon" element={<ComingSoonGraph />} />
            <Route path="/dashboard/property-trends" element={<PropertyTrends />} />
            <Route path="/dashboard/account-settings" element={<AccountSettings />} />
            {/* Optional: nested Manage page */}
            <Route
              path="/dashboard/account-settings/manage"
              element={<AccountSettings manageMode={true} />}
            />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;