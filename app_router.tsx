// ui/main.tsx
import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AuditPage from './pages/AuditPage';

const App = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/audit" element={<AuditPage />} />
      <Route path="*" element={<div className="p-4">Welcome to NeuroNote!</div>} />
    </Routes>
  </BrowserRouter>
);

const root = createRoot(document.getElementById('root')!);
root.render(<App />);
