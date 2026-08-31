from Model.EducationModel import Education
from DataAccessLayer.EducationDataAccess import EducationDataAccess

class EducationBusinessLogic:
    def __init__(self, education: Education = None):
        self.Education = education
        self.AllDataEducation = []

    def getEducationList(self):
        GetEducationListDALObject = EducationDataAccess()
        GetEducationListDALObject.spGetEducationList()
        self.AllDataEducation = GetEducationListDALObject.AllData

    def insertEducation(self):
        insertEducationDALObject = EducationDataAccess(self.Education)
        return insertEducationDALObject.spInsertEducation()  # Return the new education ID



    def updateEducation(self, education_id):
        updateEducationDALObject = EducationDataAccess(self.Education)
        updateEducationDALObject.spUpdateEducation(education_id)

    def deleteEducation(self, education_id):
        deleteEducationDALObject = EducationDataAccess(education_id)
        deleteEducationDALObject.spDeleteEducation()

    def getAllEducations(self):
        getAllDALObject = EducationDataAccess()
        getAllDALObject.spGetAllEducations()
        self.AllDataEducation = getAllDALObject.AllData