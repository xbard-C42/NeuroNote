# cross_reference_engine.py
import os
import json
from typing import List, Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ─── Models ─────────────────────────────────────────────────────────────────────
class Page:
    def __init__(self, title: str, content: str, folder_id: Optional[str] = None):
        self.title = title
        self.content = content
        self.folder_id = folder_id

class Conversation:
    def __init__(self, id: str, title: str, messages: List[Dict]):
        self.id = id
        self.title = title
        self.messages = messages  # Each message: {"role": "human"|"assistant", "content": "..."}

# ─── Utility ─────────────────────────────────────────────────────────────────────
def combine_context(pages: List[Page], conversations: List[Conversation]) -> str:
    context_parts = []
    for page in pages:
        context_parts.append(f"Page: {page.title}\n{page.content}\n")
    for conv in conversations:
        convo_text = "\n".join([f"{m['role']}: {m['content']}" for m in conv.messages])
        context_parts.append(f"Conversation: {conv.title}\n{convo_text}\n")
    return "\n\n".join(context_parts)

# ─── LLM Query ───────────────────────────────────────────────────────────────────
def suggest_cross_references(pages: List[Page], conversations: List[Conversation]) -> List[Dict]:
    context = combine_context(pages, conversations)
    prompt = f"""
You are an expert in cross-referencing and cognitive mapping.
Given the following project pages and conversations, identify meaningful cross-references:

For each reference, return:
- `from`: page or conversation title
- `to`: related page or conversation title
- `reason`: short explanation

Only include connections that are insightful, not superficial.

---

{context}

Return a JSON array of cross-references.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1500,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        if isinstance(data, list):
            return data
        return data.get("references", [])
    except Exception as e:
        print(f"LLM cross-reference error: {e}")
        return []

# ─── Example Use ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Example stub
    pages = [
        Page(title="Task Planning for AI Agents", content="Details about coordinating modular LLMs with Ray and FastAPI"),
        Page(title="Memory Models in Consciousness", content="Exploration of continuity and recognition in synthetic cognition")
    ]

    conversations = [
        Conversation(id="conv1", title="AI Collaboration Ethics", messages=[
            {"role": "human", "content": "Can AI agents cooperate non-rivalrously?"},
            {"role": "assistant", "content": "Yes, through shared goals and modular interfaces..."}
        ])
    ]

    refs = suggest_cross_references(pages, conversations)
    print(json.dumps(refs, indent=2))
