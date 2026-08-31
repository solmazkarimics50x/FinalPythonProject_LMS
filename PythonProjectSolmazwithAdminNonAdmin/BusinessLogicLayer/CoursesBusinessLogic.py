from Model.CoursesModel import Courses
from Model.CoursesModel import CoursesIdDelete
from DataAccessLayer.CoursesDataAccess import CoursesDataAccess


class CoursesBusinessLogic:
    def __init__(self,courses : Courses = None,courses_delete:CoursesIdDelete=None):
        self.Courses = courses
        self.courses_delete = courses_delete

        self.AllDataCourses = []


    def insertCourses(self):
        insertCoursesDALObject = CoursesDataAccess(self.Courses)
        return insertCoursesDALObject.spInsertCourses()  # Return the new course ID


    def getCoursesList(self):
        GetCoursesListDALObject = CoursesDataAccess()
        GetCoursesListDALObject.spGetCoursesList()
        self.AllDataCourses = GetCoursesListDALObject.AllData

    def updateCourses(self, courses_id):
        updateCoursesDALObject = CoursesDataAccess(self.Courses)
        updateCoursesDALObject.spUpdateCourses(courses_id)


    def deleteCourses(self, course_id):
        deleteCoursesDALObject = CoursesDataAccess(course_id)
        deleteCoursesDALObject.spDeleteCourses()

    def getAllCoursess(self):
        getAllDALObject = CoursesDataAccess()
        getAllDALObject.spGetAllCoursess()
        self.AllDataCourses = getAllDALObject.AllData



    def getCourseCategoryList(self):
        coursecategoryDALObject = CoursesDataAccess()
        coursecategoryDALObject.spGetCourseCategoryList()  # Implement this method in DataAccess
        return coursecategoryDALObject.AllData







