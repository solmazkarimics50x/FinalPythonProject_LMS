# Import necessary libraries for GUI, image handling, and date management
import customtkinter as ctk
import tkinter
import io
from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo, showerror
from datetime import datetime, timedelta
from tkcalendar.dateentry import DateEntry



from BusinessLogicLayer.ScoreBusinessLogic import ScoreBusinessLogic
from Model.UserModule import UserModel
from Model.ScoreModel import Score,ScoreIdDelete

ctk.set_appearance_mode("Dark")  # Set appearance mode (optional, for modern look)
ctk.set_default_color_theme("green")  # Set default color theme (optional)

class ScoreFormClass:
    # Initialize the ScoreFormClass with user and main form references
    def __init__(self,userparam = UserModel,main_form=None, switch_indication_func=None, home_indicator=None):
        self.User = userparam
        self.main_form = main_form  # Store the reference to main_form
        self.switch_indication = switch_indication_func  # Store the function
        self.home_btn_indicator = home_indicator  # Store the indicator
        self.GetData = []
        self.DeleteID = 0
        self.UpdateID = 0




    # Fetch student levels from the business logic layer
    def fetchStudentLevels(self):
        score_business_logic = ScoreBusinessLogic()
        student_levels = score_business_logic.getStudentScoreList()  # Fetch student levels
        return student_levels

    # Fetch courses levels from the business logic layer
    def fetchCoursesLevels(self):
        score_business_logic = ScoreBusinessLogic()
        courses_levels = score_business_logic.getCoursesList()  # Fetch courses levels
        return courses_levels

    # Fetch teacher levels from the business logic layer
    def fetchTeacherLevels(self):
        score_business_logic = ScoreBusinessLogic()
        teacher_levels = score_business_logic.getTeacherScoreList()  # Fetch teacher levels
        return teacher_levels



    # Load the score form
    def score_form_load(self,userparam : UserModel):
        # score_form =ctk.CTk()
        score_form = ctk.CTkToplevel(self.main_form)
        score_form.title('ScoreForm...')
        score_form.resizable(0, 0)
        score_form.geometry('860x450')
        x = int(score_form.winfo_screenwidth() / 2 - 860 / 2)
        y = int(score_form.winfo_screenheight() / 2 - 450 / 2)
        score_form.geometry('+{}+{}'.format(x, y))
        score_form.iconbitmap('images/ImagesScoreForm/Score.ico')

        # Function to close the score form and show the main form
        def destroyForm():
            score_form.withdraw()  # Close the score form
            self.main_form.deiconify()  # Show the main form FIRST
            self.main_form.update()  # Force a UI refresh to ensure changes are visible
            if self.switch_indication and self.home_btn_indicator:  # Check if home indicator is available (fixed condition)
                self.switch_indication(
                    indicator_lb=self.home_btn_indicator)  # Activate home indicator AFTER showing the form
                self.main_form.update()  # Force another UI refresh to ensure the indicator change is visible


        # Function to clear all input fields
        def clearText():
            comb_student_id.set("")
            comb_courses_id.set("")
            comb_teacher_id.set("")
            ent_score.delete(0, ctk.END)

        # Function to register a new Score
        def registerScore():

            ###Gather data from the input field
            # StudentID validation
            selected_student = comb_student_id.get()
            # Get selected student ID from the combobox
            if selected_student:
                student_id = int(selected_student.split(" - ")[0])  # Extract ID from the selected value
            else:
                showinfo('Error', 'Please select the StudentCode')
                return False

            # CoursesID validation
            selected_courses = comb_courses_id.get()
            # Get selected courses ID from the combobox
            if selected_courses:
                courses_id = int(selected_courses.split(" - ")[0])  # Extract ID from the selected value
            else:
                showinfo('Error', 'Please select the CourseName')
                return False

            # TeacherID validation
            selected_teacher = comb_teacher_id.get()
            # Get selected teacher ID from the combobox
            if selected_teacher:
                teacher_id = int(selected_teacher.split(" - ")[0])  # Extract ID from the selected value
            else:
                showinfo('Error', 'Please select the TeacherID')
                return False

            # TermNumber validation
            termNumber_value = ent_term_number.get()
            if not termNumber_value or not termNumber_value.isdigit():
                showinfo('Error', 'TermNumber is required and must contain only digits')
                score_form.focus_force()
                return False

            #Score validation
            score_value = ent_score.get()
            if not score_value or not score_value.isdigit():
                showinfo('Error', 'Score is required and must contain only digits')
                score_form.focus_force()
                return False


            # Create a new Score object
            new_score = Score(student_id = student_id, courses_id= courses_id,teacher_id= teacher_id,term_number=termNumber_value,score= score_value)
            # Insert the score into the database
            score_business_logic = ScoreBusinessLogic(new_score)
            term_number = score_business_logic.insertScore()  # Get the new term_number
            if term_number:  # Check if the courses was inserted successfully
                showinfo('Success', 'Score registered successfully')
                score_form.focus_force()
                # Clear the tree view
                for item in tree.get_children():
                    tree.delete(item)


                # Insert just the new record into the tree
                tree.insert("", 'end',
                            values=(
                                    student_id,
                                    courses_id,
                                    teacher_id,
                                    termNumber_value,
                                    score_value))

                clearText()  # Clear the input fields
            else:
                showerror('Error', 'Failed to register CourseCategory. Please try again.')

        def updateScore():
            selected_item = tree.focus()
            if not selected_item:
                showinfo('Error', 'Please select a record to update')
                return

            item = tree.item(selected_item)
            record = item['values']



            # Get the original composite key values
            original_term = record[3]
            original_student = record[0]
            original_course = record[1]
            original_teacher = record[2]
            score_value = ent_score.get()

            # Create updated Score object
            updated_score = Score(
                term_number=original_term,# Preserve original key values
                student_id=original_student,
                courses_id=original_course,
                teacher_id=original_teacher,

                score=score_value # Only update the score
            )
            # Perform update
            score_business_logic = ScoreBusinessLogic(updated_score)
            if score_business_logic.updateScore(original_student, original_course, original_teacher, original_term):
                showinfo('Success', 'Score updated successfully')

                # Clear the tree view
                for item in tree.get_children():
                    tree.delete(item)

                # Insert JUST the updated record into the tree
                tree.insert("", "end", values=(
                    updated_score.student_id,
                    updated_score.courses_id,
                    updated_score.teacher_id,
                    updated_score.term_number,
                    updated_score.score
                ))

                # Clear the form fields
                clearText()
            else:
                showerror('Error', 'Failed to update score')



        # Function to delete a Score
        def deleteScore():
            selected_item = tree.focus()
            if not selected_item:
                showinfo('Error', 'Please select a record to delete')
                return
            item = tree.item(selected_item)
            record = item['values']
            # Get the composite key values
            student_id = record[0]
            courses_id = record[1]
            teacher_id = record[2]
            term_number = record[3]
            # Call the delete method in the business logic layer
            score_business_logic = ScoreBusinessLogic()
            score_business_logic.deleteScore(student_id, courses_id, teacher_id, term_number)  # Pass the student_id & courses_id & teacher_id & term_number to delete
            showinfo('Success', 'Score deleted successfully')
            selectAllScores()  # Refresh the view



        # Function to select all Scores and populate the tree view
        def selectAllScores():
            # Clear existing tree data
            for item in tree.get_children():
                tree.delete(item)

            # Fetch all Scores from database
            scoreBL = ScoreBusinessLogic()
            scoreBL.getAllScores()  # Fetch all scores
            self.GetData = scoreBL.AllDataScore

            # Insert all records into treeview
            for item in self.GetData:

                tree.insert("", "end",
                            values=(item[0], item[1], item[2],item[3], item[4]))




        ###
        frame = ctk.CTkFrame(score_form, width=800, height=300)
        frame_button = ctk.CTkFrame(score_form, width=800, height=200)
        frame_grid = ctk.CTkFrame(score_form, width=800, height=500)

        frame.grid(row=0, column=0, padx=10,sticky='nsew')
        frame_button.grid(row=1, column=0, padx=10,sticky='nsew')
        frame_grid.grid(row=2, column=0, padx=10,sticky='nsew')
        ###

        ## Label : StudentID
        lbl_student_id = ctk.CTkLabel(frame, text='StudentID: ')
        lbl_student_id.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        comb_student_id = ctk.CTkComboBox(frame, width=300)
        comb_student_id.grid(row=0, column=1, padx=10, pady=10, sticky='e')
        # Fetch student levels and populate the combobox
        student_levels = self.fetchStudentLevels()
        comb_student_id.configure(values=[f"{level[0]} - {level[1]}" for level in student_levels])  # Assuming level[0] is ID and level[1] is StudentCode
        comb_student_id.set("Enter StudentID")
        # Label : CoursesID
        lbl_courses_id = ctk.CTkLabel(frame, text='CoursesID: ')
        lbl_courses_id.grid(row=0, column=2, padx=10, pady=10, sticky='w')
        comb_courses_id = ctk.CTkComboBox(frame, width=300)
        comb_courses_id.grid(row=0, column=3, padx=10, pady=10, sticky='e')
        # Fetch courses levels and populate the combobox
        courses_levels = self.fetchCoursesLevels()
        comb_courses_id.configure(values=[f"{level[0]} - {level[1]}" for level in courses_levels])  # Assuming level[0] is ID and level[1] is CourseName
        comb_courses_id.set("Enter CoursesID")
        ## Label : TeacherID
        lbl_teacher_id = ctk.CTkLabel(frame, text='TeacherID: ')
        lbl_teacher_id.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        comb_teacher_id = ctk.CTkComboBox(frame, width=300)
        comb_teacher_id.grid(row=1, column=1, padx=10, pady=10, sticky='e')
        # Fetch teacher levels and populate the combobox
        teacher_levels = self.fetchTeacherLevels()
        comb_teacher_id.configure(values=[f"{level[0]} - {level[1]}" for level in teacher_levels])  # Assuming level[0] is ID and level[1] is TeacherCode
        comb_teacher_id.set("Enter TeacherID")
        # Label : TermNumber
        lbl_term_number = ctk.CTkLabel(frame, text='TermNumber')
        lbl_term_number.grid(row=1, column=2, padx=10, pady=10, sticky='w')
        # Entry :TermNumber
        ent_term_number = ctk.CTkEntry(frame, width=300)
        ent_term_number.grid(row=1, column=3, padx=10, pady=10, sticky='e')
        ### Label : Score
        lbl_score = ctk.CTkLabel(frame, text='Score: ')
        lbl_score.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        ent_score = ctk.CTkEntry(frame, width=300)
        ent_score.grid(row=2, column=1, padx=10, pady=10, sticky='e')

        ## Button : Clear
        btnClearScore = ctk.CTkButton(frame_button, text='Clear', command=clearText, width=120)
        btnClearScore.grid(row=8, column=0, padx=10, pady=10, sticky='e')
        # Button: SelectAll
        btn_select_all = ctk.CTkButton(frame_button, text='Select All', command=selectAllScores, width=120)
        btn_select_all.grid(row=8, column=1, padx=10, pady=10, sticky='w')
        ## Button : Insert
        btnInsertScore = ctk.CTkButton(frame_button, text='Insert', command=registerScore, width=120)
        btnInsertScore.grid(row=8, column=2, padx=10, pady=10, sticky='e')
        ## Button : Update
        btnUpdateScore = ctk.CTkButton(frame_button, text='Update', command=updateScore, width=120)
        btnUpdateScore.grid(row=8, column=3, padx=10, pady=10, sticky='e')
        ## Button : Delete
        btnDeleteScore = ctk.CTkButton(frame_button, text='Delete', command=deleteScore, width=120)
        btnDeleteScore.grid(row=8, column=4, padx=10, pady=10, sticky='e')
        ## Button : BackToMain
        btnBackToMain = ctk.CTkButton(frame_button, text='BackToMain', command=destroyForm, width=120)
        btnBackToMain.grid(row=8, column=5, padx=10, pady=10, sticky='w')
        ###

        style = ttk.Style()
        style.theme_use('default')  # Or 'clam' for a cleaner look
        style.configure("Treeview", background=ctk.get_appearance_mode() == "Dark" and "#2b2b2b" or "#ffffff",
                        foreground=ctk.get_appearance_mode() == "Dark" and "#ffffff" or "#000000",
                        fieldbackground=ctk.get_appearance_mode() == "Dark" and "#2b2b2b" or "#ffffff")
        style.configure("Treeview.Heading", background="#4CAF50", foreground="white")  # Green to match your theme
        # New: Configure selection colors (gray background for selected rows)
        select_bg = ctk.get_appearance_mode() == "Dark" and "#666666" or "#cccccc"  # Gray shades for dark/light modes
        select_fg = ctk.get_appearance_mode() == "Dark" and "#ffffff" or "#000000"  # Ensure text remains readable
        style.map("Treeview",
                  background=[("selected", select_bg)],
                  foreground=[("selected", select_fg)])
        #frameGrid
        columns = ('student_id','courses_id','teacher_id','term_number','score')
        tree = ttk.Treeview(frame_grid, columns = columns , show = 'headings')
        # Set up headings for the Treeview

        tree.heading('student_id',text='StudentID',anchor='w')
        tree.heading('courses_id', text='CoursesID', anchor='w')
        tree.heading('teacher_id', text='TeacherID', anchor='w')
        tree.heading('term_number', text='TermNumber', anchor='w')
        tree.heading('score', text='Score', anchor='w')

        column_width = 200  # Set a common width for all columns
        for col in columns:
            tree.column(col, width=column_width)  # Set the width for each column

        # Function to populate the Treeview with data
        def populate_treeview():
            # Clear existing data in the Treeview
            tree.delete(*tree.get_children())

            # Insert new data into the Treeview
            for item in self.GetData:
                tree.insert("", "end",
                            values=(item[0], item[1], item[2], item[3],item[4]))



        def item_selected(event):
            # Get the selected item from the tree
            selected_item = tree.focus()
            if not selected_item:  # If nothing is selected, exit
                return

            item = tree.item( selected_item)
            record = item['values']



            # Populate the fields with the selected record
            comb_student_id.set(record[0])  # Set the selected value for the combobox
            comb_courses_id.set(record[1])  # Set the selected value for the combobox
            comb_teacher_id.set(record[2])  # Set the selected value for the combobox
            ent_term_number.delete(0,END)
            ent_term_number.insert(0,record[3])
            ent_score.delete(0, END)
            ent_score.insert(0, record[4])




            # Store IDs for operations (for delete/update)
            self.DeleteID = record[0] # Assuming this is the TermNumber
            self.UpdateID = record[0]  # Assuming this is the TermNumber

        # Bind selection event
        tree.bind('<<TreeviewSelect>>', item_selected)

        # Call this function after loading data into self.GetData
        populate_treeview()

        ## Bind the selection event
        tree.bind('<<TreeviewSelect>>', item_selected)
        #

        tree.grid(row=0, column=0, sticky='nsew')

        # treeYScroll = ttk.Scrollbar(frame_grid, orient=VERTICAL)
        # treeYScroll.configure(command=tree.yview)
        # Scrollbar configuration
        treeXScroll = ttk.Scrollbar(frame_grid, orient=HORIZONTAL)
        treeXScroll.configure(command=tree.xview)
        tree.configure(xscrollcommand=treeXScroll.set)
        #tree.configure(yscrollcommand=treeYScroll.set)

        #Layout configuration
        frame_grid.grid(column=0, row=3, sticky=(N, S, E, W))
        tree.grid(column=0, row=0, columnspan=3,rowspan= 2, sticky=(N, S, E, W))
        treeXScroll.grid(column=0, row=2, columnspan=3, sticky=W + E)
        #treeYScroll.grid(column=0, row=0,columnspan=3, rowspan=2, sticky=N + S)
        #
        #
        # Configure grid weights
        score_form.columnconfigure(0, weight=1)
        score_form.rowconfigure(0, weight=1)
        frame_grid.columnconfigure(0, weight=3)
        frame_grid.columnconfigure(1, weight=3)
        frame_grid.columnconfigure(2, weight=3)
        frame_grid.columnconfigure(3, weight=1)
        frame_grid.columnconfigure(4, weight=1)
        frame_grid.rowconfigure(1, weight=1)




        score_form.mainloop()

