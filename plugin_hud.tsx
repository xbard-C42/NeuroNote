// ui/components/PluginHUD.tsx
import React from 'react';

interface PluginHUDProps {
  activePlugins: { plugin: string; success: boolean; output?: string; error?: string }[];
}

const PluginHUD: React.FC<PluginHUDProps> = ({ activePlugins }) => {
  if (!activePlugins.length) return null;

  return (
    <div className="fixed top-4 right-4 z-50 bg-white shadow-lg border border-gray-300 rounded-lg p-3 text-sm w-80">
      <h3 className="font-bold text-gray-800 mb-2">Active Plugins</h3>
      <ul className="space-y-1">
        {activePlugins.map((plugin, idx) => (
          <li key={idx} className={`text-${plugin.success ? 'green' : 'red'}-700`}>
            <strong>{plugin.plugin}</strong> {plugin.success ? '✓' : '✕'}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PluginHUD;
