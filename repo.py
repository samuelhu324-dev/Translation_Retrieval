from sqlalchemy import select, or_, func
from models import SessionLocal, Entry, Source, EntrySource
from typing import List, Optional, Tuple

def add_entry(src:str, tgt:str, ls="zh", lt="en",
              source_name:Optional[str]=None, source_url:Optional[str]=None)->int:
    src = src.strip(); tgt = tgt.strip()
    if not src or not tgt: raise ValueError("src/tgt required")
    with SessionLocal() as s:
        e = Entry(src_text=src, tgt_text=tgt, lang_src=ls, lang_tgt=lt)
        s.add(e); s.flush()
        if source_name:
            src_obj = s.execute(select(Source).where(Source.name==source_name)).scalar_one_or_none()
            if not src_obj:
                src_obj = Source(name=source_name, url=source_url); s.add(src_obj); s.flush()
            s.add(EntrySource(entry_id=e.id, source_id=src_obj.id))
        s.commit()
        return e.id

def search(q:str, ls=None, lt=None, source_names:Optional[List[str]]=None,
           limit=50, offset=0)->List[Tuple[int,str,str]]:
    with SessionLocal() as s:
        stmt = select(Entry.id, Entry.src_text, Entry.tgt_text)
        if q:
            like = f"%{q.strip()}%"
            stmt = stmt.where(or_(Entry.src_text.like(like), Entry.tgt_text.like(like)))
        if ls: stmt = stmt.where(Entry.lang_src==ls)
        if lt: stmt = stmt.where(Entry.lang_tgt==lt)
        stmt = stmt.order_by(Entry.created_at.desc()).limit(limit).offset(offset)
        return s.execute(stmt).all()
