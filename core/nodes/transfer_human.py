def transfer_human(state):
    return {
        "messages": state["messages"] + ["已为你转接专属人工客服，预计等待时间1-2分钟，请耐心等候~"]
    }
