from Model.EducationModel import *
from DataAccessLayer.ConnectionString import *
from datetime import *
import struct
import pyodbc


class EducationDataAccess:
    def __init__(self,education:Education=None):
        self.AllData = []
        self.ConnectionString = f'Driver={"{SQL SERVER}"};Server={Server};Database={DB_Name};UID={UserName};PWD={Password};'
        self.Education = education

    def spGetEducationList(self):
        commandTextSP = '''EXEC [dbo].[GetEducationList]'''  # Stored procedure to be created
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]



    def spInsertEducation(self):
        commandTextSP = 'EXEC [dbo].[sp_EducationInsert] @Education = ?'
        params = (self.Education.education,)
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            new_education_id = cursor.fetchone()[0]  # Fetch the new EducationID from the result
            sqlConnection.commit()
            return new_education_id  # Return the new EducationID


    def spUpdateEducation(self, education_id):
        commandTextSP = 'EXEC [dbo].[UpdateEducation] @EducationID=?, @Education = ?'
        params = ( education_id,self.Education.education)
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            sqlConnection.commit()


    def spDeleteEducation(self):
        commandTextSP = 'EXEC [dbo].[SP_DeleteEducation] @EducationID = ?'
        params = (self.Education)
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            sqlConnection.commit()

    def spGetAllEducations(self):
        commandTextSP = '''EXEC [dbo].[GetAllEducations]'''  # Stored procedure to be created
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]
