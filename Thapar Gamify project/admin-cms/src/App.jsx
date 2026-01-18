import React from 'react';
import { Admin, Resource, ListGuesser, EditGuesser, CreateGuesser } from 'react-admin';
import { fetchUtils } from 'ra-core';
import jsonServerProvider from 'ra-data-json-server';

// Custom API provider
const httpClient = (url, options = {}) => {
  const token = localStorage.getItem('accessToken');
  if (!token) return fetchUtils.fetchJson(url, options);

  const customHeaders = new Headers({
    ...options.headers,
    Authorization: `Bearer ${token}`,
  });
  return fetchUtils.fetchJson(url, { ...options, headers: customHeaders });
};

// Create data provider pointing to your backend
const dataProvider = jsonServerProvider('http://localhost:8000/api/v1', httpClient);

// Task List Component
const TaskList = (props) => (
  <div>
    <h1>Manage Tasks</h1>
    {/* Task management UI here */}
  </div>
);

// SDG Goal List Component
const SDGGoalList = (props) => (
  <div>
    <h1>SDG Goals Management</h1>
    {/* SDG goals management UI here */}
  </div>
);

// Quiz Management Component
const QuizList = (props) => (
  <div>
    <h1>Manage Quizzes</h1>
    {/* Quiz management UI here */}
  </div>
);

// Reward Management Component
const RewardList = (props) => (
  <div>
    <h1>Manage Rewards</h1>
    {/* Reward management UI here */}
  </div>
);

// User Management Component
const UserList = (props) => (
  <div>
    <h1>Manage Users</h1>
    {/* User management UI here */}
  </div>
);

// Dashboard Component
const Dashboard = () => (
  <div style={{ padding: 20 }}>
    <h1>Gamify SDG Admin Panel</h1>
    <div style={{ marginTop: 20 }}>
      <h2>Quick Stats</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 20 }}>
        <div style={{ padding: 20, backgroundColor: '#e3f2fd', borderRadius: 8 }}>
          <h3>Total Users</h3>
          <p style={{ fontSize: 28, fontWeight: 'bold' }}>--</p>
        </div>
        <div style={{ padding: 20, backgroundColor: '#e8f5e9', borderRadius: 8 }}>
          <h3>Active Users</h3>
          <p style={{ fontSize: 28, fontWeight: 'bold' }}>--</p>
        </div>
        <div style={{ padding: 20, backgroundColor: '#fff3e0', borderRadius: 8 }}>
          <h3>Total Points Awarded</h3>
          <p style={{ fontSize: 28, fontWeight: 'bold' }}>--</p>
        </div>
        <div style={{ padding: 20, backgroundColor: '#fce4ec', borderRadius: 8 }}>
          <h3>Tasks Completed</h3>
          <p style={{ fontSize: 28, fontWeight: 'bold' }}>--</p>
        </div>
      </div>
    </div>
  </div>
);

export default function App() {
  return (
    <Admin dataProvider={dataProvider} dashboard={Dashboard}>
      <Resource name="users" list={UserList} />
      <Resource name="tasks" list={TaskList} />
      <Resource name="sdg-goals" list={SDGGoalList} />
      <Resource name="quizzes" list={QuizList} />
      <Resource name="rewards" list={RewardList} />
    </Admin>
  );
}
