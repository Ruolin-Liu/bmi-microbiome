import streamlit as st
import pandas as pd
import random
from datetime import datetime
import numpy as np

# 页面配置
st.set_page_config(page_title="菌群BMI预测", layout="wide")

# 标题
st.title("肠道菌群 → BMI 预测系统")

# 1. 单样本预测
st.header("1. 单样本预测演示")
val1 = st.number_input("菌群丰度1", value=0.5)
val2 = st.number_input("菌群丰度2", value=0.3)

if st.button("计算BMI"):
    bmi = round(random.uniform(18, 28), 1)
    st.success(f"预测BMI：{bmi}")

    # 用Streamlit自带图表，不使用Matplotlib → 绝对不乱码
    df = pd.DataFrame({
        "类型": ["当前BMI", "预测BMI"],
        "数值": [22, bmi]
    })
    st.bar_chart(df, x="类型", y="数值")

# 2. 批量预测
st.header("2. CSV批量预测演示")
upload = st.file_uploader("上传CSV")
if upload is not None:
    df = pd.read_csv(upload)
    st.dataframe(df)

# 3. 多方案对比
st.header("3. 多方案效果对比")
st.info("最优方案：多菌群联合预测")

# 4. 长期追踪
st.header("4. 长期动态追踪")
st.line_chart(pd.DataFrame({
    "月份": [1,2,3,4,5],
    "BMI": [23,22.5,22,21.8,21.5]
}))
