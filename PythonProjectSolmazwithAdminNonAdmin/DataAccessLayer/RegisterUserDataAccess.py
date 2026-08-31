from DataAccessLayer.ConnectionString import *
# from datetime import *
import struct
import pyodbc

from Model.RegisterUserModel import RegisterUser


class RegisterUserDataAccess:
    def __init__(self,registerUser:RegisterUser=None):
        self.AllData = []
        # self.ConnectionString = f'Driver={"{SQL SERVER}"};Server={Server};Database={DB_Name};UID={UserName};PWD={Password};'
        self.ConnectionString = f'Driver={{{Driver}}};Server={Server};Database={DB_Name};UID={UserName};PWD={Password};'
        # self.ConnectionString = 'driver={SQL Server};server=DESKTOP-I32O9T3;database=DS_1403_09_SK;trusted_connection=yes'

        self.RegisterUser = registerUser

    def spInsertRegisterUser(self):
        commandTextSP = 'EXEC [dbo].[RegisterUsers] @UserName=?, @Password=?, @FirstName=?, @LastName=?,@isAdmin=?'
        params = (self.RegisterUser.UserName, self.RegisterUser.Password, self.RegisterUser.FirstName,
                  self.RegisterUser.LastName,  self.RegisterUser.isAdmin)

        with pyodbc.connect(self.ConnectionString) as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandTextSP, params)
            sqlConnection.commit()


