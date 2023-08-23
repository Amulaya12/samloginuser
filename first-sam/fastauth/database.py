from abc import abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:lobb123@localhost/fastauth"
import models

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
class BaseDBInit:
    def __init__(self, db_uri) -> None:
        self.db_uri = db_uri
        self.engine = None
        self.create_engine()
        models.Base.metadata.create_all(bind=self.engine)

    @abstractmethod
    def create_engine(self):
        pass

    def get_session(self):
        session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return session


class DBInitTest(BaseDBInit):
    def create_engine(self):
        self.engine = create_engine( self.db_uri, connect_args={"check_same_thread": False} )


class DBInit(BaseDBInit):
    def create_engine(self):
        self.engine = create_engine(self.db_uri)
