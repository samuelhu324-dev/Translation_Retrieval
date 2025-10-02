import streamlit as st
from repo import search

st.title("🔎 搜索 / Search")
q = st.text_input("关键词 / Keyword")
ls = st.selectbox("源语言", ["","zh","en"], index=1)
lt = st.selectbox("目标语言", ["","en","zh"], index=1)
limit = st.number_input("每页数量", 10, 200, 50)

if st.button("搜索 / Go"):
    rows = search(q, ls or None, lt or None, limit=limit)
    for _id, src, tgt in rows:
        with st.expander(f"#{_id}"):
            st.markdown(f"**SRC**: {src}")
            st.markdown(f"**TGT**: {tgt}")
            st.code(tgt, language="text")
