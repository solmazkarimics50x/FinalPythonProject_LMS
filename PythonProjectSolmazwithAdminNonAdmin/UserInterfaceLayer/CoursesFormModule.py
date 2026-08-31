# Import necessary libraries for GUI, image handling, and date management
import tkinter
import customtkinter as ctk
import io
from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo, showerror
from datetime import datetime, timedelta
from tkcalendar.dateentry import DateEntry
from PIL import Image


from BusinessLogicLayer.CoursesBusinessLogic import CoursesBusinessLogic
from Model.UserModule import UserModel
from Model.CoursesModel import Courses,CoursesIdDelete


class CoursesFormClass:
    # Initialize the CoursesFormClass with user and main form references
    def __init__(self,userparam = UserModel,main_form=None, switch_indication_func=None, home_indicator=None):
        self.User = userparam
        self.main_form = main_form  # Store the reference to main_form
        self.switch_indication = switch_indication_func  # Store the function
        self.home_btn_indicator = home_indicator  # Store the indicator
        self.GetData = []
        self.DeleteID = 0
        self.UpdateID = 0
        self.current_syllabus_file = None
        self.uploaded_syllabus_file = None  # Initialize uploaded_photo attribute


    # Fetch course_category levels from the business logic layer
    def fetchCourseCategoryLevels(self):
        courses_business_logic = CoursesBusinessLogic()
        course_category_levels = courses_business_logic.getCourseCategoryList()  # Fetch course_category levels
        return course_category_levels


    def fetchPrerequisiteLevels(self):
        courses_business_logic = CoursesBusinessLogic()
        courses_business_logic.getAllCoursess()  # Fetch all Coursess
        # print("Fetched Prerequisites:", courses_business_logic.AllDataCourses)  # Debugging line
        return courses_business_logic.AllDataCourses  # Return the fetched data

    # Load the courses form
    def courses_form_load(self,userparam : UserModel):
        ctk.set_appearance_mode("Dark")  # Set appearance mode (optional, for modern look)
        ctk.set_default_color_theme("green")  # Set default color theme (optional)

        # courses_form =ctk.CTk()
        courses_form =ctk.CTkToplevel(self.main_form)
        courses_form.title('CoursesForm...')
        courses_form.tk.call('tk', 'scaling', 1.5)
        courses_form.resizable(0, 0)
        courses_form.geometry('720x430')
        x = int(courses_form.winfo_screenwidth() / 2 - 720 / 2)
        y = int(courses_form.winfo_screenheight() / 2 - 430/ 2)
        courses_form.geometry('+{}+{}'.format(x, y))
        courses_form.iconbitmap('images/ImagesCoursesForm/Courses.ico')


        def upload_syllabus_file():
            try:
                f_types = [('PDF Files', '*.pdf'), ('All Files', '*.*')]
                filename = filedialog.askopenfilename(filetypes=f_types)
                if filename:
                    # Read the file as binary data
                    with open(filename, 'rb') as file:
                        self.uploaded_syllabus_file = file.read()  # Store the binary data for later use
                    # Optionally, you can display the file name in the button or a label
                    btn_upload_syllabus_file.configure(text=f'Uploaded: {filename.split("/")[-1]}')
            except Exception as e:
                msg.showerror("Error", f"An error occurred while uploading the syllabus file: {e}")



        # Function to close the courses form and show the main form
        def destroyForm():
            courses_form.withdraw()  # Close the courses form
            self.main_form.deiconify()  # Show the main form FIRST
            self.main_form.update()  # Force a UI refresh to ensure changes are visible
            if self.switch_indication and self.home_btn_indicator:  # Check if home indicator is available (fixed condition)
                self.switch_indication(
                    indicator_lb=self.home_btn_indicator)  # Activate home indicator AFTER showing the form
                self.main_form.update()  # Force another UI refresh to ensure the indicator change is visible

        # Function to clear all input fields
        def clearText():
            ent_course_name.delete(0,END)
            ent_english_course_name.delete(0,END)
            ent_duration.delete(0,END)
            # Clear the uploaded syllabus file state
            self.uploaded_syllabus_file = None  # Reset the uploaded syllabus file variable
            btn_upload_syllabus_file.configure(text='Upload SyllabusFile')  # Reset button text
            comb_course_category_id.set('')  # Clear the combobox
            comb_prerequisite_id.set('') # Clear the combobox


        # Validation functions for input fields
        def validate50(value):
            return  len(value) <= 50

        # Function to register a new Course
        def registerCourses():

            # Gather data from the input fields
            courseName = ent_course_name.get()
            englishCourseName = ent_english_course_name.get()


            # courseName validation
            if not courseName :
                showinfo('Error', 'Please enter the course\'s name')
                courses_form.focus_force()
                return False

            # englishCourseName validation
            if not englishCourseName :
                showinfo('Error', 'Please enter the EnglishCourse\'s name')
                courses_form.focus_force()
                return False

            #Duration validation
            duration_value = ent_duration.get()
            if not duration_value or not duration_value.isdigit():
                showinfo('Error', 'Duration is required and must contain only digits')
                courses_form.focus_force()
                return False

            # SyllabusFile validation # Check if an file was uploaded
            if not self.uploaded_syllabus_file:
                showinfo('Error', 'Please upload a Syllabus File of the Courses.')
                return False

            # Use the uploaded syllabus file directly as binary data
            syllabus_file_data = self.uploaded_syllabus_file  # No need to convert to PDF format

            # Prerequisite ID handling -
            selected_prerequisite = comb_prerequisite_id.get()
            prerequisite_id = None  # Default to None

            # Only try to parse if an actual prerequisite is selected
            if selected_prerequisite and selected_prerequisite != "None - No PrerequisiteCourses":
                try:
                    prerequisite_id = int(selected_prerequisite.split(" - ")[0])
                except (ValueError, IndexError):
                    showinfo('Error', 'Invalid prerequisite selection format')
                    return False


            # CourseCategoryID validation
            selected_courseCategory = comb_course_category_id.get()
            # Get selected coursecategory ID from the combobox
            if selected_courseCategory:
                course_category_id = int(selected_courseCategory.split(" - ")[0])  # Extract ID from the selected value
            else:
                showinfo('Error', 'Please select the course\'s category')
                return False

            # Create a new Courses object
            new_courses = Courses(course_name=courseName, english_course_name = englishCourseName,
                                  duration= duration_value,syllabus_file= syllabus_file_data,
                                  prerequisite_id= prerequisite_id, course_category_id = course_category_id)
            # Insert the courses into the database
            courses_business_logic = CoursesBusinessLogic(new_courses)
            courses_id = courses_business_logic.insertCourses()  # Get the new courses ID
            if courses_id:  # Check if the courses was inserted successfully
                showinfo('Success', 'Course registered successfully')
                courses_form.focus_force()
                # Clear the tree view
                for item in tree.get_children():
                    tree.delete(item)

                # Show only the newly inserted course in the tree view
                # Read the syllabus file to display a preview
                syllabus_preview = "Syllabus Uploaded" if syllabus_file_data else ""

                # Format syllabus file for display (first 50 chars of binary data)
                # syllabus_display = f"Syllabus (size: {len(syllabus_file_data)} bytes)"

                # Insert just the new record into the tree
                tree.insert("", 'end',
                            values=(courses_id,
                                    courseName,
                                    englishCourseName,
                                    duration_value,
                                    syllabus_preview,
                                    prerequisite_id,
                                    course_category_id))

                clearText()  # Clear the input fields
            else:
                showerror('Error', 'Failed to register CourseCategory. Please try again.')


        def updateCourses():
            courseName = ent_course_name.get()
            englishCourseName = ent_english_course_name.get()

            # CourseName validation
            if not courseName :
                showinfo('Error', 'Please enter the Course\'s name')
                courses_form.focus_force()
                return False

            # englishCourseName validation
            if not englishCourseName :
                showinfo('Error', 'Please enter the EnglishCourse\'s name')
                courses_form.focus_force()
                return False
            #Duration validation
            duration_value = ent_duration.get()
            if not duration_value or not duration_value.isdigit():
                showinfo('Error', 'Duration is required and must contain only digits')
                courses_form.focus_force()
                return False

            # SyllabusFile validation # Check if an file was uploaded
            if not self.uploaded_syllabus_file:
                showinfo('Error', 'Please upload a Syllabus File of the Courses.')
                return False

            # Use the uploaded syllabus file directly as binary data
            syllabus_file_data = self.uploaded_syllabus_file  # No need to convert to PDF format

            # Prerequisite ID handling -
            selected_prerequisite = comb_prerequisite_id.get()
            prerequisite_id = None  # Default to None

            # Only try to parse if an actual prerequisite is selected
            if selected_prerequisite and selected_prerequisite != "None - No PrerequisiteCourses":
                try:
                    prerequisite_id = int(selected_prerequisite.split(" - ")[0])
                except (ValueError, IndexError):
                    showinfo('Error', 'Invalid prerequisite selection format')
                    return False


            # CourseCategoryID validation
            selected_courseCategory = comb_course_category_id.get()
            # Get selected coursecategory ID from the combobox
            if selected_courseCategory:
                course_category_id = int(selected_courseCategory.split(" - ")[0])  # Extract ID from the selected value
            else:
                showinfo('Error', 'Please select the course\'s category')
                return False


            # Create a Courses object with the updated title
            coursesObject = Courses(courses_id=self.UpdateID,
                                            course_name=courseName,
                                            english_course_name = englishCourseName,
                                            duration= duration_value,
                                            syllabus_file= syllabus_file_data,
                                            prerequisite_id= prerequisite_id,
                                            course_category_id = course_category_id)

            # Update the course in the database
            coursesBusinessLogic = CoursesBusinessLogic(coursesObject)
            coursesBusinessLogic.updateCourses(self.UpdateID)

            showinfo('Success', 'Course updated successfully.')
            courses_form.focus_force()
            # Clear the tree view
            for item in tree.get_children():
                tree.delete(item)

            # Show only the updated course in the tree view
            syllabus_preview = "Syllabus Updated" if self.uploaded_syllabus_file else "No Syllabus"

            tree.insert("", 'end',
                        values=(self.UpdateID,
                                courseName,
                                englishCourseName,
                                duration_value,
                                syllabus_preview,
                                prerequisite_id,
                                course_category_id))

            clearText()  # Clear the input fields

        def deleteCourses():
            if self.DeleteID == 0:  # Check if a course is selected
                showinfo('Error', 'Please select a course to delete.')
                return
            # Create a CoursesIdDelete object with the selected course ID
            coursesObject = CoursesIdDelete(courses_id=self.DeleteID)
            coursesBusinessLogic = CoursesBusinessLogic(coursesObject)
            # Delete the course from the database
            coursesBusinessLogic.deleteCourses(self.DeleteID)
            # Show success message
            showinfo('Success', 'Course deleted successfully.')
            # Clear the tree view
            for item in tree.get_children():
                tree.delete(item)

            # Fetch updated course list from the database
            coursesBusinessLogic.getCoursesList()
            self.GetData = coursesBusinessLogic.AllDataCourses
            # Populate the tree view with the updated data
            for item in self.GetData:
                syllabus_display = "Syllabus Available" if item[4] else "No Syllabus"
                tree.insert("", 'end', values=(item[0], item[1], item[2], item[3], syllabus_display, item[5], item[6]))
            clearText()  # Clear the input fields



        # Function to select all Coursess and populate the tree view
        def selectAllCoursess():
            # Clear existing tree data
            for item in tree.get_children():
                tree.delete(item)

            # Fetch all coursess from database
            coursesBL = CoursesBusinessLogic()
            coursesBL.getAllCoursess()  # Fetch all coursess
            self.GetData = coursesBL.AllDataCourses

            # Insert all records into treeview with syllabus indicator
            for item in self.GetData:
                # syllabus_display = f"Syllabus (size: {len(item[4])} bytes)" if item[4] else "No syllabus"
                syllabus_display = "Syllabus Available" if item[4] else "No Syllabus"
                tree.insert("", "end",
                            values=(item[0], item[1], item[2],
                                    item[3], syllabus_display,
                                    item[5], item[6]))

        vcmd_50 = (courses_form.register(validate50), '%P')

        #frame
        frame = ctk.CTkFrame(courses_form, width = 700,height= 200)
        frame_button  = ctk.CTkFrame(courses_form,width = 700 , height= 150)
        frame_grid = ctk.CTkFrame(courses_form,width= 700,height=190)


        frame.grid(row=0,column=0, padx= 10,sticky='nsew')
        frame_button.grid(row=1,column=0 , padx=10 ,sticky='nsew' )
        frame_grid.grid(row=2,column=0, sticky='nsew' , padx = 10)
        ##
        # Label : CourseName
        lbl_course_name = ctk.CTkLabel(frame, text='CourseName: ')
        lbl_course_name.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        # Entry : FirstName
        ent_course_name = ctk.CTkEntry(frame, width=200, placeholder_text= " Enter CourseName")
        ent_course_name.configure(validate="key", validatecommand=vcmd_50)
        ent_course_name.grid(row=0, column=1, padx=10, pady=5, sticky='e')
        # Label : EnglishCourseName
        lbl_english_course_name = ctk.CTkLabel(frame, text='EnglishCourseName: ')
        lbl_english_course_name.grid(row=0, column=2, padx=10, pady=5, sticky='w')
        # Entry : EnglishCourseName
        ent_english_course_name = ctk.CTkEntry(frame, width=200, placeholder_text="Enter EnglishCourseName")
        ent_english_course_name.configure(validate="key", validatecommand=vcmd_50)
        ent_english_course_name.grid(row=0, column=3, padx=10, pady=5, sticky='e')
        # Label : Duration
        #
        lbl_duration = ctk.CTkLabel(frame, text='Duration')
        lbl_duration.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        # Entry : Duration (add placeholder_text here if desired)
        ent_duration = ctk.CTkEntry(frame, width=200, placeholder_text="Enter Duration")
        ent_duration.grid(row=1, column=1, padx=10, pady=5, sticky='e')


        # SyllabusFile
        lbl_syllabus_file = ctk.CTkLabel(frame, text='SyllabusFile: ')
        lbl_syllabus_file.grid(row=1, column=2, padx=10, pady=5, sticky='w')
        btn_upload_syllabus_file = ctk.CTkButton(frame, text='Upload SyllabusFile', command=upload_syllabus_file,
                                                 width=200)
        btn_upload_syllabus_file.grid(row=1, column=3, padx=10, pady=5, sticky='e')
        # Label : CourseCategoryID
        lbl_course_category_id = ctk.CTkLabel(frame, text='CourseCategoryID: ')
        lbl_course_category_id.grid(row=2, column=0, padx=10, pady=5, sticky='w')
        comb_course_category_id = ctk.CTkComboBox(frame, width=200)
        comb_course_category_id.grid(row=2, column=1, padx=10, pady=5, sticky='e')

        # Fetch course_category levels and populate the combobox
        course_category_levels = self.fetchCourseCategoryLevels()
        comb_course_category_id.configure(values=[f"{level[0]} - {level[1]}" for level in course_category_levels])
        comb_course_category_id.set("Select CourseCategoryID")

        # Label : PrerequisiteID
        lbl_prerequisite_id = ctk.CTkLabel(frame, text='PrerequisiteID: ')
        lbl_prerequisite_id.grid(row=2, column=2, padx=10, pady=5, sticky='w')
        comb_prerequisite_id = ctk.CTkComboBox(frame, width=200)
        comb_prerequisite_id.grid(row=2, column=3, padx=10, pady=5, sticky='e')

        # Fetch prerequisites and add "No Prerequisite" option
        prerequisites = self.fetchPrerequisiteLevels()
        comb_prerequisite_id.configure(
            values=["None - No Prerequisite"] + [f"{cou[0]} - {cou[1]} {cou[2]}" for cou in prerequisites])
        comb_prerequisite_id.set("Select PrerequisiteID")

        # frameButton : clearCourses
        btn_clear_courses = ctk.CTkButton(frame_button, text='Clear', command=clearText, width=120)
        btn_clear_courses.grid(row=0, column=0, padx=10, pady=3, sticky='w')
        btn_select_all = ctk.CTkButton(frame_button, text='Select All', command=selectAllCoursess, width=120)
        btn_select_all.grid(row=0, column=1, padx=10, pady=3, sticky='w')
        # frameButton : insertCourses
        btn_insert_courses = ctk.CTkButton(frame_button, text='Insert', command=registerCourses, width=120)
        btn_insert_courses.grid(row=0, column=2, padx=10, pady=3, sticky='e')
        # frameButton : updateCourses
        btn_update_courses = ctk.CTkButton(frame_button, text='Update', command=updateCourses, width=120)
        btn_update_courses.grid(row=0, column=3, padx=10, pady=3, sticky='w')
        # frameButton : deleteCourses
        btn_delete_courses = ctk.CTkButton(frame_button, text='Delete', command=deleteCourses, width=120)
        btn_delete_courses.grid(row=0, column=4, padx=10, pady=3, sticky='w')
        #
        #frameButton : closeCourses
        btn_backToMain_courses = ctk.CTkButton(frame_button, text= 'BackToMain', command=destroyForm,width= 120)
        btn_backToMain_courses.grid(row=1,column=4, padx=10, pady=3,sticky='w')
        #
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
        columns = ('courses_id','course_name','english_course_name','duration','syllabus_file','prerequisite_id','course_category_id')
        tree = ttk.Treeview(frame_grid, columns = columns , show = 'headings')
        # Set up headings for the Treeview
        tree.heading('courses_id', text='CourseID', anchor='w')
        tree.heading('course_name',text='CourseName',anchor='w')
        tree.heading('english_course_name', text='EnglishCourseName', anchor='w')
        tree.heading('duration', text='Duration', anchor='w')
        tree.heading('syllabus_file', text='SyllabusFile', anchor='w')
        tree.heading('prerequisite_id', text='PrerequisiteID', anchor='w')
        tree.heading('course_category_id', text='CourseCategoryID', anchor='w')


        # Set the width of each column
        # Set the width of each column
        tree.column('courses_id', width=100)
        tree.column('course_name', width=150)
        tree.column('english_course_name', width=150)
        tree.column('duration', width=100)
        tree.column('syllabus_file', width=150)  # Increased width for syllabus info
        tree.column('prerequisite_id', width=120)
        tree.column('course_category_id', width=150)
        # column_width = 200  # Set a common width for all columns
        # for col in columns:
        #     tree.column(col, width=column_width)  # Set the width for each column

        # Function to populate the Treeview with data
        def populate_treeview():
            tree.delete(*tree.get_children())  # Clear existing data
            for item in self.GetData:
                syllabus_display = "Syllabus Available" if item[
                    4] else "No Syllabus"  # Assuming item[4] is the syllabus binary data
                tree.insert("", "end", values=(item[0], item[1], item[2], item[3], syllabus_display, item[5], item[6]))

        # def populate_treeview():
        #     # Clear existing data in the Treeview
        #     tree.delete(*tree.get_children())
        #
        #     # Insert new data into the Treeview
        #     for item in self.GetData:
        #         tree.insert("", "end",
        #                     values=(item[0], item[1], item[2], item[3], "",
        #                             item[5], item[6]))



        def item_selected(event):
            # Get the selected item from the tree
            selected_item = tree.focus()
            if not selected_item:  # If nothing is selected, exit
                return

            item = tree.item( selected_item)
            record = item['values']

            # Store the current syllabus file (assuming it's at index 4)
            self.current_syllabus_file = next((x[4] for x in self.GetData if x[0] == record[0]), None)

            # Populate the fields with the selected record
            ent_course_name.delete(0, END)
            ent_course_name.insert(0, record[1])
            ent_english_course_name.delete(0, END)
            ent_english_course_name.insert(0, record[2])
            ent_duration.delete(0, END)
            if record[3] is not None:
                ent_duration.insert(0, str(record[3]))  # Ensure it's a string
            # ent_duration.insert(0, record[3])

            # For prerequisite (assuming prerequisites list is available)
            if record[5]:  # If not None
                matching_prereq = next(
                    (f"{cou[0]} - {cou[1]} {cou[2]}" for cou in prerequisites if cou[0] == record[5]), None)
                comb_prerequisite_id.set(matching_prereq or "None - No Prerequisite")
            else:
                comb_prerequisite_id.set("None - No Prerequisite")
            # For course category (similarly)
            if record[6]:
                matching_cat = next(
                    (f"{level[0]} - {level[1]}" for level in course_category_levels if level[0] == record[6]), None)
                comb_course_category_id.set(matching_cat or "")
            else:
                comb_course_category_id.set("")

            # comb_prerequisite_id.set(record[5])  # Set the selected value for the combobox
            # comb_course_category_id.set(record[6])  # Set the selected value for the combobox


            # Store IDs for operations (for delete/update)
            self.DeleteID = record[0] # Assuming this is the Courses ID
            self.UpdateID = record[0]  # Assuming this is the Courses ID

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
        courses_form.columnconfigure(0, weight=1)
        courses_form.rowconfigure(0, weight=1)
        frame_grid.columnconfigure(0, weight=3)
        frame_grid.columnconfigure(1, weight=3)
        frame_grid.columnconfigure(2, weight=3)
        frame_grid.columnconfigure(3, weight=1)
        frame_grid.columnconfigure(4, weight=1)
        frame_grid.rowconfigure(1, weight=1)





        courses_form.mainloop()
