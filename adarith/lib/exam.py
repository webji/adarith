
class Exam(object):
    def __init__(self):
        self.incompleted_questions = {}
        self.completed_questions = {}
        self.question = None
        self.number = 0
        super().__init__()

    @property
    def total_count(self):
        ret = len(self.incompleted_questions) + len(self.completed_questions)
        if self.question != None:
            ret += 1
        return ret

    @property
    def complete_count(self):
        return len(self.completed_questions)

    @property
    def incomplete_count(self):
        ret = len(self.incompleted_questions)
        ret += 0 if self.question == None else 1
        return ret
    
    def result_count(self, result = True):
        c = 0
        for k in self.completed_questions.keys():
            q = self.completed_questions[k]
            if q.result == result:
                c += 1
        return c
    
    def load(self):
        self.number = 0
