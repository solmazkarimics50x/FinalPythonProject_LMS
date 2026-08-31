from Model.ScoreModel import Score
from DataAccessLayer.ConnectionString import *

from datetime import *
import struct
import pyodbc


class ScoreDataAccess:

    def __init__(self, score: Score = None):
        self.AllData = []
        self.ConnectionString = f'Driver={"{SQL SERVER}"};Server={Server};Database={DB_Name};UID={UserName};PWD={Password};'
        self.Score = score

    def spInsertScore(self):
        commandTextSP = '''EXEC [dbo].[sp_ScoreInsert]
                            @StudentID = ?,
                            @CoursesID = ?,
                            @TeacherID = ?,
                            @TermNumber = ?,
                            @Score = ?'''
        params = (self.Score.student_id,
                  self.Score.courses_id,
                  self.Score.teacher_id,
                  self.Score.term_number,
                  self.Score.score)
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            new_term_number = cursor.fetchone()[0]  # Get auto-generated TermNumber
            sqlConnection.commit()
            return new_term_number




    def spGetScoreList(self):
        commandTextSP = '''EXEC	[dbo].[GetScoreList] '''
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP)
            data = cursor.fetchall()
            self.AllData = [tuple(row) for row in data]  # Store the fetched data

    def spUpdateScore(self, term_number, student_id, courses_id, teacher_id):
        commandTextSP = '''EXEC [dbo].[UpdateScore]
                            
                            @StudentID = ?,
                            @CoursesID = ?,
                            @TeacherID = ?,
                            @TermNumber = ?,
                            @Score = ?'''

        params = (
                  student_id,
                  courses_id,
                  teacher_id,
                  term_number,
                  self.Score.score)

        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            sqlConnection.commit()
            return True

    def spDeleteScore(self, student_id, courses_id, teacher_id, term_number):
        commandTextSP = 'EXEC [dbo].[SP_DeleteScore] @StudentID = ?, @CoursesID = ?, @TeacherID = ?, @TermNumber = ?'
        params = (student_id, courses_id, teacher_id, term_number)
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            sqlConnection.commit()



    def spGetAllScores(self):
        commandTextSP = '''EXEC [dbo].[GetAllScores]'''  # Stored procedure to be created
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]



    def spGetStudentScoreList(self):
        commandTextSP = '''EXEC [dbo].[GetStudentScoreList]'''  # Create this stored procedure
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]

    def spGetCoursesList(self):
        commandTextSP = '''EXEC [dbo].[GetCoursesList]'''  # Create this stored procedure
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]

    def spGetTeacherScoreList(self):
        commandTextSP = '''EXEC [dbo].[GetTeacherScoreList]'''  # Create this stored procedure
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]






