from Model.ScoreModel import Score
from Model.ScoreModel import ScoreIdDelete
from DataAccessLayer.ScoreDataAccess import ScoreDataAccess


class ScoreBusinessLogic:
    def __init__(self,score : Score = None, ):
        self.Score = score

        self.AllDataScore = []


    def insertScore(self):
        insertScoreDALObject = ScoreDataAccess(self.Score)
        return insertScoreDALObject.spInsertScore()  # Return the new term_number


    def getScoreList(self):
        GetScoreListDALObject = ScoreDataAccess()
        GetScoreListDALObject.spGetScoreList()
        self.AllDataScore = GetScoreListDALObject.AllData

    def updateScore(self, student_id, courses_id, teacher_id,term_number):
        updateScoreDALObject = ScoreDataAccess(self.Score)
        return updateScoreDALObject.spUpdateScore( student_id, courses_id, teacher_id,term_number)

    def deleteScore(self, student_id, courses_id, teacher_id, term_number):
        # Create ScoreIdDelete instance with all composite key components
        score_to_delete = ScoreIdDelete(
            student_id=student_id,
            courses_id=courses_id,
            teacher_id=teacher_id,
            term_number=term_number
        )

        # Create DataAccess with the delete object
        score_dao = ScoreDataAccess(score_to_delete)

        # Execute deletion (no need to pass parameters again)
        return score_dao.spDeleteScore(student_id, courses_id, teacher_id, term_number)


    def getAllScores(self):
        getAllDALObject = ScoreDataAccess()
        getAllDALObject.spGetAllScores()
        self.AllDataScore = getAllDALObject.AllData



    def getStudentScoreList(self):
        studentDALObject = ScoreDataAccess()
        studentDALObject.spGetStudentScoreList()  # Implement this method in DataAccess
        return studentDALObject.AllData

    def getCoursesList(self):
        coursesDALObject = ScoreDataAccess()
        coursesDALObject.spGetCoursesList()  # Implement this method in DataAccess
        return coursesDALObject.AllData


    def getTeacherScoreList(self):
        teacherDALObject = ScoreDataAccess()
        teacherDALObject.spGetTeacherScoreList()  # Implement this method in DataAccess
        return teacherDALObject.AllData




