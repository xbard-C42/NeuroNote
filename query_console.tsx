// ui/pages/QueryConsole.tsx
import React, { useState } from 'react';
import axios from 'axios';

const QueryConsole = () => {
  const [userId, setUserId] = useState('default');
  const [inputText, setInputText] = useState('');
  const [response, setResponse] = useState<any>(null);

  const submitQuery = async () => {
    try {
      const res = await axios.post('/query', {
        user_id: userId,
        input_text: inputText,
        context: {}
      });
      setResponse(res.data);
    } catch (err) {
      setResponse({ error: 'Failed to fetch response' });
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">LLM Query Console</h2>
      <input
        type="text"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
        placeholder="User ID"
        className="border rounded px-2 py-1 mr-2"
      />
      <textarea
        rows={4}
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Enter your query..."
        className="w-full border rounded px-2 py-1 mt-2"
      />
      <button
        onClick={submitQuery}
        className="bg-blue-600 text-white px-4 py-2 mt-3 rounded"
      >
        Send
      </button>
      {response && (
        <div className="mt-4">
          <h3 className="font-semibold">Response</h3>
          <pre className="bg-gray-100 p-3 rounded overflow-x-auto text-sm">
            {JSON.stringify(response, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default QueryConsole;
