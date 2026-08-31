from Model.EmployeeModel import Employee
from Model.EmployeeModel import EmployeeUpdate,EmployeeIdDelete
from DataAccessLayer.EmployeeDataAccess import EmployeeDataAccess


class EmployeeBusinessLogic:
    def __init__(self,employee : Employee = None, employee_update: EmployeeUpdate = None,
                 employee_delete:EmployeeIdDelete=None):
        self.Employee = employee
        self.employee_update = employee_update
        self.employee_delete = employee_delete

        self.AllDataEmployee = []

    def checkNationalCodeExists(self, national_code):
        checkNationalCodeDALObject = EmployeeDataAccess()
        return checkNationalCodeDALObject.spCheckNationalCodeExists(national_code)

    def insertEmployee(self, employee):
        insertEmployeeDALObject = EmployeeDataAccess(employee)
        insertEmployeeDALObject.spInsertEmployee()


    def getEmployeeList(self, person_id):
        GetEmployeeListDALObject = EmployeeDataAccess()
        GetEmployeeListDALObject.spGetEmployeeList(person_id)
        self.AllDataEmployee = GetEmployeeListDALObject.AllData

    def updateEmployee(self):
        if self.employee_update.manager_id is None:
            # Handle cases where employee has no manager (e.g., skip manager checks)
            pass
        # # Check if employee_update is None
        # if self.employee_update is None:
        #     #print("employee_update is None")  # Debugging statement
        #     return False  # Or raise an exception
        # Validate required fields
        if not all([self.employee_update.first_name,
                    self.employee_update.last_name,
                    self.employee_update.national_code]):
            return False

        employeeDA = EmployeeDataAccess(employee_update=self.employee_update)  # Ensure employee_update is passed
        return employeeDA.spUpdateEmployee()


    def deleteEmployee(self,employee_delete):
        deleteEmployeeDALObject = EmployeeDataAccess(employee_delete)
        deleteEmployeeDALObject.spDeleteEmployee(employee_delete.person_id) # Pass the person_id

    def getAllEmployees(self):
        getAllDALObject = EmployeeDataAccess()
        getAllDALObject.spGetAllEmployees()
        self.AllDataEmployee = getAllDALObject.AllData



    def getEducationList(self):
        educationDALObject = EmployeeDataAccess()
        educationDALObject.spGetEducationList()  # Implement this method in DataAccess
        return educationDALObject.AllData

    def getDepartmentList(self):
        departmentDALObject = EmployeeDataAccess()
        departmentDALObject.spGetDepartmentList()  # Implement this method in DataAccess
        return departmentDALObject.AllData

    def getJobList(self):
        jobDALObject = EmployeeDataAccess()
        jobDALObject.spGetJobList()  # Implement this method in DataAccess
        return jobDALObject.AllData

    def getEmployeeListByNationalCode(self, national_code):
        employee_data_access = EmployeeDataAccess()
        employee_data_access.spGetEmployeeListByNationalCode(national_code)  # Implement this method in DataAccess
        self.AllDataEmployee = employee_data_access.AllData




