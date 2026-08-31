class Student:
    def __init__(self,person_id=None ,first_name='', last_name='',birthdate=None, national_code='',
                  gender=None, address='', mobile='', photo=None,
                 education_id=None, student_code=None,job=''):
        self.person_id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.national_code = national_code
        self.gender = gender  # Should be 1/0 or 'Male'/'Female'
        self.address = address
        self.mobile = mobile
        self.photo = photo
        self.education_id = education_id
        self.student_code = student_code
        self.job = job

class StudentUpdate:
    def __init__(self, person_id=None, first_name='', last_name='', birthdate=None,
                national_code='', gender=None, address='', mobile='', photo=None,
                education_id=None, student_code=None, job=''):
        self.person_id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.national_code = national_code
        self.gender = gender
        self.address = address
        self.mobile = mobile
        self.photo = photo
        self.education_id = education_id
        self.student_code = student_code
        self.job = job

class StudentIdDelete:
    def __init__(self, person_id = None):
        self.person_id = person_id







