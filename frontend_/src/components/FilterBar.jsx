import React from 'react';

const FilterBar = ({ filters, stores, onFilterChange }) => {
  const handleDateChange = (e) => {
    const { name, value } = e.target;
    onFilterChange({ [name]: value });
  };

  const handleStoreChange = (e) => {
    const value = e.target.value === '' ? null : Number(e.target.value);
    onFilterChange({ store_id: value });
  };

  return (
    <div className="filter-bar">
      <div className="filter-group">
        <label>Дата с:</label>
        <input
          type="date"
          name="date_from"
          value={filters.date_from}
          onChange={handleDateChange}
        />
      </div>
      <div className="filter-group">
        <label>Дата по:</label>
        <input
          type="date"
          name="date_to"
          value={filters.date_to}
          onChange={handleDateChange}
        />
      </div>
      <div className="filter-group">
        <label>Магазин:</label>
        <select value={filters.store_id || ''} onChange={handleStoreChange}>
          <option value="">Все магазины</option>
          {stores.map((store) => (
            <option key={store.id} value={store.id}>
              {store.name}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default FilterBar;