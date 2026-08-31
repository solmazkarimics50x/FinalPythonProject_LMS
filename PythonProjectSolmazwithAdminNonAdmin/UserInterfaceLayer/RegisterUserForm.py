
import customtkinter as ctk
from tkinter import *
from tkinter import Tk

from tkinter import ttk, Entry, StringVar, Button
from tkinter import messagebox as msg
from tkinter.messagebox import showinfo


from Model.UserModule import UserModel

from Model.RegisterUserModel import RegisterUser

from BusinessLogicLayer.RegisterUserBusinessLogic import RegisterUserBusinessLogic



class RegisterUserForm:

    def __init__(self, user: UserModel):
        self.UserModel = user
        self.GetData = []
        self.DeleteID = 0
        self.UpdateID = 0

    def registerUser_FormLoad(self):
        registerUserForm = ctk.CTk()
        registerUserForm.title('User Registeration')
        registerUserForm.geometry('435x300') #('410x300')
        # registerUserForm.config(bg="LightBlue")
        positionRight = int(registerUserForm.winfo_screenwidth() / 2 - 435 / 2)
        positionDown = int(registerUserForm.winfo_screenheight() / 2 - 300 / 2)
        registerUserForm.geometry("+{}+{}".format(positionRight, positionDown))
        registerUserForm.iconbitmap('images/ImagesRegisterUsers/users.ico')




        def destroyForm():
            registerUserForm.withdraw()



        def clearText():
            # txtIsAdmin.delete(0, END)
            entLastName.delete(0, END)
            entPassword.delete(0, END)
            entFirstName.delete(0, END)
            entUserName.delete(0, END)

        def checkValidation(*args):
            username = txtUserName.get()
            password = txtPassword.get()
            if username is not None and password is not None:
                if len(username) > 20:
                    txtUserName.set(txtUserName.get()[:len(txtUserName.get()) - 1])
                if not username.isalnum():
                    txtUserName.set(txtUserName.get()[:len(txtUserName.get()) - 1])
                if len(password) > 30:
                    txtPassword.set(txtPassword.get()[:len(txtPassword.get()) - 1])

        def registerUser():

            # Get values directly from widgets (bypasses StringVar binding issues)
            username = entUserName.get().lower()
            password = entPassword.get()
            first_name = entFirstName.get()
            last_name = entLastName.get()
            is_admin = int(txtIsAdmin.get())  # Keep this for radio buttons (StringVar works here)
            is_active = 1


            #  Validate that all fields are filled
            if not username.strip() or not password.strip() or not first_name.strip() or not last_name.strip():
                msg.showerror('Error', 'All fields (Username, Password, First Name, Last Name) must be filled!')
                return  # Stop submission
            # TEMPORARY DEBUG: Print raw captured values
            # print(
            #     f"Raw Captured - Username: '{username}', Password: '{password}', FirstName: '{first_name}', LastName: '{last_name}', IsAdmin: {is_admin}")

            # Create a RegisterUser  object
            new_user = RegisterUser(userName=username, password=password, firstName=first_name, lastName=last_name, isAdmin=is_admin, isActive=is_active)
            # Create a business logic object and insert the user
            register_user_logic = RegisterUserBusinessLogic(new_user)
            try:
                register_user_logic.insertRegisterUserObject(new_user)
                msg.showinfo('Success', 'User  registered successfully!')
                clearText()  # Clear the form after successful registration
            except Exception as e:
                msg.showerror('Error', f'Failed to register user: {str(e)}')

        # Frames
        frame = ctk.CTkFrame(registerUserForm, width=410, height=300, fg_color='#73C2FB')
        # frame_label = ctk.CTkLabel(frame, text="Field...", fg_color='#73C2FB')
        # frame_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        frameButton = ctk.CTkFrame(registerUserForm, width=410, height=80, fg_color='#95C8D8')
        # frameButton_label = ctk.CTkLabel(frameButton, text="Operation ...", fg_color='#95C8D8')
        # frameButton_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        frame.grid(row=0, column=0, padx=10)
        frameButton.grid(row=1, column=0, padx=10)

        # Username
        lblUserName = ctk.CTkLabel(frame, text='Username: ', fg_color='#73C2FB', font=("Arial", 12, "bold"), text_color="black")
        lblUserName.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        txtUserName = StringVar()
        entUserName = ctk.CTkEntry(frame, textvariable=txtUserName, width=300)
        entUserName.focus()
        entUserName.grid(row=1, column=1, padx=10, pady=10, sticky='e')

        # Password
        lblPassword = ctk.CTkLabel(frame, text='Password: ', fg_color='#73C2FB', font=("Arial", 12, "bold"), text_color="black")
        lblPassword.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        txtPassword = StringVar()
        entPassword = ctk.CTkEntry(frame, show='*', textvariable=txtPassword, width=300)
        entPassword.grid(row=2, column=1, padx=10, pady=10, sticky='e')

        # First Name
        lblFirstName = ctk.CTkLabel(frame, text='FirstName: ', fg_color='#73C2FB', font=("Arial", 12, "bold"), text_color="black")
        lblFirstName.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        txtFirstName = StringVar()
        entFirstName = ctk.CTkEntry(frame, textvariable=txtFirstName, width=300)
        entFirstName.grid(row=3, column=1, padx=10, pady=10, sticky='e')

        # Last Name
        lblLastName = ctk.CTkLabel(frame, text='LastName: ', fg_color='#73C2FB', font=("Arial", 12, "bold"), text_color="black")
        lblLastName.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        txtLastName = StringVar()
        entLastName = ctk.CTkEntry(frame, textvariable=txtLastName, width=300)
        entLastName.grid(row=4, column=1, padx=10, pady=10, sticky='e')

        # Is Admin
        lblisAdmin = ctk.CTkLabel(frame, text='isAdmin: ', fg_color='#73C2FB', font=("Arial", 12, "bold"), text_color="black")
        lblisAdmin.grid(row=5, column=0, padx=10, pady=10, sticky='w')
        txtIsAdmin = StringVar(value="0")  # Default to non-admin (0)

        rb_non_admin = ctk.CTkRadioButton(frame, text='No (Non-Admin)', variable=txtIsAdmin, value="0"
                                          , font=("Arial", 12, "bold"), text_color="black")#fg_color='#73C2FB'
        rb_non_admin.grid(row=5, column=1, padx=10, pady=10, sticky='w')
        rb_admin = ctk.CTkRadioButton(frame, text='Yes (Admin)', variable=txtIsAdmin, value="1", font=("Arial", 12, "bold"), text_color="black")#, fg_color='#73C2FB'
        rb_admin.grid(row=5, column=1, padx=10, pady=10, sticky='e')

        # Buttons
        btnClearRegisterUser = ctk.CTkButton(frameButton, text='Clear', command=clearText, width=120)
        btnClearRegisterUser.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        btnInsertRegisterUser = ctk.CTkButton(frameButton, text='Insert', command=registerUser, width=120)
        btnInsertRegisterUser.grid(row=1, column=1, padx=10, pady=10, sticky='ns')




        btnBackToMain = ctk.CTkButton(frameButton, text='Close', command=destroyForm, width=120)
        btnBackToMain.grid(row=1, column=2, padx=10, pady=10, sticky='e')





        registerUserForm.mainloop()