from Model.StudentModel import Student
from Model.StudentModel import StudentUpdate
from DataAccessLayer.ConnectionString import *

from datetime import *
import struct
import pyodbc


class StudentDataAccess:

    def __init__(self, student: Student = None, student_update: StudentUpdate = None):
        self.AllData = []
        self.ConnectionString = f'Driver={"{SQL SERVER}"};Server={Server};Database={DB_Name};UID={UserName};PWD={Password};'
        self.Student = student
        self.student_update = student_update


    def spInsertStudent(self):
        commandTextSP ='''EXEC [dbo].[sp_InsertStudent] 
                                @FirstName = ?,
                                @LastName = ?,
                                @Birthdate = ?,
                                @NationalCode = ?,
                                @Gender = ?,
                                @Address = ?,
                                @Mobile = ?,
                                @Photo = ?,
                                @EducationID = ?,
                                @StudentCode = ?,
                                @Job = ?;
                                SELECT SCOPE_IDENTITY();'''  # Get the last inserted ID

        params = (self.Student.first_name,self.Student.last_name,self.Student.birthdate,self.Student.national_code,
                  self.Student.gender,self.Student.address,self.Student.mobile,self.Student.photo,# Pass the binary photo data
                  self.Student.education_id,
                  self.Student.student_code,self.Student.job)

        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            self.Student.person_id = cursor.fetchone()[0]  # Set the person_id from the last inserted ID
            sqlConnection.commit()




    def spGetStudentList(self, person_id):
        commandTextSP = '''EXEC	[dbo].[GetStudentList] @PersonID = ?'''
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


    def spUpdateStudent(self):
        if self.student_update is None:
            #print("student_update is None in spUpdateStudent")  # Debugging statement
            return False  # Or raise an exception
        commandTextSP = '''EXEC [dbo].[UpdateStudent]
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
                            @StudentCode = ?,
                            @Job = ?'''

        params = (
            self.student_update.person_id,
            self.student_update.first_name,
            self.student_update.last_name,
            self.student_update.birthdate,
            self.student_update.national_code,
            self.student_update.gender,
            self.student_update.address,
            self.student_update.mobile,
            self.student_update.photo,
            self.student_update.education_id,
            self.student_update.student_code,
            self.student_update.job
        )
        with pyodbc.connect(self.ConnectionString) as connection:
            cursor = connection.cursor()
            cursor.execute(commandTextSP, params)
            connection.commit()
            return cursor.rowcount > 0

    def spDeleteStudent(self, person_id):
        commandTextSP = 'EXEC [dbo].[SP_DeleteStudent] @PersonID = ?'

        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, (person_id,))
            sqlConnection.commit()

    def spGetAllStudents(self):
        commandTextSP = '''EXEC [dbo].[GetAllStudents]'''  # Stored procedure to be created
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

    def spGetStudentListByNationalCode(self, national_code):
        commandTextSP = '''EXEC [dbo].[GetStudentByNationalCode] @NationalCode = ?'''
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, (national_code,))
            data = cursor.fetchall()
            self.AllData = [tuple(row) for row in data]  # Store the fetched data



