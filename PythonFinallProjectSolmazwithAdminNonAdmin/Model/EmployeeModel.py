class Employee:
    def __init__(self,person_id=None ,first_name='', last_name='',birthdate=None, national_code='',
                  gender=None, address='', mobile='', photo=None,
                 education_id=None, employee_id=None,marital_status = None,job_id = None,department_id = None,
                 hire_date=None,insurance_number= None,account_number = '',manager_id = None):
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
        self.employee_id = employee_id
        self.marital_status = marital_status
        self.job_id = job_id
        self.department_id = department_id
        self.hire_date = hire_date
        self.insurance_number = insurance_number
        self.account_number = account_number
        self.manager_id = manager_id


class EmployeeUpdate:
    def __init__(self, person_id=None, first_name='', last_name='', birthdate=None,
                national_code='', gender=None, address='', mobile='', photo=None,
                education_id=None, employee_id=None,marital_status = None,job_id = None,department_id = None,
                 hire_date=None,insurance_number= None,account_number = '',manager_id = None):
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
        self.employee_id = employee_id
        self.marital_status = marital_status
        self.job_id = job_id
        self.department_id = department_id
        self.hire_date = hire_date
        self.insurance_number = insurance_number
        self.account_number = account_number
        self.manager_id = manager_id

class EmployeeIdDelete:
    def __init__(self, person_id = None):
        self.person_id = person_id







