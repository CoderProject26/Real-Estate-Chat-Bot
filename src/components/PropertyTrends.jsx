import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const data = [
  { month: "Jan", sales: 120, listings: 90 },
  { month: "Feb", sales: 200, listings: 150 },
  { month: "Mar", sales: 150, listings: 100 },
  { month: "Apr", sales: 250, listings: 200 },
  { month: "May", sales: 300, listings: 250 },
];

export default function PropertyTrends() {
  return (
    <div className="p-6 bg-white rounded-xl shadow-md">
      <h2 className="text-2xl font-bold mb-4">Property Trends</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="sales" stroke="#8884d8" strokeWidth={2} />
          <Line type="monotone" dataKey="listings" stroke="#82ca9d" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}