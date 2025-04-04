import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from 'antd';
import Navigation from './components/Navigation';
import Dashboard from './pages/Dashboard';
import ContentGenerator from './pages/ContentGenerator';
import History from './pages/History';
import Login from './pages/Login';
import PrivateRoute from './components/PrivateRoute';

const { Header, Content } = Layout;

function App() {
  return (
    <BrowserRouter>
      <Layout style={{ minHeight: '100vh' }}>
        <Header>
          <Navigation />
        </Header>
        <Content style={{ padding: '24px' }}>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            } />
            <Route path="/generate" element={
              <PrivateRoute>
                <ContentGenerator />
              </PrivateRoute>
            } />
            <Route path="/history" element={
              <PrivateRoute>
                <History />
              </PrivateRoute>
            } />
          </Routes>
        </Content>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
