# interface/fastapi_routes.py
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from core.orchestrator import NeuroOrchestrator
from memory.vector_store import store_note, search_notes
from core.orchestration_log import persist_trace, load_trace
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
    trace = orchestrator.process_user_input(
        input.user_id,
        input.input_text,
        input.context
    )
    trace_id = persist_trace(trace)
    return {"trace_id": trace_id, "results": trace["results"]}

class SearchInput(BaseModel):
    query: str
    limit: int = 5

@app.post("/memory/search")
async def memory_search(input: SearchInput):
    results = search_notes(input.query, input.limit)
    return {"results": results}

@app.get("/audit/{trace_id}")
async def get_audit_trace(trace_id: str):
    try:
        trace = load_trace(trace_id)
        return {"trace_id": trace_id, "trace": trace}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Trace not found")
