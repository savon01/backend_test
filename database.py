from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE = 'database.db'
engine = create_engine(f'sqlite:///{DATABASE}', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True)
    cadastre_number = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    result = Column(Boolean, nullable=False)


Base.metadata.create_all(bind=engine)


def create_request(cadastre_number, latitude, longitude):
    session = Session()
    request = Request(cadastre_number=cadastre_number, latitude=latitude, longitude=longitude)
    session.add(request)
    session.commit()
    request_id = request.id
    session.close()
    return request_id


def update_result(request_id, result):
    session = Session()
    request = session.query(Request).get(request_id)
    if request:
        request.result = result
        session.commit()
    session.close()


def get_history(cadastre_number=None):
    session = Session()
    query = session.query(Request)
    if cadastre_number:
        query = query.filter(Request.cadastre_number == cadastre_number)
    history = query.all()
    session.close()
    return history
