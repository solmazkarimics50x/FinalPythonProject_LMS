# Import necessary libraries for GUI and image handling
import sys

from tkinter import *
from tkinter import messagebox as msg
import tkinter as tk
from tkinter import ttk



from Model.UserModule import UserModel
from PIL import Image, ImageTk



class MainFormClass:


    # Method to load the main form with user information
    def main_form_load(self,userparam:UserModel):

        main_form = Tk()  # Create the main application window
        main_form.title('MainForm...')
        main_form.resizable(0, 0)  # Disable resizing of the window
        # main_form = ctk.CTk()
        main_form.geometry('900x680')
        # Center the window on the screen
        x = int(main_form.winfo_screenwidth() / 2 - 900 / 2)
        y = int(main_form.winfo_screenheight() / 2 - 680 / 2)
        main_form.geometry('+{}+{}'.format(x, y))
        main_form.iconbitmap('images/ImagesMainForm/mainForm.ico')  # Set the window icon



        #icons
        toggle_icon = tk.PhotoImage(file ='images/ImagesMainForm/toggle.png')
        close_icon = tk.PhotoImage(file ='images/ImagesMainForm/Exit.png')
        home_icon = tk.PhotoImage(file="images/ImagesMainForm/home.png")
        student_crud_icon = tk.PhotoImage(file="images/ImagesMainForm/student_crud.png")
        teacher_crud_icon = tk.PhotoImage(file="images/ImagesMainForm/teacher_crud.png")
        employee_crud_icon = tk.PhotoImage(file="images/ImagesMainForm/employee_crud.png")
        courses_crud_icon = tk.PhotoImage(file="images/ImagesMainForm/courses_crud.png")
        courseCategory_crud_icon = tk.PhotoImage(file="images/ImagesMainForm/courseCategory_crud.png")
        department_crud_icon = tk.PhotoImage(file="images/ImagesMainForm/department_crud.png")
        education_crud_icon = tk.PhotoImage(file="images/ImagesMainForm/education_crud.png")
        certificate_crud_icon = tk.PhotoImage(file="images/ImagesMainForm/certificate_crud.png")
        job_crud_icon = tk.PhotoImage(file="images/ImagesMainForm/job_crud.png")
        score_crud_icon = tk.PhotoImage(file="images/ImagesMainForm/Score-crud.png")

        def switch_indication(indicator_lb):

            home_btn_indicator.config(bg =menu_bar_colour)
            student_crud_btn_indicator.config(bg =menu_bar_colour)
            teacher_crud_btn_indicator.config(bg =menu_bar_colour)
            employee_crud_btn_indicator.config(bg = menu_bar_colour)
            courses_crud_btn_indicator.config(bg = menu_bar_colour)
            courseCategory_crud_btn_indicator.config(bg = menu_bar_colour)
            department_crud_btn_indicator.config(bg =menu_bar_colour)
            education_crud_btn_indicator.config(bg =menu_bar_colour)
            certificate_crud_btn_indicator.config(bg= menu_bar_colour)
            job_crud_btn_indicator.config(bg =menu_bar_colour)
            score_crud_btn_indicator.config(bg =menu_bar_colour)

            indicator_lb.config(bg = "black")

            if menu_bar_frame.winfo_width() > 45 :
                fold_menu_bar()

        close_btn_icon = tk.PhotoImage(file = "images/ImagesMainForm/close.png")


        def extending_animation():
            current_width = menu_bar_frame.winfo_width()
            if not current_width > 230:
                current_width += 10
                menu_bar_frame.config(width = current_width)
                main_form.after(ms=8 , func = extending_animation)

        def extend_menu_bar():
            extending_animation()
            toggle_icon_btn.config(image=close_btn_icon , bg = menu_bar_colour)
            toggle_icon_btn.config(command = fold_menu_bar)



        def folding_animation():
            current_width = menu_bar_frame.winfo_width()
            if current_width != 45:
                current_width -= 10
                menu_bar_frame.config(width = current_width)
                main_form.after(ms=8 , func = folding_animation)

        def fold_menu_bar():
            folding_animation()
            toggle_icon_btn.config(image = toggle_icon)
            toggle_icon_btn.config(command=extend_menu_bar)

        # Define CRUD load function for StudentFormModule
        def student_crud_load():
            main_form.withdraw()
            from UserInterfaceLayer.StudentFormModule import StudentFormClass
            # StudentFormClass(userparam, main_form).student_form_load(userparam)
            # Pass switch_indication, home_btn_indicator
            StudentFormClass(userparam, main_form, switch_indication, home_btn_indicator).student_form_load(userparam)


        # Define CRUD load function for TeacherFormModule
        def teacher_crud_load():
            main_form.withdraw()
            from UserInterfaceLayer.TeacherFormModule import TeacherFormClass
            # TeacherFormClass(userparam, main_form).teacher_form_load(userparam)
            # Pass switch_indication, home_btn_indicator
            TeacherFormClass(userparam, main_form, switch_indication, home_btn_indicator).teacher_form_load(userparam)


        # Define CRUD load function for EmployeeFormModule
        def employee_crud_load():
            main_form.withdraw()
            from UserInterfaceLayer.EmployeeFormModule import EmployeeFormClass
            # EmployeeFormClass(userparam, main_form).employee_form_load(userparam)  #, main_form
            # Pass switch_indication, home_btn_indicator
            EmployeeFormClass(userparam, main_form, switch_indication, home_btn_indicator).employee_form_load(userparam)

        # Define CRUD load function for CoursesFormModule
        def courses_crud_load():
            main_form.withdraw()  # Hide the main form instead of destroying it
            #main_form.destroy()
            from UserInterfaceLayer.CoursesFormModule import CoursesFormClass
            # courses_form_object = CoursesFormClass(userparam, main_form)
            # courses_form_object.courses_form_load(userparam)
            # Pass switch_indication, home_btn_indicator
            CoursesFormClass(userparam, main_form, switch_indication, home_btn_indicator).courses_form_load(userparam)

        # Define CRUD load function for CourseCategoryFormModule
        def course_category_crud_load():
            main_form.withdraw()  # Hide the main form instead of destroying it
            #main_form.destroy()
            from UserInterfaceLayer.CourseCategoryFormModule import CourseCategoryFormClass
            # course_category_object = CourseCategoryFormClass(userparam, main_form)
            # course_category_object.course_category_form_load(userparam)
            # Pass switch_indication, home_btn_indicator
            CourseCategoryFormClass(userparam, main_form, switch_indication, home_btn_indicator).course_category_form_load(userparam)

        # Define CRUD load function for DepartmentFormModule
        def department_crud_load():
            main_form.withdraw()  # Hide the main form instead of destroying it
            #main_form.destroy()
            from UserInterfaceLayer.DepartmentFormModule import DepartmentFormClass
            # department_object = DepartmentFormClass(userparam, main_form)
            # department_object.department_form_load(userparam)
            # Pass switch_indication, home_btn_indicator
            DepartmentFormClass(userparam, main_form, switch_indication,
                                    home_btn_indicator).department_form_load(userparam)

        # Define CRUD load function for EducationFormModule
        def education_crud_load():
            main_form.withdraw()  # Hide the main form instead of destroying it
            #main_form.destroy()
            from UserInterfaceLayer.EducationFormModule import EducationFormClass
            # education_object = EducationFormClass(userparam, main_form)
            # education_object.education_form_load(userparam)
            # Pass switch_indication, home_btn_indicator
            EducationFormClass(userparam, main_form, switch_indication,
                                home_btn_indicator).education_form_load(userparam)

        # Define CRUD load function for CertificateFormModule
        def certificate_crud_load():
            main_form.withdraw()  # Hide the main form instead of destroying it
            #main_form.destroy()
            from UserInterfaceLayer.CertificateFormModule import CertificateFormClass
            # certificate_object = CertificateFormClass(userparam,main_form)
            # certificate_object.certificate_form_load(userparam)
            # Pass switch_indication, home_btn_indicator
            CertificateFormClass(userparam, main_form, switch_indication,
                               home_btn_indicator).certificate_form_load(userparam)

        # Define CRUD load function for JobFormModule
        def job_crud_load():
            main_form.withdraw() # Hide the main form instead of destroying it

            from UserInterfaceLayer.JobFormModule import JobFormClass
            # job_object = JobFormClass(userparam, main_form)
            # job_object.job_form_load(userparam)
            # Pass switch_indication, home_btn_indicator
            JobFormClass(userparam, main_form, switch_indication,
                                 home_btn_indicator).job_form_load(userparam)

        # Define CRUD load function for ScoreFormModule
        def score_crud_load():
            main_form.withdraw() # Hide the main form instead of destroying it
            from UserInterfaceLayer.ScoreFormModule import ScoreFormClass
            # score_object = ScoreFormClass(userparam, main_form)
            # score_object.score_form_load(userparam)
            # Pass switch_indication, home_btn_indicator
            ScoreFormClass(userparam, main_form, switch_indication,
                         home_btn_indicator).score_form_load(userparam)

        def home_page():
            home_page_fm = tk.Frame(page_frame)

            # # Create blue header strip
            # header_frame = Frame(home_page_fm, bg='#007BFF', height=100)
            # header_frame.pack(fill=X, side=TOP)
            # Main content frame for Image
            content_frame = Frame(home_page_fm, bg ="#082742" ) # bg='#1e2530' ,#"#00008b",#bg ="#03045E" v"#032174"
            content_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

            # Load the circular icon image for the header
            circular_icon = Image.open('images/ImagesMainForm/SematecIcon.png').resize((80, 80), Image.LANCZOS)
            circular_icon_photo = ImageTk.PhotoImage(circular_icon)
            # Add the circular icon next to the title
            lbl_icon = Label(content_frame, image=circular_icon_photo, bg = "#082742")  # bg='#007BFF'# bg= "white' # bg='#1e2530'
            lbl_icon.image = circular_icon_photo  # Keep a reference to avoid garbage collection
            # lbl_icon.pack(side=RIGHT, padx=80)
            lbl_icon.place(x = 750, y = 10 )

            # Label to display current user information
            lbl_user_info = Label(content_frame, text=f'Current User : {userparam.FirstName} {userparam.LastName}',
                                  font=('Arial', 10, 'bold'), fg='yellow', bg="#082742") # , bg='#007BFF'v bg='#1e2530'
            # lbl_user_info.grid(row=0,column= 0 ,padx = 10,pady = 10 ,sticky= 'w')
            lbl_user_info.place(x=530, y=15)



            # # Main content frame for Image
            # content_frame = Frame(home_page_fm, bg= '#1e2530')
            # content_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
            # image for Main content
            lms_image = tk.PhotoImage(file = 'images/ImagesMainForm/LMS.png')
            # Create a label to display the image in the center of content_frame
            image_label = tk.Label(content_frame, image=lms_image, bg="#082742") #, bg='#1e2530'
            image_label.place(relx=0.5, rely=0.5, anchor='center')
            # Keep a reference to the image to prevent garbage collection
            image_label.image = lms_image

            home_page_fm.pack(fill =tk.BOTH, expand =True)

        # Page Home frame
        page_frame = tk.Frame(main_form)
        page_frame.place(relwidth=1.0, relheight=1.0 , x = 53)
        home_page()

        # Menu Bar frame
        menu_bar_colour = "#add8e6"#"yellow"
        menu_bar_frame = Frame(main_form, bg = menu_bar_colour)
        menu_bar_frame.pack(side = LEFT , fill = Y, pady = 4,padx = 5 )
        menu_bar_frame.pack_propagate(flag= False)
        menu_bar_frame.configure(width = 45)
        # Button : Toggle_menu
        toggle_icon_btn = tk.Button(menu_bar_frame, image= toggle_icon , bd = 0, bg =menu_bar_colour, activebackground=menu_bar_colour,command =extend_menu_bar)
        toggle_icon_btn.place( x= 4 , y =5)
        # Button : Exit
        exit_icon_btn = tk.Button(menu_bar_frame, image=close_icon, bd=0, bg=menu_bar_colour,
                                  activebackground=menu_bar_colour, command=main_form.destroy)
        exit_icon_btn.place(x=9, y=620)
        # Button : Home
        home_btn = tk.Button(menu_bar_frame, image= home_icon , bd = 0, bg =menu_bar_colour, activebackground=menu_bar_colour,command=lambda : switch_indication(indicator_lb=home_btn_indicator))
        home_btn.place( x= 9 , y =70, width = 30, height = 40)
        # Indicator for home_btn
        home_btn_indicator = tk.Label(menu_bar_frame ,bg =menu_bar_colour)
        home_btn_indicator.place(x = 3, y = 70, height = 40, width = 3)
        # Lable Home
        home_page_lb = tk.Label(menu_bar_frame ,text ="Home", bg = menu_bar_colour, fg = "Black", font = ("Arial",15,"bold") , anchor= tk.W)
        home_page_lb.place(x =48 , y = 70, width = 100, height = 40)
        home_page_lb.bind('<Button-1>' , lambda e : switch_indication(home_btn_indicator))

        # Button : Student CRUD
        student_crud_btn = tk.Button(menu_bar_frame, image= student_crud_icon , bd = 0, bg =menu_bar_colour, activebackground=menu_bar_colour,command=lambda : [switch_indication(indicator_lb=student_crud_btn_indicator), student_crud_load()])
        student_crud_btn.place( x= 9 , y =120, width = 30, height = 40)
        # Indicator for student_crud_btn
        student_crud_btn_indicator = tk.Label(menu_bar_frame ,bg =menu_bar_colour)
        student_crud_btn_indicator.place(x = 3, y = 120, height = 40, width = 3)
        # Lable Student CRUD
        student_crud_lb = tk.Label(menu_bar_frame ,text ="Student CRUD", bg = menu_bar_colour, fg = "Black", font = ("Arial",12,"bold") , anchor= tk.W)
        student_crud_lb.place(x =48 , y = 120, width = 150, height = 40)
        # Modified binding for student_crud_lb to add an 8-millisecond delay between switch_indication and student_crud_load
        student_crud_lb.bind('<Button-1>', lambda e: [switch_indication(student_crud_btn_indicator),main_form.after(8, student_crud_load)])
        # student_crud_lb.bind('<Button-1>' , lambda e : [switch_indication(student_crud_btn_indicator),student_crud_load()])

        # Button : Teacher CRUD
        teacher_crud_btn = tk.Button(menu_bar_frame, image= teacher_crud_icon , bd = 0, bg =menu_bar_colour, activebackground=menu_bar_colour,command=lambda : [switch_indication(indicator_lb=teacher_crud_btn_indicator),teacher_crud_load()])
        teacher_crud_btn.place( x= 4 , y =170, width = 38, height = 40)
        # Indicator for teacher_crud_btn
        teacher_crud_btn_indicator = tk.Label(menu_bar_frame ,bg =menu_bar_colour)
        teacher_crud_btn_indicator.place(x = 3, y = 170, height = 40, width = 3)
        # Lable Teacher CRUD
        teacher_crud_lb = tk.Label(menu_bar_frame ,text ="Teacher CRUD", bg = menu_bar_colour, fg = "Black", font = ("Arial",12,"bold") , anchor= tk.W)
        teacher_crud_lb.place(x =48 , y = 170, width = 150, height = 40)
        # teacher_crud_lb.bind('<Button-1>' , lambda e : [switch_indication(teacher_crud_btn_indicator),teacher_crud_load()])
        # Modified binding for teacher_crud_lb to add an 8-millisecond delay between switch_indication and teacher_crud_load
        teacher_crud_lb.bind('<Button-1>', lambda e: [switch_indication(teacher_crud_btn_indicator),
                                                      main_form.after(8, teacher_crud_load)])
        # Button : Employee CRUD
        employee_crud_btn = tk.Button(menu_bar_frame, image= employee_crud_icon , bd = 0, bg =menu_bar_colour, activebackground=menu_bar_colour,command=lambda : [switch_indication(indicator_lb=employee_crud_btn_indicator),employee_crud_load()])
        employee_crud_btn.place( x= 7 , y =220, width = 35, height = 40)
        # Indicator for employee_crud_btn
        employee_crud_btn_indicator = tk.Label(menu_bar_frame ,bg =menu_bar_colour)
        employee_crud_btn_indicator.place(x = 3, y = 220, height = 40, width = 3)
        # Lable Employee CRUD
        employee_crud_lb = tk.Label(menu_bar_frame ,text ="Employee CRUD", bg = menu_bar_colour, fg = "Black", font = ("Arial",12,"bold") , anchor= tk.W)
        employee_crud_lb.place(x =48 , y = 220, width = 200, height = 40)
        # employee_crud_lb.bind('<Button-1>' , lambda e : [switch_indication(employee_crud_btn_indicator),employee_crud_load()])
        # Modified binding for employee_crud_lb to add an 8-millisecond delay between switch_indication and employee_crud_load
        employee_crud_lb.bind('<Button-1>', lambda e: [switch_indication(employee_crud_btn_indicator),
                                                      main_form.after(8, employee_crud_load)])
        # Button : Courses CRUD
        courses_crud_btn = tk.Button(menu_bar_frame, image= courses_crud_icon , bd = 0, bg =menu_bar_colour, activebackground=menu_bar_colour,command=lambda : [switch_indication(indicator_lb=courses_crud_btn_indicator),courses_crud_load()])
        courses_crud_btn.place( x= 5 , y =270, width = 37, height = 40)
        # Indicator for courses_crud_btn
        courses_crud_btn_indicator = tk.Label(menu_bar_frame ,bg =menu_bar_colour)
        courses_crud_btn_indicator.place(x = 3, y = 270, height = 40, width = 3)
        # Lable Courses CRUD
        courses_crud_lb = tk.Label(menu_bar_frame ,text ="Courses CRUD", bg = menu_bar_colour, fg = "Black", font = ("Arial",12,"bold") , anchor= tk.W)
        courses_crud_lb.place(x =48 , y = 270, width = 200, height = 40)
        # courses_crud_lb.bind('<Button-1>' , lambda e : [switch_indication(courses_crud_btn_indicator),courses_crud_load()])
        # Modified binding for courses_crud_lb to add an 8-millisecond delay between switch_indication and courses_crud_load
        courses_crud_lb.bind('<Button-1>', lambda e: [switch_indication(courses_crud_btn_indicator),
                                                       main_form.after(8, courses_crud_load)])
        # Button : Course Category CRUD
        courseCategory_crud_btn = tk.Button(menu_bar_frame, image= courseCategory_crud_icon , bd = 0, bg =menu_bar_colour, activebackground=menu_bar_colour,command=lambda : [switch_indication(indicator_lb=courseCategory_crud_btn_indicator),course_category_crud_load()])
        courseCategory_crud_btn.place( x= 5 , y =320, width = 38, height = 40)
        # Indicator for courseCategory_crud_btn
        courseCategory_crud_btn_indicator = tk.Label(menu_bar_frame ,bg =menu_bar_colour)
        courseCategory_crud_btn_indicator.place(x = 3, y = 320, height = 40, width = 3)
        # Lable CourseCategory CRUD
        courseCategory_crud_lb = tk.Label(menu_bar_frame ,text ="CourseCategory CRUD", bg = menu_bar_colour, fg = "Black", font = ("Arial",12,"bold") , anchor= tk.W)
        courseCategory_crud_lb.place(x =48 , y = 320, width = 210, height = 40)
        # courseCategory_crud_lb.bind('<Button-1>' , lambda e : [switch_indication(courseCategory_crud_btn_indicator),course_category_crud_load()])
        # Modified binding for courseCategory_crud_lb to add an 8-millisecond delay between switch_indication and courseCategory_crud_load
        courseCategory_crud_lb.bind('<Button-1>', lambda e: [switch_indication(courseCategory_crud_btn_indicator),
                                                      main_form.after(8, course_category_crud_load)])
        # Button : Department CRUD
        department_crud_btn = tk.Button(menu_bar_frame, image= department_crud_icon , bd = 0, bg =menu_bar_colour, activebackground=menu_bar_colour,command=lambda : [switch_indication(indicator_lb=department_crud_btn_indicator),department_crud_load()])
        department_crud_btn.place( x= 5 , y =370, width = 38, height = 40)
        # Indicator for department_crud_btn
        department_crud_btn_indicator = tk.Label(menu_bar_frame ,bg =menu_bar_colour)
        department_crud_btn_indicator.place(x = 3, y = 370, height = 40, width = 3)
        # Lable Department CRUD
        department_crud_lb = tk.Label(menu_bar_frame ,text ="Department CRUD", bg = menu_bar_colour, fg = "Black", font = ("Arial",12,"bold") , anchor= tk.W)
        department_crud_lb.place(x =48 , y = 370, width = 160, height = 40)
        # department_crud_lb.bind('<Button-1>' , lambda e : [switch_indication(department_crud_btn_indicator),department_crud_load()])
        # Modified binding for department_crud_lb to add an 8-millisecond delay between switch_indication and department_crud_load
        department_crud_lb.bind('<Button-1>', lambda e: [switch_indication(department_crud_btn_indicator),
                                                             main_form.after(8, department_crud_load)])

        # Button : Education CRUD
        education_crud_btn = tk.Button(menu_bar_frame, image= education_crud_icon , bd = 0, bg =menu_bar_colour, activebackground=menu_bar_colour,command=lambda : [switch_indication(indicator_lb=education_crud_btn_indicator),education_crud_load()])
        education_crud_btn.place( x= 5 , y =420, width = 40, height = 40)
        # Indicator for education_crud_btn
        education_crud_btn_indicator = tk.Label(menu_bar_frame ,bg =menu_bar_colour)
        education_crud_btn_indicator.place(x = 3, y = 420, height = 40, width = 3)
        # Lable Education CRUD
        education_crud_lb = tk.Label(menu_bar_frame ,text ="Education CRUD", bg = menu_bar_colour, fg = "Black", font = ("Arial",12,"bold") , anchor= tk.W)
        education_crud_lb.place(x =48 , y = 420, width = 160, height = 40)
        # education_crud_lb.bind('<Button-1>' , lambda e : [switch_indication(education_crud_btn_indicator),education_crud_load()])
        # Modified binding for education_crud_lb to add an 8-millisecond delay between switch_indication and education_crud_load
        education_crud_lb.bind('<Button-1>', lambda e: [switch_indication(education_crud_btn_indicator),
                                                         main_form.after(8, education_crud_load)])
        # Button : Certificate CRUD
        certificate_crud_btn = tk.Button(menu_bar_frame, image= certificate_crud_icon , bd = 0, bg =menu_bar_colour, activebackground=menu_bar_colour,command=lambda : [switch_indication(indicator_lb=certificate_crud_btn_indicator),certificate_crud_load()])
        certificate_crud_btn.place( x= 6 , y =470, width = 40, height = 40)
        # Indicator for certificate_crud_btn
        certificate_crud_btn_indicator = tk.Label(menu_bar_frame ,bg =menu_bar_colour)
        certificate_crud_btn_indicator.place(x = 3, y = 470, height = 40, width = 3)
        # Lable Certificate CRUD
        certificate_crud_lb = tk.Label(menu_bar_frame ,text ="Certificate CRUD", bg = menu_bar_colour, fg = "Black", font = ("Arial",12,"bold") , anchor= tk.W)
        certificate_crud_lb.place(x =48 , y = 470, width = 160, height = 40)
        # certificate_crud_lb.bind('<Button-1>' , lambda e : [switch_indication(certificate_crud_btn_indicator),certificate_crud_load()])
        # Modified binding for certificate_crud_lb to add an 8-millisecond delay between switch_indication and certificate_crud_load
        certificate_crud_lb.bind('<Button-1>', lambda e: [switch_indication(certificate_crud_btn_indicator),
                                                        main_form.after(8, certificate_crud_load)])
        # Button : Job CRUD
        job_crud_btn = tk.Button(menu_bar_frame, image= job_crud_icon , bd = 0, bg =menu_bar_colour, activebackground=menu_bar_colour,command=lambda : [switch_indication(indicator_lb=job_crud_btn_indicator),job_crud_load()])
        job_crud_btn.place( x= 6 , y =520, width = 38, height = 40)
        # Indicator for job_crud_btn
        job_crud_btn_indicator = tk.Label(menu_bar_frame ,bg =menu_bar_colour)
        job_crud_btn_indicator.place(x = 3, y = 520, height = 40, width = 3)
        # Lable Job CRUD
        job_crud_lb = tk.Label(menu_bar_frame ,text ="Job CRUD", bg = menu_bar_colour, fg = "Black", font = ("Arial",12,"bold") , anchor= tk.W)
        job_crud_lb.place(x =48 , y = 520, width = 160, height = 40)
        # job_crud_lb.bind('<Button-1>' , lambda e : [switch_indication(job_crud_btn_indicator),job_crud_load()])
        # Modified binding for job_crud_lb to add an 8-millisecond delay between switch_indication and job_crud_load
        job_crud_lb.bind('<Button-1>', lambda e: [switch_indication(job_crud_btn_indicator),
                                                          main_form.after(8, job_crud_load)])

        # Button : Score CRUD
        score_crud_btn = tk.Button(menu_bar_frame, image=score_crud_icon , bd = 0, bg =menu_bar_colour, activebackground=menu_bar_colour,command=lambda : [switch_indication(indicator_lb=score_crud_btn_indicator),score_crud_load()])
        score_crud_btn.place( x= 6 , y =570, width = 38, height = 40)
        # Indicator for score_crud_btn
        score_crud_btn_indicator = tk.Label(menu_bar_frame ,bg =menu_bar_colour)
        score_crud_btn_indicator.place(x = 3, y = 570, height = 40, width = 3)
        # Lable Score CRUD
        score_crud_lb = tk.Label(menu_bar_frame ,text ="Score CRUD", bg = menu_bar_colour, fg = "Black", font = ("Arial",12,"bold") , anchor= tk.W)
        score_crud_lb.place(x =48 , y = 570, width = 160, height = 40)
        # score_crud_lb.bind('<Button-1>' , lambda e : [switch_indication(score_crud_btn_indicator),score_crud_load()])
        # Modified binding for score_crud_lb to add an 8-millisecond delay between switch_indication and score_crud_load
        score_crud_lb.bind('<Button-1>', lambda e: [switch_indication(score_crud_btn_indicator),
                                                  main_form.after(8, score_crud_load)])
        # Activate the home indicator by default when the form loads
        switch_indication(indicator_lb=home_btn_indicator)

        # Access control: Disable restricted buttons & Lables for non-admin users
        if not userparam.IsAdmin:
            courses_crud_btn.config(state='disabled')
            courses_crud_lb.config(state='disabled')
            courseCategory_crud_btn.config(state='disabled')
            courseCategory_crud_lb.config(state='disabled')
            department_crud_btn.config(state='disabled')
            department_crud_lb.config(state='disabled')
            education_crud_btn.config(state='disabled')
            education_crud_lb.config(state='disabled')
            certificate_crud_btn.config(state='disabled')
            certificate_crud_lb.config(state='disabled')
            job_crud_btn.config(state='disabled')
            job_crud_lb.config(state='disabled')
            score_crud_btn.config(state='disabled')
            score_crud_lb.config(state='disabled')
            # Note: btn_student_crud, btn_teacher_crud, btn_employee_crud, and btn_exit remain enabled


        main_form.mainloop()
