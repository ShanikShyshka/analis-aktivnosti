import React, { useMemo } from 'react';
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

const COLORS = [
  '#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#AF19FF',
  '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
  '#FF9F40', '#C9CBCF', '#FFB1C1', '#9AD0F5', '#FFD8B1',
  '#B5EAD7', '#FF9AA2', '#E2F0CB', '#F2B5D4', '#D4A5A5',
  '#A8D8EA', '#AA96DA', '#FCBAD3', '#FFFFD2', '#B5EAD7',
  '#C7CEEA', '#F5B7B1', '#D5F5E3', '#FADBD8'
];

const RFMSegmentation = ({ data }) => {

  const chartData = useMemo(() => {
    if (!data || data.length === 0) return [];

    // Проверяем, есть ли уже агрегированные данные
    if (data[0]?.customer_segment && data[0]?.customer_count) {
      return data.map(item => ({
        name: item.customer_segment,
        value: item.customer_count,
      }));
    }

    const map = new Map();
    data.forEach(item => {
      const seg = item.segment || 'Unknown';
      map.set(seg, (map.get(seg) || 0) + 1);
    });
    return Array.from(map.entries()).map(([name, value]) => ({ name, value }));
  }, [data]);

  const sortedData = useMemo(() => [...chartData].sort((a, b) => b.value - a.value), [chartData]);
  const top10 = sortedData.slice(0, 10);

  if (chartData.length === 0) {
    return <div className="no-data">Нет RFM-данных</div>;
  }

  return (
    <div className="rfm-container">
      <h3>RFM-сегментация</h3>
      <div className="rfm-chart">
        <ResponsiveContainer width="100%" height={280}>
          <PieChart>
            <Pie
              data={top10}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) =>
                `${name} (${(percent * 100).toFixed(0)}%)`
              }
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {top10.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Pie>
            <Tooltip formatter={(value) => `${value} клиентов`} />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="rfm-table">
        <table>
          <thead>
            <tr>
              <th>Сегмент</th>
              <th>Кол-во клиентов</th>
              <th>Доля, %</th>
            </tr>
          </thead>
          <tbody>
            {chartData.map((item) => (
              <tr key={item.name}>
                <td>{item.name}</td>
                <td>{item.value}</td>
                <td>{(item.value / chartData.reduce((acc, d) => acc + d.value, 0) * 100).toFixed(2)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RFMSegmentation;