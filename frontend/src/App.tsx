import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store/useAuthStore';
import { MainLayout } from './components/layout/MainLayout';
import { ExecutiveDashboard } from './features/dashboard/ExecutiveDashboard';
import { PipelineListView } from './features/pipelines/PipelineListView';
import { DAGCanvas } from './features/builder/DAGCanvas';
import { DataSourceListView } from './features/sources/DataSourceListView';
import { LoginView } from './features/auth/LoginView';

export const App: React.FC = () => {
  const { isAuthenticated } = useAuthStore();

  if (!isAuthenticated) {
    return <LoginView />;
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<ExecutiveDashboard />} />
          <Route path="pipelines" element={<PipelineListView />} />
          <Route path="builder" element={<DAGCanvas />} />
          <Route path="sources" element={<DataSourceListView />} />
          <Route path="monitoring" element={<ExecutiveDashboard />} />
          <Route path="audit" element={<ExecutiveDashboard />} />
          <Route path="settings" element={<ExecutiveDashboard />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
