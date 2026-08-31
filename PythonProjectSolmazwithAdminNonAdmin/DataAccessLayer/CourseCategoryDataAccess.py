from Model.CourseCategoryModel import *
from DataAccessLayer.ConnectionString import *
from datetime import *
import struct
import pyodbc


class CourseCategoryDataAccess:
    def __init__(self,coursecategory:CourseCategory=None):
        self.AllData = []
        self.ConnectionString = f'Driver={"{SQL SERVER}"};Server={Server};Database={DB_Name};UID={UserName};PWD={Password};'
        self.CourseCategory = coursecategory

    def spGetCourseCategoryList(self):
        commandTextSP = '''EXEC [dbo].[GetCourseCategoryList]'''  # Stored procedure to be created
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]



    def spInsertCourseCategory(self):
        commandTextSP = 'EXEC [dbo].[sp_CourseCategoryInsert] @CourseCategoryName = ? ,@EnglishCourseCategoryName =?'
        params = (self.CourseCategory.course_category_name, self.CourseCategory.english_course_category_name,)
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            new_course_category_id = cursor.fetchone()[0]  # Fetch the new CourseCategoryID from the result
            sqlConnection.commit()
            return new_course_category_id  # Return the new CourseCategoryID


    def spUpdateCourseCategory(self, course_category_id):
        commandTextSP = 'EXEC [dbo].[UpdateCourseCategory] @CourseCategoryID=?, @CourseCategoryName = ?, @EnglishCourseCategoryName = ?'
        params = ( course_category_id,self.CourseCategory.course_category_name, self.CourseCategory.english_course_category_name)
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            sqlConnection.commit()


    def spDeleteCourseCategory(self):
        commandTextSP = 'EXEC [dbo].[SP_DeleteCourseCategory] @CourseCategoryID = ?'
        params = (self.CourseCategory)
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            sqlConnection.commit()

    def spGetAllCourseCategories(self):
        commandTextSP = '''EXEC [dbo].[GetAllCourseCategories]'''  # Stored procedure to be created
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]