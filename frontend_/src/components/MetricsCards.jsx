import React from 'react';

const MetricsCards = ({ totalRevenue, totalOrders, globalAvgCheck }) => {
  return (
    <div className="metrics-cards">
      <div className="card">
        <h3>Общая выручка</h3>
        <p>{totalRevenue.toFixed(2)} ₽</p>
      </div>
      <div className="card">
        <h3>Средний чек</h3>
        <p>{globalAvgCheck.toFixed(2)} ₽</p>
      </div>
      <div className="card">
        <h3>Количество чеков</h3>
        <p>{totalOrders}</p>
      </div>
    </div>
  );
};

export default MetricsCards;