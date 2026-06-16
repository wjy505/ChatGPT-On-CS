import pandas as pd
import requests
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# ========== 配置项 ==========
AGENT_CHAT_URL = "http://127.0.0.1:8000/chat"

# 打分用大模型，和业务模型一致
score_llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME", "deepseek-chat"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1"),
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)

def get_agent_answer(question):
    """调用本地Agent接口获取回复"""
    try:
        resp = requests.post(AGENT_CHAT_URL, json={"query": question}, timeout=10)
        resp.raise_for_status()
        return resp.json()["reply"]
    except Exception as e:
        print(f"调用失败：{question}，错误：{str(e)}")
        return ""

def calc_faithfulness(ground_truth, answer, contexts):
    """事实一致性打分（对应Ragas的faithfulness），0-1分"""
    prompt = f"""
    请判断AI回答是否完全符合参考上下文和标准答案，没有编造信息。
    满分1分，只返回数字，不要任何解释。
    参考上下文：{contexts}
    标准答案：{ground_truth}
    AI回答：{answer}
    """
    try:
        res = score_llm.invoke(prompt).content.strip()
        return float(res)
    except:
        return 0.0

def calc_context_recall(ground_truth, answer):
    """上下文召回率打分，0-1分"""
    # 基于关键词重合度计算
    gt_words = set(ground_truth.replace("，", "").replace("。", "").replace("：", "").split())
    ans_words = set(answer.replace("，", "").replace("。", "").replace("：", "").split())
    if not gt_words:
        return 0.0
    return len(gt_words & ans_words) / len(gt_words)

def calc_context_precision(ground_truth, answer):
    """上下文准确率打分，0-1分"""
    gt_words = set(ground_truth.replace("，", "").replace("。", "").replace("：", "").split())
    ans_words = set(answer.replace("，", "").replace("。", "").replace("：", "").split())
    if not ans_words:
        return 0.0
    return len(gt_words & ans_words) / len(ans_words)

def run_full_evaluation():
    print("===== 开始执行Agent效果评测 =====")

    # 1. 加载测试数据集
    df = pd.read_csv("./evaluate/test_dataset.csv")
    print(f"加载测试用例：{len(df)}条")

    # 2. 批量调用Agent生成回答
    print("正在批量生成回答...")
    df["answer"] = df["question"].apply(get_agent_answer)

    # 3. 计算三项核心指标（完全对应JD要求的准确率、召回率）
    print("正在计算评测指标...")
    df["事实一致性"] = df.apply(lambda row: calc_faithfulness(row["ground_truth"], row["answer"], row["contexts"]), axis=1)
    df["上下文准确率"] = df.apply(lambda row: calc_context_precision(row["ground_truth"], row["answer"]), axis=1)
    df["上下文召回率"] = df.apply(lambda row: calc_context_recall(row["ground_truth"], row["answer"]), axis=1)
    df["综合得分"] = round((df["事实一致性"] + df["上下文准确率"] + df["上下文召回率"]) / 3, 3)

    # 4. 控制台输出总览
    print("\n===== 评测总览结果 =====")
    print(f"平均事实一致性：{round(df['事实一致性'].mean(), 3)}")
    print(f"平均上下文准确率：{round(df['上下文准确率'].mean(), 3)}")
    print(f"平均上下文召回率：{round(df['上下文召回率'].mean(), 3)}")
    print(f"平均综合得分：{round(df['综合得分'].mean(), 3)}")

    # 5. 导出详细评测报告
    report_path = "./evaluate/results/full_eval_report.xlsx"
    df.to_excel(report_path, index=False)
    print(f"\n详细报告已导出：{report_path}")

    # 6. 自动筛选Badcase（综合得分<0.7标记为Badcase）
    badcases = df[df["综合得分"] < 0.7]
    badcase_path = "./evaluate/results/badcases.xlsx"
    badcases.to_excel(badcase_path, index=False)
    print(f"自动筛选Badcase共{len(badcases)}条，已导出：{badcase_path}")

    print("\n===== 评测执行完成 =====")

if __name__ == "__main__":
    run_full_evaluation()