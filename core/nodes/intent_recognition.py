from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME", "deepseek-chat"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1"),
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)

def intent_recognition(state):
    user_input = state["messages"][-1]
    prompt = f"""
    你是零售电商客服意图分类器，只能从以下5种结果中选一个返回：
    订单查询、退换货申请、知识库问答、投诉建议、其他
    用户问题：{user_input}
    只返回分类结果，不要任何多余内容、标点符号
    """
    intent = llm.invoke(prompt).content.strip()
    return {"intent": intent}