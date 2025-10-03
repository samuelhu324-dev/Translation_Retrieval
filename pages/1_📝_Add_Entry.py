import streamlit as st
from repo import add_entry
from models import init_db

init_db()
st.title("📝 快速录入 / Quick Add")

with st.form("add"):
    src = st.text_area("原文 / Source", height=140)
    tgt = st.text_area("译文 / Target", height=140)
    c1,c2,c3 = st.columns(3)
    with c1: ls = st.selectbox("源语言", ["en", "zh"], index=0)  # 默认 en
    with c2: lt = st.selectbox("目标语言", ["zh", "en"], index=0) # 默认 zh
    with c3:
        source_name = st.text_input("来源名称")
    source_url = st.text_input("来源链接（可选）")
    submitted = st.form_submit_button("保存 / Save")
    if submitted:
        try:
            eid = add_entry(src, tgt, ls, lt, source_name or None, source_url or None)
            st.success(f"Saved entry #{eid}")
        except Exception as e:
            st.error(str(e))
