from Model.TeacherModel import Teacher
from Model.TeacherModel import TeacherUpdate
from DataAccessLayer.ConnectionString import *

from datetime import *
import struct
import pyodbc


class TeacherDataAccess:

    def __init__(self, teacher: Teacher = None, teacher_update: TeacherUpdate = None):
        self.AllData = []
        self.ConnectionString = f'Driver={"{SQL SERVER}"};Server={Server};Database={DB_Name};UID={UserName};PWD={Password};'
        self.Teacher = teacher
        self.teacher_update = teacher_update


    def spInsertTeacher(self):
        commandTextSP ='''EXEC [dbo].[InsertTeacher] 
                                @FirstName = ?,
                                @LastName = ?,
                                @Birthdate = ?,
                                @NationalCode = ?,
                                @Gender = ?,
                                @Address = ?,
                                @Mobile = ?,
                                @Photo = ?,
                                @EducationID = ?,
                                @TeacherCode = ?,
                                @MaritalStatus = ?,
		                        @Startdate = ?,
		                        @InsuranceNumber = ?,
		                        @AccountNumber = ?,
		                        @CertificateID =?, 
		                        @Expirationdate = ?,
		                        @ResID = ? ;
                                SELECT SCOPE_IDENTITY();'''  # Get the last inserted ID

        params = (self.Teacher.first_name,self.Teacher.last_name,self.Teacher.birthdate,self.Teacher.national_code,
                  self.Teacher.gender,self.Teacher.address,self.Teacher.mobile,self.Teacher.photo,# Pass the binary photo data
                  self.Teacher.education_id,
                  self.Teacher.teacher_code,self.Teacher.marital_status,self.Teacher.start_date,
                  self.Teacher.insurance_number,self.Teacher.account_number,
                  self.Teacher.certificate_id,self.Teacher.expiration_date,self.Teacher.res_id)

        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            self.Teacher.person_id = cursor.fetchone()[0]  # Set the person_id from the last inserted ID
            sqlConnection.commit()




    def spGetNewTeacherList(self,person_id):
        commandTextSP = '''EXEC	[dbo].[GetNewTeacherList] @PersonID = ?'''
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


    def spUpdateTeacher(self):
        if self.teacher_update is None:
            #print("teacher_update is None in spUpdateTeacher")  # Debugging statement
            return False  # Or raise an exception
        commandTextSP = '''EXEC [dbo].[UpdateTeacher]
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
                            @TeacherCode = ?,
                            @MaritalStatus = ?,
		                    @Startdate = ?,
		                    @InsuranceNumber = ?,
		                    @AccountNumber = ?'''

        params = (
            self.teacher_update.person_id,
            self.teacher_update.first_name,
            self.teacher_update.last_name,
            self.teacher_update.birthdate,
            self.teacher_update.national_code,
            self.teacher_update.gender,
            self.teacher_update.address,
            self.teacher_update.mobile,
            self.teacher_update.photo,
            self.teacher_update.education_id,
            self.teacher_update.teacher_code,
            self.teacher_update.marital_status,
            self.teacher_update.start_date,
            self.teacher_update.insurance_number,
            self.teacher_update.account_number
        )
        with pyodbc.connect(self.ConnectionString) as connection:
            cursor = connection.cursor()
            cursor.execute(commandTextSP, params)
            connection.commit()
            return cursor.rowcount > 0

    def spDeleteTeacher(self, person_id):
        commandTextSP = 'EXEC [dbo].[DeleteTeacher] @PersonID = ?'

        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, (person_id,))
            sqlConnection.commit()

    def spGetNewAllTeachers(self):
        commandTextSP = '''EXEC [dbo].[GetNewAllTeachers]'''  # Stored procedure to be created
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

    def spGetNewTeacherListByNationalCode(self, national_code):
        commandTextSP = '''EXEC [dbo].[GetNewTeacherByNationalCode] @NationalCode = ?'''
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, (national_code,))
            data = cursor.fetchall()
            self.AllData = [tuple(row) for row in data]  # Store the fetched data



    # def spGetTeacherTeacherList(self):
    #     commandTextSP = '''EXEC [dbo].[GetTeacherTeacherList]'''  # Create this stored procedure
    #     with pyodbc.connect(self.ConnectionString) as conn:
    #         cursor = conn.cursor()
    #         cursor.execute(commandTextSP)
    #         self.AllData = [tuple(row) for row in cursor.fetchall()]

    def spGetCertificateList(self):
        commandTextSP = '''EXEC [dbo].[GetCertificateList]'''  # Create this stored procedure
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]



