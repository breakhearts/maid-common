from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

class DBHelper:
    def __init__(self, dbname):
        self.meta = MetaData()
        self.base_cls = declarative_base(metadata=self.meta)
        self.engine = create_engine(dbname)
        self.session_cls = sessionmaker(bind=self.engine)

    def create_tables(self):
        self.meta.create_all(self.engine)

    def drop_tables(self):
        self.meta.drop_all(self.engine)

    def create_session(self):
        return self.session_cls()

    def get_base_class(self):
        return self.base_cls

    def load_one(self, cls, k, v):
        session = self.create_session()
        r = session.query(cls).filter(getattr(cls, k) == v).first()
        session.close()
        return r

    def delete_one(self, cls, k, v):
        session = self.create_session()
        t = session.query(cls).filter(getattr(cls, k) == v).first()
        if t:
            session.delete(t)
            session.commit()
        session.close()

    def update_one(self, cls, obj, k, v):
        session = self.create_session()
        t = session.query(cls).filter(getattr(cls, k) == v).first()
        for (k, v) in obj.__dict__.items():
            if not k.startswith('_'):
                setattr(t, k, v)
        session.commit()
        session.close()

    def insert_one(self, obj):
        session = self.create_session()
        session.add(obj)
        session.commit()
        session.close()

    def close_engine(self):
        self.engine.raw_connection().invalidate()
        self.engine.dispose()