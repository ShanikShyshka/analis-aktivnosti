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

const CustomerActivityChart = ({ data, groupBy, onGroupByChange }) => {
  const chartData = data
    .filter((item) => item.timestamp)
    .map((item) => {
      const date = parseISO(item.timestamp);
      const label = groupBy === 'hour'
        ? format(date, 'dd.MM HH:mm')
        : format(date, 'dd.MM');
      return {
        date: label,
        customers: item.customer_count || 0,
      };
    });

  if (chartData.length === 0) {
    return (
      <div className="chart-container">
        <h3>Покупательская активность</h3>
        <div className="no-data">Нет данных за период</div>
      </div>
    );
  }

  return (
    <div className="chart-container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3>Покупательская активность</h3>
        <div className="group-switcher">
          <button
            className={groupBy === 'day' ? 'active' : ''}
            onClick={() => onGroupByChange('day')}
          >
            День
          </button>
          <button
            className={groupBy === 'hour' ? 'active' : ''}
            onClick={() => onGroupByChange('hour')}
          >
            Час
          </button>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="customers"
            stroke="#82ca9d"
            name="Кол-во покупателей"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default CustomerActivityChart;