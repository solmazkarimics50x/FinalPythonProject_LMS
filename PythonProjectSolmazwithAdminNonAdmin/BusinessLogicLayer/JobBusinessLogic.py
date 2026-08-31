from Model.JobModel import Job
from DataAccessLayer.JobDataAccess import JobDataAccess

class JobBusinessLogic:
    def __init__(self, job: Job = None):
        self.Job = job
        self.AllDataJob = []

    def getJobList(self):
        GetJobListDALObject = JobDataAccess()
        GetJobListDALObject.spGetJobList()
        self.AllDataJob = GetJobListDALObject.AllData

    def insertJob(self):
        insertJobDALObject = JobDataAccess(self.Job)
        return insertJobDALObject.spInsertJob()  # Return the new job ID



    def updateJob(self, job_id):
        updateJobDALObject = JobDataAccess(self.Job)
        updateJobDALObject.spUpdateJob(job_id)

    def deleteJob(self, job_id):
        deleteJobDALObject = JobDataAccess(job_id)
        deleteJobDALObject.spDeleteJob()

    def getAllJobs(self):
        getAllDALObject = JobDataAccess()
        getAllDALObject.spGetAllJobs()
        self.AllDataJob = getAllDALObject.AllData