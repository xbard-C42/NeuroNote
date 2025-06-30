# core/plugin_registry.py
from typing import List, Dict, Any
from core.plugin import Plugin, EchoPlugin

# Plugin registry (could be made dynamic via importlib)
registered_plugins: List[Plugin] = [
    EchoPlugin()
    # Future: Add FileSummaryPlugin(), MemorySearchPlugin(), etc.
]

def get_applicable_plugins(agent: str, input_text: str, context: Dict[str, Any]) -> List[Plugin]:
    return [plugin for plugin in registered_plugins if plugin.applies(input_text, context)]

def execute_plugin_chain(plugins: List[Plugin], input_text: str, context: Dict[str, Any]) -> str:
    results = []
    for plugin in plugins:
        try:
            result = plugin.execute(input_text, context)
            results.append(f"[{plugin.name}] {result}")
        except Exception as e:
            results.append(f"[{plugin.name}] Error: {str(e)}")
    return "\n".join(results)
