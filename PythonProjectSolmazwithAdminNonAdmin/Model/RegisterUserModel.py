
class RegisterUser :
    def __init__(self, userName, password, firstName, lastName, isAdmin, isActive=1):
        self.UserName = userName
        self.Password = password
        self.FirstName = firstName
        self.LastName = lastName
        self.isAdmin = isAdmin
        self.isActive = isActive  # Default to 1