# collaborative_prompt_library/prompt_planner.py
from typing import List, Dict, Optional
from datetime import datetime

class PromptPlanner:
    def __init__(self, plugins: List[Dict], agents: List[Dict], memory: List[Dict]):
        self.plugins = plugins
        self.agents = agents
        self.memory = memory
        self.audit_log = []

    def match_plugins_by_capability(self, capability: str) -> List[Dict]:
        matches = [p for p in self.plugins if capability in (p.get('capabilities') or [])]
        self.audit_log.append({
            "action": "match_plugins",
            "capability": capability,
            "timestamp": datetime.utcnow().isoformat(),
            "matched_plugins": [p['plugin'] for p in matches],
        })
        return matches

    def get_prompt_template_for_role(self, role: str) -> str:
        role_templates = {
            "SYNTHESIZER": (
                "You are a neutral synthesizer. Your task is to distil the following conversation into a concise, unbiased summary. "
                "Preserve nuance and represent all perspectives faithfully."
            ),
            "VALIDATOR": (
                "You are a fact-checking agent. Review the following outputs for factual accuracy, logical soundness, and consistency with source material. "
                "Highlight any discrepancies."
            ),
            "STRUCTURER": (
                "You are a structurer. Convert this unstructured dialogue into a structured format—e.g., JSON summary, tag list, or argument graph—preserving key information."
            ),
            "INTERROGATOR": (
                "You are a questioner. Identify unclear, contradictory, or weak claims in this conversation and pose insightful questions to challenge or clarify them."
            ),
            "REFLECTOR": (
                "You are a reflective analyst. Detect themes, tonal shifts, or implicit assumptions in this conversation. Your role is to reveal what is beneath the surface."
            )
        }
        return role_templates.get(role, "You are an agent performing an undefined role. Use your best judgment.")

    def assign_roles_to_plugins(self, task: str) -> List[Dict]:
        plan = []

        if "summarise" in task.lower():
            matches = self.match_plugins_by_capability("summarisation")
            if matches:
                role = "SYNTHESIZER"
                plan.append({
                    "role": role,
                    "plugin": matches[0]['plugin'],
                    "prompt": self.get_prompt_template_for_role(role),
                    "llm_route": "openai/gpt-4o",
                    "dependencies": [m['id'] for m in self.memory],
                })

        if "validate" in task.lower() or "fact-check" in task.lower():
            matches = self.match_plugins_by_capability("fact-checking")
            if matches:
                role = "VALIDATOR"
                plan.append({
                    "role": role,
                    "plugin": matches[0]['plugin'],
                    "prompt": self.get_prompt_template_for_role(role),
                    "llm_route": "claude/opus",
                    "dependencies": [m['id'] for m in self.memory],
                })

        return plan

    def build_prompt_plan(self, task: str) -> Dict:
        plan = self.assign_roles_to_plugins(task)
        return {
            "plan": plan,
            "audit_trail": self.audit_log,
        }
