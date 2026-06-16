from typing import TypedDict
from langgraph.graph import StateGraph, END

from .nodes.intent_recognition import intent_recognition
from .nodes.order_query import query_order
from .nodes.return_process import return_process
from .nodes.knowledge_query import knowledge_query
from .nodes.transfer_human import transfer_human

class AgentState(TypedDict):
    messages: list
    intent: str
    order_id: str
    return_step: int
    need_order_id: bool

def intent_router(state):
    intent = state["intent"]
    if intent == "订单查询":
        return "order_query"
    elif intent == "退换货申请":
        return "return_process"
    elif intent == "知识库问答":
        return "knowledge_query"
    else:
        return "transfer_human"

def build_workflow():
    workflow = StateGraph(AgentState)

    workflow.add_node("intent_recognition", intent_recognition)
    workflow.add_node("order_query", query_order)
    workflow.add_node("return_process", return_process)
    workflow.add_node("knowledge_query", knowledge_query)
    workflow.add_node("transfer_human", transfer_human)

    workflow.set_entry_point("intent_recognition")

    workflow.add_conditional_edges(
        "intent_recognition",
        intent_router,
        {
            "order_query": "order_query",
            "return_process": "return_process",
            "knowledge_query": "knowledge_query",
            "transfer_human": "transfer_human"
        }
    )

    workflow.add_edge("order_query", END)
    workflow.add_edge("return_process", END)
    workflow.add_edge("knowledge_query", END)
    workflow.add_edge("transfer_human", END)

    return workflow.compile()

agent_app = build_workflow()