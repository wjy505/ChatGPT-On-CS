import streamlit as st
import requests

st.set_page_config(page_title="零售智能客服Agent", page_icon="🤖")
st.title("🤖 零售智能客服Agent演示")

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 渲染历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 用户输入
if prompt := st.chat_input("请输入你的问题，比如：查订单、问退货政策"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 调用后端接口
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                resp = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={"query": prompt}
                )
                reply = resp.json()["reply"]
                intent = resp.json()["intent"]
                st.markdown(reply)
                st.caption(f"识别意图：{intent}")
            except Exception as e:
                st.error(f"接口调用失败：{str(e)}")
                reply = "服务异常，请检查后端是否启动"

    st.session_state.messages.append({"role": "assistant", "content": reply})