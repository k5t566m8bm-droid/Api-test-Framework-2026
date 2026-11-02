from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

class DBClient:
    def __init__(self, db_path):
        # 使用 SQLAlchemy 创建引擎，并开启连接池 (pool_size=5, max_overflow=10)
        # 如果换成 MySQL，只需要把连接串改成: mysql+pymysql://user:pass@localhost/db
        self.engine = create_engine(
            f"sqlite:///{db_path}",
            pool_size=5,
            max_overflow=10,
            connect_args={"check_same_thread": False} # SQLite特有
        )
        self.Session = sessionmaker(bind=self.engine)
        self._init_db()

    def _init_db(self):
        with self.engine.connect() as conn:
            conn.execute(text('''CREATE TABLE IF NOT EXISTS users 
                                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, job TEXT)'''))
            conn.commit()

    def insert(self, sql, params=()):
        with self.Session() as session:
            result = session.execute(text(sql), params)
            session.commit()
            return result.lastrowid

    def delete(self, sql, params=()):
        with self.Session() as session:
            result = session.execute(text(sql), params)
            session.commit()
            return result.rowcount

    def query_one(self, sql, params=()):
        with self.Session() as session:
            result = session.execute(text(sql), params).fetchone()
            return result

    def close(self):
        self.engine.dispose()