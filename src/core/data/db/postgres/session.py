from contextlib import contextmanager
from typing import Generator
from sqlalchemy.orm import Session, sessionmaker
from src.core.data.db.postgres.engine import engine


local_session: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    session: Session = local_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()