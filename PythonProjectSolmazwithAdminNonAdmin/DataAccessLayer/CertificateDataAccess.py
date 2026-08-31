from Model.CertificateModel import *
from DataAccessLayer.ConnectionString import *
from datetime import *
import struct
import pyodbc


class CertificateDataAccess:
    def __init__(self,certificate:Certificate=None):
        self.AllData = []
        self.ConnectionString = f'Driver={"{SQL SERVER}"};Server={Server};Database={DB_Name};UID={UserName};PWD={Password};'
        self.Certificate = certificate

    def spGetCertificateList(self):
        commandTextSP = '''EXEC [dbo].[GetCertificateList]'''  # Stored procedure to be created
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]



    def spInsertCertificate(self):
        commandTextSP = 'EXEC [dbo].[sp_CertificateInsert] @CertificateTitle = ? ,@Vendor =?'
        params = (self.Certificate.certificate_title, self.Certificate.vendor,)
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            new_certificate_id = cursor.fetchone()[0]  # Fetch the new CertificateID from the result
            sqlConnection.commit()
            return new_certificate_id  # Return the new CertificateID


    def spUpdateCertificate(self, certificate_id):
        commandTextSP = 'EXEC [dbo].[UpdateCertificate] @CertificateID=?, @CertificateTitle = ?, @Vendor = ?'
        params = ( certificate_id,self.Certificate.certificate_title, self.Certificate.vendor)
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            sqlConnection.commit()


    def spDeleteCertificate(self):
        commandTextSP = 'EXEC [dbo].[SP_DeleteCertificate] @CertificateID = ?'
        params = (self.Certificate)
        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            sqlConnection.commit()

    def spGetAllCertificates(self):
        commandTextSP = '''EXEC [dbo].[GetAllCertificates]'''  # Stored procedure to be created
        with pyodbc.connect(self.ConnectionString) as conn:
            cursor = conn.cursor()
            cursor.execute(commandTextSP)
            self.AllData = [tuple(row) for row in cursor.fetchall()]