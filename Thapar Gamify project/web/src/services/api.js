import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Authentication
export const authService = {
  register: (email, username, password, fullName, location) =>
    api.post('/auth/register', { email, username, password, full_name: fullName, location }),
  login: (email, password) =>
    api.post('/auth/login', { email, password }),
};

// User
export const userService = {
  getProfile: (userId) =>
    api.get(`/users/${userId}`),
  updateProfile: (userId, data) =>
    api.put(`/users/${userId}`, data),
  getStats: (userId) =>
    api.get(`/users/${userId}`),
};

// Leaderboard
export const leaderboardService = {
  getDailyLeaderboard: (limit = 100, userId = null) =>
    api.get('/leaderboard/daily', { params: { limit, user_id: userId } }),
  getWeeklyLeaderboard: (limit = 100, userId = null) =>
    api.get('/leaderboard/weekly', { params: { limit, user_id: userId } }),
  getAllTimeLeaderboard: (limit = 100, userId = null) =>
    api.get('/leaderboard/all-time', { params: { limit, user_id: userId } }),
  getUserRank: (userId, period = 'all_time') =>
    api.get(`/users/${userId}/rank`, { params: { period } }),
};

// Recommendations
export const recommendationService = {
  getTaskRecommendations: (userId, limit = 5) =>
    api.get(`/users/${userId}/recommendations/tasks`, { params: { limit } }),
  getQuizRecommendations: (userId, limit = 3) =>
    api.get(`/users/${userId}/recommendations/quizzes`, { params: { limit } }),
  getEngagement: (userId) =>
    api.get(`/users/${userId}/engagement`),
  getSimilarUsers: (userId, limit = 5) =>
    api.get(`/users/${userId}/similar-users`, { params: { limit } }),
};

// Payments
export const paymentService = {
  createOrder: (userId, rewardId, amount) =>
    api.post('/payments/create-order', { user_id: userId, reward_id: rewardId, amount }),
  verifyPayment: (userId, paymentId, orderId, signature, rewardId) =>
    api.post('/payments/verify', { 
      user_id: userId, 
      payment_id: paymentId, 
      order_id: orderId, 
      signature, 
      reward_id: rewardId 
    }),
};

export default api;
