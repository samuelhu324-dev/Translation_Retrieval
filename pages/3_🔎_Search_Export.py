import streamlit as st

st.set_page_config(
    layout="wide",       # 页面全宽
    page_title="Translation Retrieval",  # 浏览器标签页标题
    page_icon="🔎",       # favicon 图标
)

from repo import search

st.title("🔎 搜索 / Search")
q = st.text_input("关键词 / Keyword")
ls = st.selectbox("源语言", ["","zh","en"], index=2)
lt = st.selectbox("目标语言", ["","en","zh"], index=2)
limit = st.number_input("每页数量", 10, 200, 50)

if st.button("搜索 / Go"):
    rows = search(q, ls or None, lt or None, limit=limit)
    for _id, src, tgt in rows:
        with st.expander(f"#{_id}"):

            st.markdown("**SRC:**")
            st.markdown(
                f"<div style='white-space: pre-wrap; word-wrap: break-word;'>{src}</div>",
                unsafe_allow_html=True,
            )

            # 提供下载按钮（相当于“复制”替代方案）
            st.download_button(
                label="📋 下载原文 / Download SRC",
                data=src,
                file_name=f"src_{_id}.txt",
                mime="text/plain",
                key=f"src_dl_{_id}"
            )

            st.markdown("**TGT:**")
            st.markdown(
                f"<div style='white-space: pre-wrap; word-wrap: break-word;'>{tgt}</div>",
                unsafe_allow_html=True,
            )

            st.download_button(
                label="📋 下载译文 / Download TGT",
                data=tgt,
                file_name=f"tgt_{_id}.txt",
                mime="text/plain",
                key=f"tgt_dl_{_id}"
            )
