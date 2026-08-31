from Model.DepartmentModel import Department
from DataAccessLayer.DepartmentDataAccess import DepartmentDataAccess

class DepartmentBusinessLogic:
    def __init__(self, department: Department = None):
        self.Department = department
        self.AllDataDepartment = []

    def getDepartmentList(self):
        GetDepartmentListDALObject = DepartmentDataAccess()
        GetDepartmentListDALObject.spGetDepartmentList()
        self.AllDataDepartment = GetDepartmentListDALObject.AllData

    def insertDepartment(self):
        insertDepartmentDALObject = DepartmentDataAccess(self.Department)
        return insertDepartmentDALObject.spInsertDepartment()  # Return the new department ID



    def updateDepartment(self, department_id):
        updateDepartmentDALObject = DepartmentDataAccess(self.Department)
        updateDepartmentDALObject.spUpdateDepartment(department_id)

    def deleteDepartment(self, department_id):
        deleteDepartmentDALObject = DepartmentDataAccess(department_id)
        deleteDepartmentDALObject.spDeleteDepartment()

    def getAllDepartments(self):
        getAllDALObject = DepartmentDataAccess()
        getAllDALObject.spGetAllDepartments()
        self.AllDataDepartment = getAllDALObject.AllData