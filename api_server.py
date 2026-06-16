from fastapi import FastAPI
from pydantic import BaseModel
from core.workflow import agent_app
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="零售智能客服Agent")

class ChatRequest(BaseModel):
    query: str
    order_id: str = ""

@app.post("/chat")
async def chat(request: ChatRequest):
    result = agent_app.invoke({
        "messages": [request.query],
        "intent": "",
        "order_id": request.order_id,
        "return_step": 0,
        "need_order_id": False
    })
    return {
        "reply": result["messages"][-1],
        "intent": result["intent"]
    }
