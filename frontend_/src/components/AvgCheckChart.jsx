import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { parseISO, format } from 'date-fns';

const AvgCheckChart = ({ dailyData }) => {
  if (!dailyData || dailyData.length === 0) {
    return <div className="no-data">Нет данных за период</div>;
  }

  const chartData = dailyData.map(item => ({
    date: format(parseISO(item.date), 'dd.MM'),
    avgCheck: item.orders > 0 ? item.revenue / item.orders : 0,
  }));

  return (
    <div className="chart-container">
      <h3>Средний чек по дням</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="avgCheck"
            stroke="#8884d8"
            name="Средний чек"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AvgCheckChart;