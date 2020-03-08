from sqlalchemy import Column, Integer, String, Date, MetaData

from . import Base

from .setting import SettingModel

class QuestionModel(Base):
    __tablename__ = 't_questions'

    id = Column(Integer, primary_key=True)
    title = Column(String(20), unique=True)
    stem = Column(String(100))
    answer = Column(String(20))
    difficulty = Column(Integer)

    def __repr__(self):
        return f"<QuestionModel (title={self.title}, stem={self.stem}, answer={self.answer}>"


    @staticmethod
    def init_question(session = None):
        initialized = session.query(SettingModel).filter_by(key='initialized').first()
        if initialized.value == 'True':
            return
        question_dict = {}
        for left in range(10):
            for right in range(10):
                difficulty = min(left, right)

                add_title = f'{left} + {right} = ?'
                add_answer = left + right
                add_question = QuestionModel(title=add_title, answer=add_answer, difficulty=difficulty)
                question_dict[add_title] = add_question

                if left >= right:
                    sub_title = f'{left} - {right} = ?'
                    sub_answer = left - right
                    sub_question = QuestionModel(title=sub_title, answer=sub_answer, difficulty=difficulty)
                    question_dict[sub_title] = sub_question
        initialized.value = 'False'
        initialized.enabled = True
        session.add_all(question_dict.values())
        session.commit()
