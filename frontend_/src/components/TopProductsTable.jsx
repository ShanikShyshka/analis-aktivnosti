import React from 'react';

const TopProductsTable = ({ data }) => {
  if (!data || data.length === 0) {
    return <div className="no-data">Нет данных по товарам</div>;
  }

  return (
    <div className="table-container">
      <h3>Топ-10 товаров</h3>
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Название</th>
            <th>Кол-во продаж</th>
            <th>Выручка</th>
          </tr>
        </thead>
        <tbody>
          {data.map((product, index) => (
            <tr key={product.product_id || index}>
              <td>{index + 1}</td>
              <td>{product.product_name || 'Неизвестно'}</td>
              <td>{product.quantity_sold}</td>
              <td>{product.revenue?.toFixed(2)} ₽</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TopProductsTable;
