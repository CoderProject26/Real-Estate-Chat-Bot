// AccountSettings.jsx
import React from "react";
import { useLocation, Link } from "react-router-dom";

export default function AccountSettings({ manageMode }) {
  const location = useLocation();
  const isManage = manageMode || location.pathname.endsWith("/manage");

  if (isManage) {
    return (
      <div className="p-6 bg-white bg-opacity-80 backdrop-blur-md rounded-2xl shadow-lg max-w-lg mx-auto mt-10">
        <h2 className="text-2xl font-bold mb-6">Manage Account Settings</h2>
        <p>Edit your username, email, and password here.</p>
      </div>
    );
  }

  return (
    <div className="p-6 bg-white bg-opacity-80 backdrop-blur-md rounded-2xl shadow-lg max-w-md mx-auto mt-10">
      <h2 className="text-2xl font-bold mb-4">Account Overview</h2>
      <p>Username: John Doe</p>
      <p>Email: john.doe@example.com</p>
      <Link
        className="mt-4 inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        to="/dashboard/account-settings/manage"
      >
        Manage
      </Link>
    </div>
  );
}