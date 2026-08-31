from Model.EmployeeModel import Employee
from Model.EmployeeModel import EmployeeUpdate
from DataAccessLayer.ConnectionString import *

from datetime import *
import struct
import pyodbc


class EmployeeDataAccess:

    def __init__(self, employee: Employee = None, employee_update: EmployeeUpdate = None):
        self.AllData = []
        self.ConnectionString = f'Driver={"{SQL SERVER}"};Server={Server};Database={DB_Name};UID={UserName};PWD={Password};'
        self.Employee = employee
        self.employee_update = employee_update


    def spInsertEmployee(self):
        commandTextSP ='''EXEC [dbo].[Sp_InsertEmployee] 
                                @FirstName = ?,
                                @LastName = ?,
                                @Birthdate = ?,
                                @NationalCode = ?,
                                @Gender = ?,
                                @Address = ?,
                                @Mobile = ?,
                                @Photo = ?,
                                @EducationID = ?,
                                @EmployeeID = ?,
                                @MaritalStatus = ?,
                                @JobID = ?,
                                @DepartmentID = ?,
                                @Hiredata = ?,
                                @InsuranceNumber = ?,
                                @AccountNumber = ?,
                                @ManagerID = ?;
                                SELECT SCOPE_IDENTITY();'''  # Get the last inserted ID

        params = (self.Employee.first_name,self.Employee.last_name,self.Employee.birthdate,self.Employee.national_code,
                  self.Employee.gender,self.Employee.address,self.Employee.mobile,self.Employee.photo,# Pass the binary photo data
                  self.Employee.education_id,
                  self.Employee.employee_id,self.Employee.marital_status,self.Employee.job_id,self.Employee.department_id,
                  self.Employee.hire_date,self.Employee.insurance_number,self.Employee.account_number,self.Employee.manager_id)

        # print("Inserting Employee with parameters:", params)  # Debugging line
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            self.Employee.person_id = cursor.fetchone()[0]  # Set the person_id from the last inserted ID
            sqlConnection.commit()




    def spGetEmployeeList(self, person_id):
        commandTextSP = '''EXEC	[dbo].[GetEmployeeList] @PersonID = ?'''
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP,(person_id,))
            data = cursor.fetchall()
            self.AllData = [tuple(row) for row in data]  # Store the fetched data


    def spCheckNationalCodeExists(self, national_code):
        commandTextSP = '''EXEC [dbo].[sp_CheckNationalCodeExists] @NationalCode = ?'''
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, (national_code,))
            result = cursor.fetchone()
            return bool(result[0]) if result else False


    def spUpdateEmployee(self):
        if self.employee_update is None:
            #print("employee_update is None in spUpdateEmployee")  # Debugging statement
            return False  # Or raise an exception
        commandTextSP = '''EXEC [dbo].[UpdateEmployee]
                            @PersonID = ?,
                            @FirstName = ?,
                            @LastName = ?,
                            @Birthdate = ?,
                            @NationalCode = ?,
                            @Gender = ?,
                            @Address = ?,
                            @Mobile = ?,
                            @Photo = ?,
                            @EducationID = ?,
                            @EmployeeID = ?,
                            @MaritalStatus = ?,
                            @JobID = ?,
                            @DepartmentID = ?,
                            @Hiredata = ?,
                            @InsuranceNumber = ?,
                            @AccountNumber = ?,
                            @ManagerID = ?'''

        params = (
            self.employee_update.person_id,
            self.employee_update.first_name,
            self.employee_update.last_name,
            self.employee_update.birthdate,
            self.employee_update.national_code,
            self.employee_update.gender,
            self.employee_update.address,
            self.employee_update.mobile,
            self.employee_update.photo,
            self.employee_update.education_id,
            self.employee_update.employee_id,
            self.employee_update.marital_status,
            self.employee_update.job_id,
            self.employee_update.department_id,
            self.employee_update.hire_date,
            self.employee_update.insurance_number,
            self.employee_update.account_number,
            self.employee_update.manager_id
        )
        with pyodbc.connect(self.ConnectionString) as connection:
            cursor = connection.cursor()
            cursor.execute(commandTextSP, params)
            connection.commit()
            return cursor.rowcount > 0

    def spDeleteEmployee(self, person_id):
        commandTextSP = 'EXEC [dbo].[SP_DeleteEmployee] @PersonID = ?'

        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, (person_id,))
            sqlConnection.commit()

    def spGetAllEmployees(self):
        commandTextSP = '''EXEC [dbo].[GetAllEmployees]'''  # Stored procedure to be created
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]


    def spGetEducationList(self):
        commandTextSP = '''EXEC [dbo].[GetEducationList]'''  # Create this stored procedure
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]

    def spGetDepartmentList(self):
        commandTextSP = '''EXEC [dbo].[GetDepartmentList]'''  # Create this stored procedure
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]

    def spGetJobList(self):
        commandTextSP = '''EXEC [dbo].[GetJobList]'''  # Create this stored procedure
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]

    def spGetEmployeeListByNationalCode(self, national_code):
        commandTextSP = '''EXEC [dbo].[GetEmployeeByNationalCode] @NationalCode = ?'''
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, (national_code,))
            data = cursor.fetchall()
            self.AllData = [tuple(row) for row in data]  # Store the fetched data



