// PromptPlanPreview.tsx
import React, { useState } from 'react';
import axios from 'axios';

interface PlanStep {
  role: string;
  plugin: string;
  prompt: string;
  llm_route: string;
  dependencies: string[];
  status?: 'active' | 'pending' | 'fallback';
  disabled?: boolean;
}

interface PlanResponse {
  plan: PlanStep[];
  audit_trail: any[];
}

const statusColor = {
  active: 'bg-green-100 border-green-400',
  pending: 'bg-yellow-100 border-yellow-400',
  fallback: 'bg-red-100 border-red-400',
  default: 'bg-gray-100 border-gray-300',
};

const PromptPlanPreview: React.FC = () => {
  const [task, setTask] = useState('');
  const [plan, setPlan] = useState<PlanStep[]>([]);
  const [auditTrail, setAuditTrail] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [useMock, setUseMock] = useState(false);
  const [executionLog, setExecutionLog] = useState<any[]>([]);

  const handleGeneratePlan = async () => {
    setLoading(true);
    try {
      const url = useMock ? '/mock/orchestrator/plan' : '/orchestrator/plan';
      const payload = useMock ? {} : { task };
      const response = await axios.post<PlanResponse>(url, payload);
      const enrichedPlan = response.data.plan.map((step, i) => ({
        ...step,
        status: i === 0 ? 'active' : i === 1 ? 'pending' : 'fallback',
        disabled: false,
      }));
      setPlan(enrichedPlan);
      setAuditTrail(response.data.audit_trail);
    } catch (error) {
      console.error('Failed to fetch plan', error);
    } finally {
      setLoading(false);
    }
  };

  const handleReorder = (index: number, direction: 'up' | 'down') => {
    const newPlan = [...plan];
    const target = direction === 'up' ? index - 1 : index + 1;
    if (target < 0 || target >= plan.length) return;
    [newPlan[index], newPlan[target]] = [newPlan[target], newPlan[index]];
    setPlan(newPlan);
  };

  const toggleDisable = (index: number) => {
    const newPlan = [...plan];
    newPlan[index].disabled = !newPlan[index].disabled;
    setPlan(newPlan);
  };

  const handleExport = () => {
    const filteredPlan = plan.filter((step) => !step.disabled);
    const blob = new Blob([JSON.stringify({ plan: filteredPlan }, null, 2)], {
      type: 'application/json',
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'prompt_plan.json';
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  };

  const handleExecute = async () => {
    try {
      const response = await axios.post('/orchestrator/execute', {
        plan,
      });
      setExecutionLog(response.data.execution_log);
    } catch (error) {
      console.error('Execution failed', error);
    }
  };

  return (
    <div className="p-4 max-w-3xl mx-auto">
      <h1 className="text-xl font-bold mb-4">Prompt Plan Preview</h1>
      <div className="mb-2">
        <label className="inline-flex items-center mr-4">
          <input
            type="checkbox"
            checked={useMock}
            onChange={() => setUseMock(!useMock)}
            className="mr-2"
          />
          Use Mock Data
        </label>
      </div>
      <textarea
        className="w-full border p-2 rounded text-sm mb-2"
        placeholder="Describe your task..."
        rows={3}
        value={task}
        onChange={(e) => setTask(e.target.value)}
        disabled={useMock}
      />
      <div className="flex space-x-2">
        <button
          onClick={handleGeneratePlan}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
          disabled={loading}
        >
          {loading ? 'Generating...' : 'Generate Plan'}
        </button>
        <button
          onClick={handleExport}
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
        >
          Export JSON
        </button>
        <button
          onClick={handleExecute}
          className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded"
        >
          Execute Plan
        </button>
      </div>

      <div className="mt-6">
        {plan.map((step, index) => (
          <div
            key={index}
            className={`border rounded p-4 mb-4 relative ${statusColor[step.status ?? 'default']} ${step.disabled ? 'opacity-50' : ''}`}
          >
            <div className="flex justify-between">
              <p><strong>Role:</strong> {step.role}</p>
              <span className="text-xs font-medium text-gray-600 uppercase">
                {step.status || 'default'}
              </span>
            </div>
            <p><strong>Plugin:</strong> {step.plugin}</p>
            <p><strong>LLM:</strong> {step.llm_route}</p>
            <p><strong>Dependencies:</strong> {step.dependencies.join(', ')}</p>
            <details className="mt-2">
              <summary className="cursor-pointer text-blue-700">Prompt</summary>
              <pre className="whitespace-pre-wrap text-sm mt-1 bg-white p-2 rounded border">
                {step.prompt}
              </pre>
            </details>
            <div className="mt-3 flex space-x-2">
              <button
                onClick={() => handleReorder(index, 'up')}
                className="text-xs bg-gray-200 px-2 py-1 rounded"
              >⬆ Up</button>
              <button
                onClick={() => handleReorder(index, 'down')}
                className="text-xs bg-gray-200 px-2 py-1 rounded"
              >⬇ Down</button>
              <button
                onClick={() => toggleDisable(index)}
                className="text-xs bg-red-100 px-2 py-1 rounded"
              >{step.disabled ? 'Enable' : 'Disable'}</button>
            </div>
          </div>
        ))}
      </div>

      {executionLog.length > 0 && (
        <div className="mt-10">
          <h2 className="text-lg font-semibold mb-2">Execution Log</h2>
          <div className="space-y-2">
            {executionLog.map((log, i) => (
              <div key={i} className="border p-3 rounded bg-white">
                <div className="text-sm text-gray-700">🔧 <strong>{log.plugin}</strong> via <code>{log.llm_route}</code></div>
                {log.skipped ? (
                  <div className="text-red-500">Step skipped</div>
                ) : (
                  <pre className="whitespace-pre-wrap text-sm mt-1">{log.output}</pre>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default PromptPlanPreview;
