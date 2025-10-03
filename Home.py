import streamlit as st

st.set_page_config(
    layout="wide",       # 页面全宽
    page_title="Translation Retrieval",  # 浏览器标签页标题
    page_icon="🔎",       # favicon 图标
)

st.title("📚 Translation Notes")
st.write("欢迎来到翻译语料工具！")
st.write("从左边侧边栏进入录入 / 批量导入 / 搜索。")
