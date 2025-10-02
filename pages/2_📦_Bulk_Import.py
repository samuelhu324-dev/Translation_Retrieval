import streamlit as st
import pandas as pd
from repo import add_entry
from models import init_db

init_db()
st.title("📦 批量导入 / Bulk Import")

uploaded = st.file_uploader("上传 CSV/Excel 文件 / Upload CSV or Excel file", 
                            type=["csv", "xlsx"])

if uploaded is not None:
    # 自动识别文件类型
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)

    st.write("检测到的列 / Detected columns:", list(df.columns))

    # 映射列
    src_col = st.selectbox("源文本列 / Source text column", df.columns)
    tgt_col = st.selectbox("译文列 / Target text column", df.columns)
    ls_col  = st.selectbox("源语言列 (可选) / Source lang col (optional)", ["(None)"] + list(df.columns))
    lt_col  = st.selectbox("目标语言列 (可选) / Target lang col (optional)", ["(None)"] + list(df.columns))
    srcname_col = st.selectbox("来源列 (可选) / Source name col (optional)", ["(None)"] + list(df.columns))

    if st.button("开始导入 / Start Import"):
        success, fail = 0, 0
        for i, row in df.iterrows():
            try:
                src = str(row[src_col])
                tgt = str(row[tgt_col])
                ls = None if ls_col == "(None)" else str(row[ls_col])
                lt = None if lt_col == "(None)" else str(row[lt_col])
                srcname = None if srcname_col == "(None)" else str(row[srcname_col])

                add_entry(src, tgt, ls or "zh", lt or "en", srcname)
                success += 1
            except Exception as e:
                fail += 1
                st.error(f"第 {i} 行出错 / Row {i} error: {e}")
        st.success(f"导入完成！成功 {success} 条，失败 {fail} 条 / Done! {success} ok, {fail} failed")
