from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def setup_db(uri):
    engine = create_engine(uri, convert_unicode=True)  # uri example: 'sqlite:////tmp/test.db'
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()
    init_db(engine)
    return db_session


def init_db(engine):
    import models
    Base.metadata.create_all(bind=engine)
