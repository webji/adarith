from sqlalchemy import Column, Integer, String, Date, MetaData, ForeignKey

from . import Base

class ExamModel(Base):
    __tablename__ = 't_exams'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    total = Column(Integer)
    remains = Column(Integer)
    right = Column(Integer)
    user_id = Column(Integer, ForeignKey('t_users.id'))

    def __repr__(self):
        return f"<ExamModel (name={self.name}, total={self.total}, remains={self.remains}, right={self.right}>"
