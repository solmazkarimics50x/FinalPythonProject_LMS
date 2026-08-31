from Model.CertificateModel import Certificate
from DataAccessLayer.CertificateDataAccess import CertificateDataAccess


class CertificateBusinessLogic:
    def __init__(self, certificate: Certificate = None):
        self.Certificate = certificate
        self.AllDataCertificate = []

    def getCertificateList(self):
        GetCertificateListDALObject = CertificateDataAccess()
        GetCertificateListDALObject.spGetCertificateList()
        self.AllDataCertificate = GetCertificateListDALObject.AllData

    def insertCertificate(self):
        insertCertificateDALObject = CertificateDataAccess(self.Certificate)
        return insertCertificateDALObject.spInsertCertificate()  # Return the new certificate ID


    def updateCertificate(self, certificate_id):
        updateCertificateDALObject = CertificateDataAccess(self.Certificate)
        updateCertificateDALObject.spUpdateCertificate(certificate_id)

    def deleteCertificate(self, certificate_id):
        deleteCertificateDALObject = CertificateDataAccess(certificate_id)
        deleteCertificateDALObject.spDeleteCertificate()

    def getAllCertificates(self):
        getAllDALObject = CertificateDataAccess()
        getAllDALObject.spGetAllCertificates()
        self.AllDataCertificate = getAllDALObject.AllData