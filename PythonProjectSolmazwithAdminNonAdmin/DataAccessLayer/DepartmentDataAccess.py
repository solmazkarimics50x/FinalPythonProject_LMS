from Model.DepartmentModel import *
from DataAccessLayer.ConnectionString import *
from datetime import *
import struct
import pyodbc


class DepartmentDataAccess:
    def __init__(self,department:Department=None):
        self.AllData = []
        self.ConnectionString = f'Driver={"{SQL SERVER}"};Server={Server};Database={DB_Name};UID={UserName};PWD={Password};'
        self.Department = department

    def spGetDepartmentList(self):
        commandTextSP = '''EXEC [dbo].[GetDepartmentList]'''  # Stored procedure to be created
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]



    def spInsertDepartment(self):
        commandTextSP = 'EXEC [dbo].[sp_DepartmentInsert] @DepartmentName = ?'
        params = (self.Department.department_name,)
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            new_department_id = cursor.fetchone()[0]  # Fetch the new DepartmentID from the result
            sqlConnection.commit()
            return new_department_id  # Return the new DepartmentID


    def spUpdateDepartment(self, department_id):
        commandTextSP = 'EXEC [dbo].[UpdateDepartment] @DepartmentID=?, @DepartmentName = ?'
        params = ( department_id,self.Department.department_name)
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            sqlConnection.commit()


    def spDeleteDepartment(self):
        commandTextSP = 'EXEC [dbo].[SP_DeleteDepartment] @DepartmentID = ?'
        params = (self.Department)
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            sqlConnection.commit()

    def spGetAllDepartments(self):
        commandTextSP = '''EXEC [dbo].[GetAllDepartments]'''  # Stored procedure to be created
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]