from contextlib import contextmanager
from typing import Optional, Generator, ContextManager

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, TEXT, ForeignKey, create_engine, Engine
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship, sessionmaker, Session

Base = declarative_base()
metadata = Base.metadata

engine: Engine = create_engine('sqlite:///data/database.db', echo=False)
session_maker = sessionmaker(bind=engine)


@contextmanager
def session_scope() -> Session:
    """Provide a transactional scope around a series of operations."""
    session = session_maker()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class CurrentPage(Base):
    __tablename__ = 'current_page'

    community_name = Column(VARCHAR(30), primary_key=True)
    page = Column(INTEGER)


class PostPhashHistory(Base):
    __tablename__ = 'post_phash_history'

    post_id = Column(INTEGER, primary_key=True, autoincrement=True)
    community_name = Column(VARCHAR(30))
    url = Column(TEXT)
    phash_id: Mapped[Optional[int]] = mapped_column(ForeignKey("phash_history.id"))
    phash: Mapped[Optional["PhashHistory"]] = relationship()


class PhashHistory(Base):
    __tablename__ = 'phash_history'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    community_name = Column(VARCHAR(30))
    phash = Column(VARCHAR(50))


Base.metadata.create_all(engine)