import { LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";

const data = [
  { month: 'Jan', value: 30 },
  { month: 'Feb', value: 45 },
  { month: 'Mar', value: 50 },
];

export default function ComingSoonGraph() {
  return (
    <div className="p-4 bg-white rounded shadow">
      <h2 className="text-xl font-bold mb-4">Coming Soon Trends</h2>
      <LineChart width={400} height={300} data={data}>
        <Line type="monotone" dataKey="value" stroke="#8884d8" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
      </LineChart>
    </div>
  );
}