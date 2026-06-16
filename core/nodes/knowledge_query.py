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

def knowledge_query(state):
    user_input = state["messages"][-1]

    knowledge_base = """
    售后政策说明：
    1. 7天无理由退换：商品签收后7天内，不影响二次销售可申请无理由退换货
    2. 质量问题保障：商品存在质量问题，30天内可免费退换货，往返运费由商家承担
    3. 发票申请：确认收货后，可在订单详情页申请电子发票，开具周期为3个工作日
    4. 地址修改：未发货订单可自行修改收货地址；已发货订单需联系人工客服协调
    """

    prompt = f"""
    严格基于以下知识库回答用户问题，禁止编造知识库以外的内容。
    知识库内容：
    {knowledge_base}
    用户问题：{user_input}
    """
    answer = llm.invoke(prompt).content.strip()
    return {"messages": state["messages"] + [answer]}
