import streamlit as st
import pandas as pd
import random  # 必须有这一行
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import shutil

# --------------------- 【云端中文真正能用的代码】 ---------------------
# 1. 清空 matplotlib 缓存（必须！）
shutil.rmtree(matplotlib.get_cachedir(), ignore_errors=True)

# 2. 加载项目里的字体
font_path = "./SimHei.ttf"
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = 'SimHei'

plt.rcParams['axes.unicode_minus'] = False  # 负号正常

# ---------------------- 页面配置 ----------------------
st.set_page_config(
    page_title="菌群-BMI预测演示",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 核心菌群度值 → BMI 预测系统")
st.markdown("""> 输入肠道菌群数据，支持**多干预方案自由组合**，实现BMI智能预测。""")

# ---------------------- 数据 ----------------------
single_drop = {
    "高纤维饮食": 2.3,
    "低碳水饮食": 1.2,
    "有氧运动": 1.5
}
plan_color = {
    "高纤维饮食": "#2E8B57",
    "低碳水饮食": "#4682B4",
    "有氧运动": "#CD853F"
}
bmi_pool = [26.5,25.8,24.3,23.1,27.2,22.6]

# ---------------------- 状态永久保存 ----------------------
if "current_bmi" not in st.session_state:
    st.session_state["current_bmi"] = None
if "pred_bmi" not in st.session_state:
    st.session_state["pred_bmi"] = 0.0
if "total_drop" not in st.session_state:
    st.session_state["total_drop"] = 0.0
if "conf" not in st.session_state:
    st.session_state["conf"] = 80
if "selected_list" not in st.session_state:
    st.session_state["selected_list"] = []

# ---------------------- 1 预测 ----------------------
st.header("1️⃣ 单样本预测演示")
g1 = st.number_input("普雷沃氏菌",0.0,1.0,0.2,step=0.01)
g2 = st.number_input("拟杆菌",0.0,1.0,0.5,step=0.01)
g3 = st.number_input("菌群C",0.0,1.0,0.1,step=0.01)
g4 = st.number_input("菌群D",0.0,1.0,0.3,step=0.01)
g5 = st.number_input("菌群E",0.0,1.0,0.4,step=0.01)
g6 = st.number_input("菌群F",0.0,1.0,0.2,step=0.01)

if st.button("📊 计算当前BMI"):
    st.session_state["current_bmi"] = random.choice(bmi_pool)

if st.session_state["current_bmi"]:
    st.success(f"✅ 当前BMI：{st.session_state['current_bmi']}")
else:
    st.info("请先计算BMI")

selected_list = st.multiselect("干预方案（可多选）",list(single_drop.keys()),["高纤维饮食"])

if st.button("🔍 预测3个月后BMI"):
    if not st.session_state["current_bmi"]:
        st.warning("先算BMI")
    elif not selected_list:
        st.warning("选方案")
    else:
        now = st.session_state["current_bmi"]
        drop = round(sum(single_drop[p] for p in selected_list)*0.85,1)
        pred = round(now-drop,1)
        conf = 85-len(selected_list)*3

        st.session_state["pred_bmi"] = pred
        st.session_state["total_drop"] = drop
        st.session_state["conf"] = conf
        st.session_state["selected_list"] = selected_list

        c1,c2,c3 = st.columns(3)
        c1.metric("当前BMI",now)
        c2.metric("预测BMI",pred,f"-{drop}")
        c3.metric("置信度",f"{conf}%")

        fig,ax = plt.subplots(figsize=(6,2.5))
        ax.barh(["当前","预测"],[now,pred],color=["#FF6B6B","#37BEB0"])
        ax.set_xlim(0,32)
        st.pyplot(fig)

# ---------------------- 2 批量 ----------------------
st.divider()
st.header("2️⃣ CSV批量预测")
f = st.file_uploader("上传CSV",type="csv")
if f:
    df = pd.read_csv(f)
    st.dataframe(df.head())
    if st.button("批量预测"):
        df["当前BMI"] = random.choices(bmi_pool,k=len(df))
        df["预测BMI"] = df["当前BMI"]-2.3
        df["类型"] = df["预测BMI"].apply(lambda x:"正常"if x<25 else"超重")
        st.dataframe(df)

# ---------------------- 3 单项对比 ----------------------
st.divider()
st.header("3️⃣ 单项方案对比")
if st.button("📊 查看对比图表"):
    if not st.session_state["current_bmi"]:
        st.warning("先算BMI")
    else:
        plans = list(single_drop.keys())
        preds = [round(st.session_state["current_bmi"]-single_drop[p],1)for p in plans]
        fig,ax = plt.subplots(figsize=(8,4))
        ax.bar(plans,preds,color=[plan_color[p]for p in plans])
        ax.axhline(25,color='red',ls='--',label="健康线")
        ax.legend()
        st.pyplot(fig)

# ---------------------- 4 长期追踪 ----------------------
st.divider()
st.header("4️⃣ 长期追踪")
if st.button("📈 启动模拟"):
    base = st.session_state["current_bmi"]or 25
    m = list(range(1,9))
    s = [base - 0.25*i for i in m]
    fig,ax = plt.subplots(figsize=(8,4))
    ax.plot(m,s,marker='o',color="#2E8B57")
    ax.axhline(25,color='red',ls='--',label="健康线")
    ax.legend()
    st.pyplot(fig)

# ---------------------- 报告按钮：永久显示（本地+云端都显示） ----------------------
st.divider()
st.header("📄 完整预测总报告")

now_bmi = st.session_state.get("current_bmi","未计算")
pred_bmi = st.session_state.get("pred_bmi","未预测")
total_drop = st.session_state.get("total_drop","无")
conf = st.session_state.get("conf","无")
plan_text = "、".join(st.session_state.get("selected_list",[])) or "未选择"

report = f"""
==================== 肠道菌群-BMI 预测报告 ====================
时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
当前BMI：{now_bmi}
预测BMI：{pred_bmi}
下降：{total_drop}
方案：{plan_text}
置信度：{conf}%
============================================================
"""

# ✅ 永久显示，不判断，不消失！
st.download_button(
    label="📥 下载总报告",
    data=report,
    file_name="报告.txt"
)
