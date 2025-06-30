// ui/pages/PluginManifest.tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface PluginInfo {
  plugin: string;
  description: string;
  usage: number;
  last_used?: string;
  tags?: string[];
  category?: string;
  capabilities?: string[];
  requires_llm?: boolean;
  namespace?: string;
  path?: string;
}

const PluginManifest: React.FC = () => {
  const [plugins, setPlugins] = useState<PluginInfo[]>([]);
  const [sortBy, setSortBy] = useState<'name' | 'usage' | 'recent'>('name');

  useEffect(() => {
    // Consider updating the backend to enrich each plugin with tags derived from its path.
    // This would support more intelligent filtering and capability routing.
    axios.get(`/plugins?sort_by=${sortBy}`)
      .then(res => setPlugins(res.data.plugins || []))
      .catch(() => setPlugins([]));
  }, [sortBy]);

  const maxUsage = Math.max(...plugins.map(p => p.usage), 1);

  const isRecentlyUsed = (timestamp?: string) => {
    if (!timestamp) return false;
    const diff = Date.now() - new Date(timestamp).getTime();
    return diff < 5 * 60 * 1000; // 5 minutes
  };

  const grouped = plugins.reduce((acc, plugin) => {
    const categoryFromPath = plugin.path?.split('/')?.slice(-2, -1)[0];
    const inferredCategory = plugin.plugin.includes('/')
      ? plugin.plugin.split('/')[plugin.plugin.split('/').length - 2]
      : plugin.plugin.split('_')[0];
    const autoCategory = plugin.category || categoryFromPath || inferredCategory || 'Uncategorized';
    acc[autoCategory] = acc[autoCategory] || [];

    // Auto-tag from path
    const folderTags = plugin.path?.split('/').slice(0, -1) || [];
    plugin.tags = Array.from(new Set([...(plugin.tags || []), ...folderTags]));

    acc[autoCategory].push(plugin);
    return acc;
  }, {} as Record<string, PluginInfo[]>);

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-semibold">Plugin Manifest</h1>
        <select
          className="border border-gray-300 rounded p-1 text-sm"
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value as 'name' | 'usage' | 'recent')}
        >
          <option value="name">Sort by Name</option>
          <option value="usage">Sort by Usage</option>
          <option value="recent">Sort by Recent</option>
        </select>
      </div>

      {plugins.length === 0 ? (
        <p className="text-gray-600">No plugins found or failed to fetch.</p>
      ) : (
        Object.entries(grouped).map(([category, group], i) => (
          <div key={i} className="mb-6">
            <h3 className="text-xl font-bold mb-2">{category}</h3>
            <ul className="space-y-3">
              {group.map((p, idx) => (
                <li key={idx} className="bg-white shadow rounded p-4 border border-gray-200" title={p.description}>
                  <div className="flex justify-between items-center">
                    <h2 className="font-bold text-lg">{p.plugin}</h2>
                    {isRecentlyUsed(p.last_used) && (
                      <span className="text-green-600 text-xs font-semibold">Recently Used</span>
                    )}
                  </div>
                  <p className="text-sm text-gray-700 mb-1">{p.description}</p>
                  <div className="flex flex-wrap gap-1 mb-1">
                    {(p.tags || []).map((tag, i) => (
                      <span key={i} className="bg-blue-100 text-blue-700 text-xs px-2 py-0.5 rounded-full">
                        {tag}
                      </span>
                    ))}
                  </div>
                  {p.capabilities && (
                    <div className="flex flex-wrap gap-1 mb-1">
                      {p.capabilities.map((cap, i) => (
                        <span key={i} className="bg-purple-100 text-purple-700 text-xs px-2 py-0.5 rounded-full">
                          {cap}
                        </span>
                      ))}
                    </div>
                  )}
                  {p.requires_llm && (
                    <p className="text-xs text-yellow-700 font-medium">Requires LLM</p>
                  )}
                  <div className="h-2 bg-gray-200 rounded overflow-hidden mb-1">
                    <div
                      className="h-full bg-blue-500"
                      style={{ width: `${(p.usage / maxUsage) * 100}%` }}
                    />
                  </div>
                  <p className="text-xs text-gray-500">Used {p.usage} time{p.usage !== 1 ? 's' : ''}</p>
                  {p.last_used && (
                    <p className="text-xs text-gray-400 italic">Last used: {new Date(p.last_used).toLocaleString()}</p>
                  )}
                </li>
              ))}
            </ul>
          </div>
        ))
      )}
    </div>
  );
};

export default PluginManifest;
