from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from db_creds import getURI

engine = create_engine(getURI(), convert_unicode=True)
metadata = MetaData()

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
def init_db():
    metadata.create_all(bind=engine)
