from Model.JobModel import *
from DataAccessLayer.ConnectionString import *
from datetime import *
import struct
import pyodbc


class JobDataAccess:
    def __init__(self,job:Job=None):
        self.AllData = []
        self.ConnectionString = f'Driver={"{SQL SERVER}"};Server={Server};Database={DB_Name};UID={UserName};PWD={Password};'
        self.Job = job

    def spGetJobList(self):
        commandTextSP = '''EXEC [dbo].[GetJobList]'''  # Stored procedure to be created
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]



    def spInsertJob(self):
        commandTextSP = 'EXEC [dbo].[sp_JobInsert] @JobTitle = ?'
        params = (self.Job.job_title,)
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            new_job_id = cursor.fetchone()[0]  # Fetch the new JobID from the result
            sqlConnection.commit()
            return new_job_id  # Return the new JobID


    def spUpdateJob(self, job_id):
        commandTextSP = 'EXEC [dbo].[UpdateJob] @JobID=?, @JobTitle = ?'
        params = ( job_id,self.Job.job_title)
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            sqlConnection.commit()


    def spDeleteJob(self):
        commandTextSP = 'EXEC [dbo].[SP_DeleteJob] @JobID = ?'
        params = (self.Job)
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            sqlConnection.commit()

    def spGetAllJobs(self):
        commandTextSP = '''EXEC [dbo].[GetAllJobs]'''  # Stored procedure to be created
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]