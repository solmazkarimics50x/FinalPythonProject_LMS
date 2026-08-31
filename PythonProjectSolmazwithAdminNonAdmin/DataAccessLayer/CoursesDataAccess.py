from Model.CoursesModel import Courses
from DataAccessLayer.ConnectionString import *

from datetime import *
import struct
import pyodbc


class CoursesDataAccess:

    def __init__(self, courses: Courses = None):
        self.AllData = []
        self.ConnectionString = f'Driver={"{SQL SERVER}"};Server={Server};Database={DB_Name};UID={UserName};PWD={Password};'
        self.Courses = courses



    def spInsertCourses(self):
        commandTextSP ='''EXEC [dbo].[sp_CoursesInsert] 
                                @CourseName = ?,
                                @EnglishCourseName = ?,
                                @Duration = ?,
                                @SyllabusFile = ?,
                                @PrerequisiteID = ?,
                                @CourseCategoryID = ?'''

        params = (self.Courses.course_name,self.Courses.english_course_name,self.Courses.duration,
                  self.Courses.syllabus_file,self.Courses.prerequisite_id ,self.Courses.course_category_id,)

        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            new_courses_id = cursor.fetchone()[0]  # Fetch the new CourseID from the result
            sqlConnection.commit()
            return new_courses_id  # Return the new CourseID




    def spGetCoursesList(self):
        commandTextSP = '''EXEC	[dbo].[GetCoursesList] '''
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP)
            data = cursor.fetchall()
            self.AllData = [tuple(row) for row in data]  # Store the fetched data

    def spUpdateCourses(self, courses_id):
        commandTextSP = ('''EXEC [dbo].[UpdateCourses]
                         @CoursesID=?,
                         @CourseName=?,
                         @EnglishCourseName=?,
                         @Duration=?,
                         @SyllabusFile=?,
                         @PrerequisiteID=?,
                         @CourseCategoryID=?''')

        params = (courses_id,  # First parameter should be courses_id
                  self.Courses.course_name,
                  self.Courses.english_course_name,
                  self.Courses.duration,
                  self.Courses.syllabus_file,
                  self.Courses.prerequisite_id,
                  self.Courses.course_category_id)

        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            sqlConnection.commit()



    def spDeleteCourses(self):
        commandTextSP = 'EXEC [dbo].[SP_DeleteCourses] @CoursesID = ?'
        params = (self.Courses)
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            sqlConnection.commit()

    def spGetAllCoursess(self):
        commandTextSP = '''EXEC [dbo].[GetAllCoursess]'''  # Stored procedure to be created
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]



    def spGetCourseCategoryList(self):
        commandTextSP = '''EXEC [dbo].[GetCourseCategoryList]'''  # Create this stored procedure
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]






