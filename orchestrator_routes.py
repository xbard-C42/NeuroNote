# api/api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.orchestrator_routes import router as orchestrator_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register orchestrator routes
app.include_router(orchestrator_router)

# --- Mock data endpoint for frontend development ---
@app.get("/mock/orchestrator/plan")
async def mock_plan():
    return {
        "plan": [
            {
                "role": "SYNTHESIZER",
                "plugin": "multi_llm_summariser",
                "prompt": "You are a neutral synthesizer...",
                "llm_route": "openai/gpt-4o",
                "dependencies": ["memory_001", "memory_002"]
            },
            {
                "role": "VALIDATOR",
                "plugin": "claim_validator",
                "prompt": "You are a fact-checking agent...",
                "llm_route": "claude/opus",
                "dependencies": ["memory_001"]
            }
        ],
        "audit_trail": [
            {"action": "match_plugins", "capability": "summarisation", "timestamp": "2025-06-30T12:00:00Z", "matched_plugins": ["multi_llm_summariser"]},
            {"action": "match_plugins", "capability": "fact-checking", "timestamp": "2025-06-30T12:00:01Z", "matched_plugins": ["claim_validator"]}
        ]
    }
