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

const RevenueChart = ({ dailyData }) => {
  if (!dailyData || dailyData.length === 0) {
    return <div className="no-data">Нет данных за период</div>;
  }

  // Преобразуем даты для оси X
  const chartData = dailyData.map(item => ({
    date: format(parseISO(item.date), 'dd.MM'),
    revenue: item.revenue,
    avgCheck: item.orders > 0 ? item.revenue / item.orders : 0,
  }));

  return (
    <div className="chart-container">
      <h3>Выручка по дням</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis yAxisId="left" />
          <YAxis yAxisId="right" orientation="right" />
          <Tooltip />
          <Legend />
          <Line yAxisId="left" type="monotone" dataKey="revenue" stroke="#1890ff" name="Выручка" />
          <Line yAxisId="right" type="monotone" dataKey="avgCheck" stroke="#52c41a" name="Средний чек" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default RevenueChart;