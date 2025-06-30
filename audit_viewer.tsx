// ui/components/AuditViewer.tsx
import React, { useState } from 'react';
import axios from 'axios';

const AuditViewer = () => {
  const [traceId, setTraceId] = useState('');
  const [trace, setTrace] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchTrace = async () => {
    try {
      const res = await axios.get(`/audit/${traceId}`);
      setTrace(res.data.trace);
      setError(null);
    } catch (err) {
      setTrace(null);
      setError('Trace not found or fetch error');
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-2">Audit Log Viewer</h2>
      <input
        type="text"
        value={traceId}
        onChange={(e) => setTraceId(e.target.value)}
        placeholder="Enter Trace ID"
        className="border px-2 py-1 rounded mr-2"
      />
      <button onClick={fetchTrace} className="bg-blue-500 text-white px-3 py-1 rounded">
        Fetch
      </button>
      {error && <p className="text-red-600 mt-2">{error}</p>}
      {trace && (
        <div className="mt-4">
          <pre className="bg-gray-100 p-3 rounded overflow-x-auto text-sm">
            {JSON.stringify(trace, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default AuditViewer;
