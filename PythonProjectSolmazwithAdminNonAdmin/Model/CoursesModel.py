class Courses:
    def __init__(self,courses_id=None ,course_name='', english_course_name='', duration=None,
                 syllabus_file = None,prerequisite_id = None,course_category_id= None):
        self.courses_id = courses_id
        self.course_name = course_name
        self.english_course_name = english_course_name
        self.duration = duration
        self.syllabus_file = syllabus_file
        self.prerequisite_id = prerequisite_id
        self.course_category_id = course_category_id





class CoursesIdDelete:
    def __init__(self, courses_id = None):
        self.courses_id = courses_id







