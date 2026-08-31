from Model.TeacherModel import Teacher
from Model.TeacherModel import TeacherUpdate,TeacherIdDelete
from DataAccessLayer.TeacherDataAccess import TeacherDataAccess


class TeacherBusinessLogic:
    def __init__(self,teacher : Teacher = None, teacher_update: TeacherUpdate = None,
                 teacher_delete:TeacherIdDelete=None):
        self.Teacher = teacher
        self.teacher_update = teacher_update
        self.teacher_delete = teacher_delete

        self.AllDataTeacher = []

    def checkNationalCodeExists(self, national_code):
        checkNationalCodeDALObject = TeacherDataAccess()
        return checkNationalCodeDALObject.spCheckNationalCodeExists(national_code)

    def insertTeacher(self, teacher):
        insertTeacherDALObject = TeacherDataAccess(teacher)
        insertTeacherDALObject.spInsertTeacher()


    def getNewTeacherList(self,person_id):
        GetNewTeacherListDALObject = TeacherDataAccess()
        GetNewTeacherListDALObject.spGetNewTeacherList(person_id)
        self.AllDataTeacher = GetNewTeacherListDALObject.AllData

    def updateTeacher(self):
        # Check if teacher_update is None
        if self.teacher_update is None:
            print("teacher_update is None")  # Debugging statement
            return False  # Or raise an exception
        # Validate required fields
        if not all([self.teacher_update.first_name,
                    self.teacher_update.last_name,
                    self.teacher_update.national_code]):
            return False

        teacherDA = TeacherDataAccess(teacher_update=self.teacher_update)  # Ensure teacher_update is passed
        return teacherDA.spUpdateTeacher()


    def deleteTeacher(self,teacher_delete):
        deleteTeacherDALObject = TeacherDataAccess(teacher_delete)
        deleteTeacherDALObject.spDeleteTeacher(teacher_delete.person_id) # Pass the person_id

    def getNewAllTeachers(self):
        getAllDALObject = TeacherDataAccess()
        getAllDALObject.spGetNewAllTeachers()
        self.AllDataTeacher = getAllDALObject.AllData

    def getEducationList(self):
        educationDALObject = TeacherDataAccess()
        educationDALObject.spGetEducationList()  # Implement this method in DataAccess
        return educationDALObject.AllData

    def getNewTeacherListByNationalCode(self, national_code):
        teacher_data_access = TeacherDataAccess()
        teacher_data_access.spGetNewTeacherListByNationalCode(national_code)  # Implement this method in DataAccess
        self.AllDataTeacher = teacher_data_access.AllData




    def getCertificateList(self):
        certificateDALObject = TeacherDataAccess()
        certificateDALObject.spGetCertificateList()  # Implement this method in DataAccess
        return certificateDALObject.AllData






