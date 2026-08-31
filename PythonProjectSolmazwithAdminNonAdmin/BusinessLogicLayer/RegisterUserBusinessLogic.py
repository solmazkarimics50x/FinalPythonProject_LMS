
from DataAccessLayer.RegisterUserDataAccess import RegisterUserDataAccess
from Model.RegisterUserModel import RegisterUser




class RegisterUserBusinessLogic:
    def __init__(self, registerUser:RegisterUser  = None):
        self.RegisterUser  = registerUser

    def insertRegisterUserObject(self, registerUser):

        insertRegisterUserObjectDALObject = RegisterUserDataAccess(registerUser)
        insertRegisterUserObjectDALObject.spInsertRegisterUser()

