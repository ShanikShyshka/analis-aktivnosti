import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
});

export const fetchRevenue = (filters) =>
  api.get('/api/analytics/revenue', { params: filters });

export const fetchAvgCheck = (filters) =>
  api.get('/api/analytics/avg-check', { params: filters });



export const fetchTopProducts = (filters, limit = 10, sortBy = 'quantity') =>
  api.get('/api/analytics/top-products', {
    params: { ...filters, limit, sort_by: sortBy },
  });

export const fetchRFM = (filters) =>
  api.get('/api/analytics/rfm', { params: filters });

export const fetchCustomerActivity = (filters, groupBy = 'day') =>
  api.get('/api/analytics/customer-activity', {
    params: { ...filters, group_by: groupBy },
  });