import sqlite3
import pandas as pd
import streamlit as st

DB = "tm.db"

@st.cache_resource
def get_db():
    con = sqlite3.connect(DB, check_same_thread=False)
    return con

def search(q, type_codes=None, doc=None, topk=50):
    con = get_db()
    sql = """
    SELECT s.id, s.src_text, s.tgt_text, s.type_code,
           d.filename AS document, so.title AS source, s.quality
    FROM segments_fts f
    JOIN segments s ON s.id=f.rowid
    LEFT JOIN documents d ON d.id=s.doc_id
    LEFT JOIN sources so ON so.id=s.source_id
    WHERE segments_fts MATCH ?
    """
    params = [q]
    if type_codes:
        conds = " OR ".join([f"instr(s.type_code, ?)>0" for _ in type_codes])
        sql += f" AND ({conds})"
        params += type_codes
    if doc:
        sql += " AND d.filename = ?"
        params.append(doc)
    sql += " ORDER BY s.quality DESC LIMIT ?"
    params.append(topk)
    return pd.read_sql_query(sql, con, params=params)

st.title("🔍 翻译语料查询系统")
q = st.text_input("关键词 / 短语", "协议")
type_filter = st.multiselect(
    "关键表述类型",
    ["DEF","OBL","RIGHT","COND","EXCP","TIME"]
)
doc_filter = st.text_input("文档名过滤", "")
topk = st.slider("返回条数", 10, 200, 50)

if st.button("检索"):
    df = search(q, type_filter or None, doc_filter or None, topk)
    # 简单高亮
    def mark(text):
        if not q: return text
        return text.replace(q, f"**{q}**")
    if not df.empty:
        df["src_text"] = df["src_text"].apply(mark)
        df["tgt_text"] = df["tgt_text"].apply(mark)
    st.dataframe(df, use_container_width=True)

st.caption("Powered by SQLite + Streamlit. 数据请用 init_tm_db.py 初始化或导入。")
