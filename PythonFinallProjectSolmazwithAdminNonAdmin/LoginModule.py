# Import necessary libraries for GUI and database handling
from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk


from UserInterfaceLayer.MainFormModule import MainFormClass
from Model.UserModule import UserModel
from UserInterfaceLayer.RegisterUserForm import RegisterUserForm
from BusinessLogicLayer.RegisterUserBusinessLogic import RegisterUserBusinessLogic
from babel import dates
from babel import numbers
from tkcalendar import DateEntry



import sqlite3
import pyodbc
from PIL import Image, ImageTk  # Import PIL for image handling




class LoginModule:
    # Initialize the Login Module class with a UserModel instance
    def __init__(self, user: UserModel):
        self.UserModel = user
        self.GetData = []
        self.DeleteID = 0
        self.UpdateID = 0

    # def run(self):

# Create the main application window
logic_form = Tk()
logic_form.title('Logic...')
logic_form.resizable(0, 0)
# logic_form.geometry('390x140')
logic_form.geometry('600x410')
logic_form.configure(bg = '#040405')
# Center the window on the screen
x = int(logic_form.winfo_screenwidth() / 2 - 600 / 2)
y = int(logic_form.winfo_screenheight() / 2 - 410 / 2)
logic_form.geometry('+{}+{}'.format(x, y))
logic_form.iconbitmap('images/ImagesLoginModule/login.ico')

lb_heading = Label(logic_form,text = "WELCOME", font = ("yu gothic ui", 20 , "bold"), fg = "white", bg = '#040405'  )
lb_heading.place(x = 20 , y =30, width = 300 , height= 30)

#**********left side Image****************
side_image = Image.open("images\\ImagesLoginModule\\side_image_ login.png")
photo = ImageTk.PhotoImage(side_image)
side_image_lb = Label(logic_form , image= photo,bg = '#040405')
side_image_lb.image = photo
side_image_lb.place(x = 20 , y =100)

#**********sign in Image****************
sign_in_image = Image.open("images\\ImagesLoginModule\\image_sign in _ login.png")
photo = ImageTk.PhotoImage(sign_in_image)
sign_in_image_lb = Label(logic_form , image= photo,bg = '#040405')
sign_in_image_lb.image = photo
sign_in_image_lb.place(x = 400 , y =50)

sign_in_lb = Label(logic_form , text = "Sign in" , font = ("yu gothic ui", 17 , "bold"), fg = "white", bg = '#040405')
sign_in_lb.place( x= 408 , y = 120)



# Load images for show/hide password functionality
eye_open_image = ImageTk.PhotoImage(Image.open("images/ImagesLoginModule/eye_open.png").resize((14, 14)))  # Adjust path and size
eye_closed_image = ImageTk.PhotoImage(Image.open("images/ImagesLoginModule/eye_closed.png").resize((14, 14)))  # Adjust path and size
# Function to close the login form
def destroyForm():
    logic_form.destroy()
# Function to load the user registration form
def userRegisteration_FormLoad():
    registerUserObject = RegisterUserForm(UserModel)
    registerUserObject.registerUser_FormLoad()
# Function to toggle password visibility
def toggle_password_visibility():
    if ent_password.cget('show') == '*':
        ent_password.config(show='')  # Show password
        btn_toggle_password.config(image=eye_open_image)  # Change icon to open eye
    else:
        ent_password.config(show='*')  # Hide password
        btn_toggle_password.config(image=eye_closed_image)  # Change icon to closed eye

# Function to handle login using SQL Server
def login_function_sql_server(*args):
    user_name = txt_user_name.get().lower()
    password = txt_password.get()
    # SQL Server connection string and command ## region SQLite Code
    # connection_string_sql_server = ('driver={SQL Server};server=DESKTOP-I32O9T3;'
    #                                 'database=DS_1403_09_SK;trusted_connection=yes')

    connection_string_sql_server = ('driver={SQL Server};server=DESKTOP-I32O9T3;'
                                    'database=DS_1403_09_SK;UID=sa;PWD=123')


    command_text_sql_server = '''EXEC [dbo].[login_check] ?,? '''
    try:
        # Connect to SQL Server and execute login check
        with pyodbc.connect(connection_string_sql_server) as connection_sql_server:

            cursor = connection_sql_server.cursor()
            cursor.execute(command_text_sql_server,(user_name, password))
            rows = cursor.fetchall()
        # Check if any rows were returned (successful login
        if len(rows) > 0 :
            user_object = UserModel(user_name = rows[0][0],
                                    password= rows[0][1],
                                    firstname= rows[0][2],
                                    lastname= rows[0][3],
                                    isadmin= rows[0][4]
                                    )
            msg.showinfo('Login', message=f' Welcome {user_object.FirstName} {user_object.LastName} ')
            logic_form.destroy()  # Close the login form
            main_form_object = MainFormClass()  # Create main form object
            main_form_object.main_form_load(user_object)  # Load main form with user data
        else :
            msg.showerror('Error', message=f' Username or Password is incorrect!!! ')
    except:
        msg.showerror('Error', message=f' SQL Server does not exist or access denied!!! ')

    # endregion

