class Score:
    def __init__(self,student_id = None,courses_id =None,teacher_id =None,term_number = None,score = None):
        self.student_id = student_id
        self.courses_id = courses_id
        self.teacher_id = teacher_id
        self.term_number = term_number
        self.score = score


class ScoreIdDelete:
    def __init__(self, student_id=None, courses_id=None, teacher_id=None, term_number=None):
        self.student_id = student_id
        self.courses_id = courses_id
        self.teacher_id = teacher_id
        self.term_number = term_number

