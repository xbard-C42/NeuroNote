# core/plugin_registry.py
from typing import List, Dict, Any, Type
from core.plugin import Plugin
import pkgutil
import importlib
import inspect
import core
import time

# Dynamically load all Plugin subclasses from core modules
registered_plugins: List[Plugin] = []

for _, module_name, _ in pkgutil.iter_modules(core.__path__, prefix="core."):
    module = importlib.import_module(module_name)
    for _, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, Plugin) and obj is not Plugin:
            try:
                registered_plugins.append(obj())
            except Exception as e:
                print(f"Failed to instantiate {obj.__name__}: {e}")

def get_applicable_plugins(agent: str, input_text: str, context: Dict[str, Any]) -> List[Plugin]:
    return [plugin for plugin in registered_plugins if plugin.applies(input_text, context)]

def execute_plugin_chain(plugins: List[Plugin], input_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
    trace = {
        "executed_at": time.time(),
        "input": input_text,
        "results": []
    }
    for plugin in plugins:
        entry = {
            "plugin": plugin.name,
            "description": plugin.description,
            "input": input_text,
            "success": True,
            "output": "",
            "error": None
        }
        try:
            result = plugin.execute(input_text, context)
            entry["output"] = result
        except Exception as e:
            entry["success"] = False
            entry["error"] = str(e)
        trace["results"].append(entry)
    return trace
