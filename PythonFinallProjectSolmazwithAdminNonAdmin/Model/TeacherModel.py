class Teacher:
    def __init__(self,person_id=None ,first_name='', last_name='',birthdate=None, national_code='',
                  gender=None, address='', mobile='', photo=None,
                 education_id=None, teacher_code=None,marital_status = None,start_date=None,
                 insurance_number= None,account_number = '', certificate_id = None,expiration_date =None,
                 res_id = ''):
        self.person_id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.national_code = national_code
        self.gender = gender  # Should be 1/0 or 'Married'/'Single'
        self.address = address
        self.mobile = mobile
        self.photo = photo
        self.education_id = education_id
        self.teacher_code = teacher_code
        self.marital_status = marital_status
        self.start_date = start_date
        self.insurance_number = insurance_number
        self.account_number = account_number
        self.certificate_id = certificate_id
        self.expiration_date = expiration_date
        self.res_id = res_id


class TeacherUpdate:
    def __init__(self, person_id=None, first_name='', last_name='', birthdate=None,
                national_code='', gender=None, address='', mobile='', photo=None,
                education_id=None, teacher_code=None,marital_status = None,start_date=None,
                 insurance_number= None,account_number = '', certificate_id = None,expiration_date =None,
                 res_id = ''):
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
        self.teacher_code = teacher_code
        self.marital_status = marital_status
        self.start_date = start_date
        self.insurance_number = insurance_number
        self.account_number = account_number
        self.certificate_id = certificate_id
        self.expiration_date = expiration_date
        self.res_id = res_id

class TeacherIdDelete:
    def __init__(self, person_id = None):
        self.person_id = person_id







