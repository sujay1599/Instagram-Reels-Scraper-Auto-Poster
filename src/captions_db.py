from sqlalchemy import Column, Integer, String, DateTime
from db import Base, engine, Session
from datetime import datetime


class Caption(Base):
    __tablename__ = 'captions'

    id         = Column(Integer, primary_key=True)
    reel_code  = Column(String, index=True)
    original   = Column(String)   # raw scraped caption_text
    processed  = Column(String)   # ready-to-post caption (@mentions replaced, hashtags kept/appended)
    created_at = Column(DateTime)


Base.metadata.create_all(engine, checkfirst=True)


def save_caption(reel_code, original, processed):
    session = Session()
    try:
        session.add(Caption(
            reel_code=reel_code,
            original=original,
            processed=processed,
            created_at=datetime.now(),
        ))
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_processed_caption(reel_code):
    session = Session()
    try:
        cap = session.query(Caption).filter_by(reel_code=reel_code).first()
        return cap.processed if cap else None
    finally:
        session.close()
