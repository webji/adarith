from sqlalchemy import Column, Integer, String, Date, MetaData

from . import Base

class UserModel(Base):
    __tablename__ = 't_users'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    fullname = Column(String(32))
    password = Column(String(32))
    born_date = Column(String(20))

    def __repr__(self):
        return f"<User (name={self.name}, fullname={self.fullname}, password={self.password}, born_date={self.born_date}>"


    @staticmethod
    def init_user(session = None):
        ada_user = session.query(UserModel).filter_by(name='Ada').first()
        if ada_user == None:
            ada_user = UserModel(name='Ada', fullname='Ada The Explorer', password='ada123', born_date='12345678')
            session.add(ada_user)
            session.commit()