# Function to handle login using SQLite
def login_function_sqlite(*args):
    user_name = txt_user_name.get().lower()
    password = txt_password.get()

    # SQLite connection string and command
    # region SQLite Code
    connection_string_sqlite = 'DB/sematec_db.db'
    command_text_sqlite = '''SELECT UserName,Password,FirstName,LastName,isAdmin FROM Users
                              WHERE UserName = ? and Password = ? and isActive = 1 '''
    # Connect to SQLite and execute login check
    with sqlite3.connect(connection_string_sqlite) as connection_sqlite:
        cursor = connection_sqlite.cursor()
        cursor.execute(command_text_sqlite,(user_name, password))
        rows = cursor.fetchall()
    # Check if any rows were returned (successful login)
    if len(rows) > 0 :
        msg.showinfo('Login', message=f' Welcome {rows[0][2]} {rows[0][3]} ')
    else:
        msg.showerror('Error', message=f' Username or Password is incorrect!!! ')

    # endregion



# Create and place the UserName label and entry field
## Label : UserName
lbl_user_name = Label(logic_form, text='UserName: ', font = ("yu gothic ui", 10, "bold"), fg = '#4f404d' , bg = '#040405' )
lbl_user_name.place(x =300, y = 180)
## Entry : UserName
txt_user_name = StringVar()
ent_user_name = Entry(logic_form,textvariable=txt_user_name, highlightthickness=0,relief=FLAT,bg = '#040405',fg="white" , font = ("yu gothic ui", 12, "bold") )#fg= "#6b6a69"
ent_user_name.place(x = 340 , y = 210, width= 180)
ent_user_line=Canvas(logic_form, width=180, height=2.0, bg ="blue",highlightthickness=0)#bg="#cdb9b1"
ent_user_line.place( x= 340 , y = 230)

# Create and place the Password label and entry field
## Label : Password
lbl_password = Label(logic_form, text='Password: ', font = ("yu gothic ui", 10, "bold"), fg = '#4f404d' , bg = '#040405' )
lbl_password.place(x = 300 , y= 250)
## Entry : Password
txt_password = StringVar()
ent_password = Entry(logic_form,textvariable=txt_password, highlightthickness=0,relief=FLAT,bg = '#040405',fg="white" , font = ("yu gothic ui", 12, "bold")  , show='*')
ent_password.place(x= 340 , y =270 , width= 180)
ent_password_line=Canvas(logic_form, width=180, height=2.0, bg ="blue",highlightthickness=0)#bg="#cdb9b1"
ent_password_line.place(x=340 , y = 290)


# Button to toggle password visibility
btn_toggle_password = Button(logic_form, image=eye_closed_image, command=toggle_password_visibility, borderwidth=1)
btn_toggle_password.place(x= 540 , y =272)



# Button to trigger the login function
btn_login = Button(logic_form, text='LogIn',command=login_function_sql_server, width=19, font = ("yu gothic ui", 12, "bold"), bd=0,bg = "#0079ff", cursor="hand2", activebackground="#0949ff", fg= "white")#bg ="#3047ff"
btn_login.place(x = 340, y =305)

# Button to add a registration button
btnQuit = Button(logic_form, text='SignIn', width=19, command=userRegisteration_FormLoad, font = ("yu gothic ui", 12, "bold"), bd=0,bg = "#0079ff", cursor="hand2", activebackground="#0949ff", fg= "white")
btnQuit.place(x = 340, y =350)

#logic_form.bind('<Return>', login_function_sql_server)


ent_user_name.focus()  # Focus on the username entry
ent_user_name.icursor(0)  # Position the insertion cursor at the beginning (index 0)

# Start the main event loop
logic_form.mainloop()

# if __name__ == "__main__":
#   login_app = LoginModule(UserModel())
#   login_app.run()


