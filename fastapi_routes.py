# interface/fastapi_routes.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from core.orchestrator import NeuroOrchestrator
from memory.vector_store import store_note, search_notes
import logging

app = FastAPI()
logger = logging.getLogger("neuronote")
logging.basicConfig(level=logging.INFO)

# --- Mock Memory class for now ---
class MemoryWrapper:
    def log_interaction(self, user_id, input_text, response):
        store_note(user_id, input_text + "\n\n" + response, {"source": "interaction"})

memory = MemoryWrapper()
orchestrator = NeuroOrchestrator(memory=memory, logger=logger)

class QueryInput(BaseModel):
    user_id: str
    input_text: str
    context: dict = {}

@app.post("/query")
async def query_llm(input: QueryInput):
    response = orchestrator.process_user_input(
        input.user_id,
        input.input_text,
        input.context
    )
    return {"response": response}

class SearchInput(BaseModel):
    query: str
    limit: int = 5

@app.post("/memory/search")
async def memory_search(input: SearchInput):
    results = search_notes(input.query, input.limit)
    return {"results": results}
