import React, { useState, useEffect } from 'react';
import {
  fetchRevenue,
  fetchAvgCheck,
  fetchCustomerActivity,
  fetchTopProducts,
  fetchRFM,
} from './api';
import FilterBar from './components/FilterBar';
import MetricsCards from './components/MetricsCards';
import RevenueChart from './components/RevenueChart';
import AvgCheckChart from './components/AvgCheckChart';
import CustomerActivityChart from './components/CustomerActivityChart';
import TopProductsTable from './components/TopProductsTable';
import RFMSegmentation from './components/RFMSegmentation';
import './index.css';

const DEFAULT_DATE_FROM = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
  .toISOString()
  .split('T')[0];
const DEFAULT_DATE_TO = new Date().toISOString().split('T')[0];

function App() {
  const [filters, setFilters] = useState({
    date_from: DEFAULT_DATE_FROM,
    date_to: DEFAULT_DATE_TO,
    store_id: null,
  });
  const [activityGroupBy, setActivityGroupBy] = useState('day');
  const [stores, setStores] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [revenueData, setRevenueData] = useState(null);
  const [avgCheckData, setAvgCheckData] = useState(null);
  const [activityData, setActivityData] = useState([]);
  const [topProducts, setTopProducts] = useState([]);
  const [rfmData, setRfmData] = useState([]);

  const loadAllData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [revenueRes, avgRes, activityRes, topRes, rfmRes] = await Promise.all([
        fetchRevenue(filters),
        fetchAvgCheck(filters),
        fetchCustomerActivity(filters, activityGroupBy),
        fetchTopProducts(filters, 10, 'quantity'),
        fetchRFM(filters),
      ]);

      setRevenueData(revenueRes.data);
      setAvgCheckData(avgRes.data);
      setActivityData(activityRes.data);
      setTopProducts(topRes.data);
      setRfmData(rfmRes.data);

      if (revenueRes.data?.stores) {
        const uniqueStores = revenueRes.data.stores.map((s) => ({
          id: s.store_id,
          name: s.store_name || `Магазин ${s.store_id}`,
        }));
        setStores(uniqueStores);
      }
    } catch (err) {
      setError(err.message || 'Ошибка загрузки данных');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAllData();
    // eslint-disable-next-line
  }, [filters, activityGroupBy]);

  const handleFilterChange = (newFilters) => {
    setFilters((prev) => ({ ...prev, ...newFilters }));
  };

  if (loading) return <div className="loading">Загрузка...</div>;
  if (error) return <div className="error">Ошибка: {error}</div>;

  return (
    <div className="app">
      <header>
        <h1>Аналитический дашборд</h1>
        <FilterBar
          filters={filters}
          stores={stores}
          onFilterChange={handleFilterChange}
        />
      </header>
      <main>
        <MetricsCards
          totalRevenue={revenueData?.total_revenue || 0}
          totalOrders={revenueData?.total_orders || 0}
          globalAvgCheck={avgCheckData?.global_avg_check || 0}
        />

        <div className="full-width-chart">
          <RevenueChart dailyData={revenueData?.daily_data || []} />
        </div>

        {/* Два графика в ряд */}
        <div className="charts-row">
          <AvgCheckChart dailyData={revenueData?.daily_data || []} />
          <CustomerActivityChart
            data={activityData}
            groupBy={activityGroupBy}
            onGroupByChange={setActivityGroupBy}
          />
        </div>

        <div className="bottom-row">
          <TopProductsTable data={topProducts} />
          <RFMSegmentation data={rfmData} />
        </div>
      </main>
    </div>
  );
}

export default App;