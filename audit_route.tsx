// ui/pages/AuditPage.tsx
import React from 'react';
import AuditViewer from '../components/AuditViewer';

const AuditPage = () => {
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <h1 className="text-2xl font-semibold mb-4">Orchestration Audit Logs</h1>
      <AuditViewer />
    </div>
  );
};

export default AuditPage;
