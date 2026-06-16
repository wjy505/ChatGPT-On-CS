def load_order_db():
    mock_data = {
        "20240601001": "订单状态：已发货，承运方：顺丰速运，当前位置：成都转运中心，预计明日送达",
        "20240601002": "订单状态：待发货，仓库已拣货，预计今日发出",
        "20240601003": "订单状态：已签收，签收时间：2024-06-05 14:30"
    }
    return mock_data

def query_order(state):
    order_id = state.get("order_id", "")
    order_db = load_order_db()

    if not order_id:
        return {
            "messages": state["messages"] + ["请提供你的订单编号，我将为你实时查询物流状态~"],
            "need_order_id": True
        }

    order_info = order_db.get(order_id, "未查询到该订单信息，请核对订单号是否正确")
    return {
        "messages": state["messages"] + [f"查询结果：{order_info}"],
        "need_order_id": False
    }
