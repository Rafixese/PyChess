from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey, or_
import bcrypt

Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)

    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash


engine = create_engine('sqlite:///database.db', echo=False, connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def create_client(username, email, password_hash):
    q = session.query(Client).filter(or_(Client.username == username, Client.email == email)).all()
    if len(q) > 0:
        raise Exception('Client username or email already in database')
    c = Client(username, email, password_hash)
    session.add(c)
    session.commit()

def auth_client(username, password_hash):
    c: Client = session.query(Client).filter(Client.username == username).first()
    if c is None:
        raise Exception('No such username in database')
    if c.password_hash != password_hash:
        raise Exception('Password incorrect')

    return c.username
