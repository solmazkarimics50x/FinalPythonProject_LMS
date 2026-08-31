class UserModel:
    def __init__(self,user_name,password,firstname:str=None,lastname:str=None,isadmin:bool=False):
        self.UserName = user_name
        self.Password = password
        self.FirstName = firstname
        self.LastName = lastname
        self.IsAdmin = isadmin

