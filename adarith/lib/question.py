from enum import Enum

class QuestionStatus(Enum):
    INITED = 0
    STARTED = 1
    ANSWERED = 2
    SUBMITED = 3
    GRADED = 4
    COMPLETED = 5


class Question(object):    
    def __init__(self, id='question_id', number=0, title='Question Title'):
        self.id = id
        self.number = number
        self.title = title
        self.stem = None
        self.status = QuestionStatus.INITED
        self.answer = None
        self.result = False
        super().__init__()

    def __repr__(self):
        return f'{self.title}'
        
    def start(self):
        self.status = QuestionStatus.STARTED

    def answering(self, answer):
        self.answer = answer
        self.status = QuestionStatus.ANSWERED
        
    def submit(self):
        self.status = QuestionStatus.SUBMITED
        self.grade()
        self.status = QuestionStatus.GRADED

    def grade(self):
        pass

    def complete(self):
        self.status = QuestionStatus.COMPLETED


    
class ArithQuestion(Question):
    def __init__(self, id, number, arithmetic):
        self.arithmetic = arithmetic
        self.answer = None
        super().__init__(id=id, number=number, title=f'{arithmetic}')

    def grade(self):
        super().grade()
        self.result = self.answer == self.arithmetic.answer
        return self.result

