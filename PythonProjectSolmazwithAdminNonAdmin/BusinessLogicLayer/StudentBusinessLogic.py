from Model.StudentModel import Student
from Model.StudentModel import StudentUpdate,StudentIdDelete
from DataAccessLayer.StudentDataAccess import StudentDataAccess


class StudentBusinessLogic:
    def __init__(self,student : Student = None, student_update: StudentUpdate = None,
                 student_delete:StudentIdDelete=None):
        self.Student = student
        self.student_update = student_update
        self.student_delete = student_delete

        self.AllDataStudent = []

    def checkNationalCodeExists(self, national_code):
        checkNationalCodeDALObject = StudentDataAccess()
        return checkNationalCodeDALObject.spCheckNationalCodeExists(national_code)

    def insertStudent(self, student):
        insertStudentDALObject = StudentDataAccess(student)
        insertStudentDALObject.spInsertStudent()


    def getStudentList(self, person_id):
        GetStudentListDALObject = StudentDataAccess()
        GetStudentListDALObject.spGetStudentList(person_id)
        self.AllDataStudent = GetStudentListDALObject.AllData

    def updateStudent(self):
        # Check if student_update is None
        if self.student_update is None:
            print("student_update is None")  # Debugging statement
            return False  # Or raise an exception
        # Validate required fields
        if not all([self.student_update.first_name,
                    self.student_update.last_name,
                    self.student_update.national_code]):
            return False

        studentDA = StudentDataAccess(student_update=self.student_update)  # Ensure student_update is passed
        return studentDA.spUpdateStudent()


    def deleteStudent(self,student_delete):
        deleteStudentDALObject = StudentDataAccess(student_delete)
        deleteStudentDALObject.spDeleteStudent(student_delete.person_id) # Pass the person_id

    def getAllStudents(self):
        getAllDALObject = StudentDataAccess()
        getAllDALObject.spGetAllStudents()
        self.AllDataStudent = getAllDALObject.AllData

    def getEducationList(self):
        educationDALObject = StudentDataAccess()
        educationDALObject.spGetEducationList()  # Implement this method in DataAccess
        return educationDALObject.AllData

    def getStudentListByNationalCode(self, national_code):
        student_data_access = StudentDataAccess()
        student_data_access.spGetStudentListByNationalCode(national_code)  # Implement this method in DataAccess
        self.AllDataStudent = student_data_access.AllData




