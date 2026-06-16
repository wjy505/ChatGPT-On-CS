def return_process(state):
    return_step = state.get("return_step", 0)

    if return_step == 0:
        return {
            "messages": state["messages"] + ["请先提供你的订单号，并简单说明退货原因，我将为你生成退货审核单~"],
            "return_step": 1
        }
    elif return_step == 1:
        return {
            "messages": state["messages"] + ["已为你生成退货申请，退货地址：成都市武侯区天府软件园A区1栋，审核通过后会以短信通知你快递指引。"],
            "return_step": 2
        }
