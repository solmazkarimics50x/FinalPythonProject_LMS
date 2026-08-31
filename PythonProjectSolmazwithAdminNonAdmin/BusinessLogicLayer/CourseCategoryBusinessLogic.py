from Model.CourseCategoryModel import CourseCategory
from DataAccessLayer.CourseCategoryDataAccess import CourseCategoryDataAccess


class CourseCategoryBusinessLogic:
    def __init__(self, coursecategory: CourseCategory = None):
        self.CourseCategory = coursecategory
        self.AllDataCourseCategory = []

    def getCourseCategoryList(self):
        GetCourseCategoryListDALObject = CourseCategoryDataAccess()
        GetCourseCategoryListDALObject.spGetCourseCategoryList()
        self.AllDataCourseCategory = GetCourseCategoryListDALObject.AllData

    def insertCourseCategory(self):
        insertCourseCategoryDALObject = CourseCategoryDataAccess(self.CourseCategory)
        return insertCourseCategoryDALObject.spInsertCourseCategory()  # Return the new CourseCategory ID


    def updateCourseCategory(self, course_category_id):
        updateCourseCategoryDALObject = CourseCategoryDataAccess(self.CourseCategory)
        updateCourseCategoryDALObject.spUpdateCourseCategory(course_category_id)

    def deleteCourseCategory(self, course_category_id):
        deleteCourseCategoryDALObject = CourseCategoryDataAccess(course_category_id)
        deleteCourseCategoryDALObject.spDeleteCourseCategory()

    def getAllCourseCategories(self):
        getAllDALObject = CourseCategoryDataAccess()
        getAllDALObject.spGetAllCourseCategories()
        self.AllDataCourseCategory = getAllDALObject.AllData