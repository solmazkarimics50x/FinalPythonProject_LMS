# Import necessary libraries for GUI, image handling, and date management

import customtkinter as ctk
import tkinter
from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo, showerror
from tkinter import Tk
from datetime import datetime, timedelta
from tkcalendar.dateentry import DateEntry

from BusinessLogicLayer.CourseCategoryBusinessLogic import CourseCategoryBusinessLogic
from Model.UserModule import UserModel
from Model.CourseCategoryModel import CourseCategory,CourseCategoryIdDelete


#
class CourseCategoryFormClass:
    # Initialize the CourseCategoryFormClass with user and main form references
    def __init__(self,userparam : UserModel, main_form, switch_indication_func=None, home_indicator=None):
        self.User = userparam
        self.main_form = main_form  # Store the reference to main_form
        self.switch_indication = switch_indication_func  # Store the function
        self.home_btn_indicator = home_indicator  # Store the indicator
        self.GetData = []
        self.DeleteID = 0
        self.UpdateID = 0
        self.SearchID = 0


    # Load the course category form
    def course_category_form_load(self,userparam : UserModel):
        ctk.set_appearance_mode("Dark")  # Set appearance mode (optional, for modern look)
        ctk.set_default_color_theme("green")  # Set default color theme (optional)
        course_category_form = ctk.CTkToplevel(self.main_form)
        # course_category_form = ctk.CTk()
        course_category_form.title('CourseCategoryForm...')
        course_category_form.resizable(0, 0) # Disable resizing of the window
        course_category_form.geometry('845x350')   # Set the window size
        x = int(course_category_form.winfo_screenwidth() / 2 - 845 / 2)
        y = int(course_category_form.winfo_screenheight() / 2 - 350 / 2)
        course_category_form.geometry('+{}+{}'.format(x, y))
        course_category_form.iconbitmap('images/ImagesCourseCategoryForm/CourseCategory.ico')  # Set the window icon

        # Function to close the course category form and show the main form
        def destroyForm():
            course_category_form.withdraw()  # Close the course_category form
            self.main_form.deiconify()  # Show the main form FIRST
            self.main_form.update()  # Force a UI refresh to ensure changes are visible
            if self.switch_indication and self.home_btn_indicator:  # Check if home indicator is available (fixed condition)
                self.switch_indication(
                    indicator_lb=self.home_btn_indicator)  # Activate home indicator AFTER showing the form
                self.main_form.update()  # Force another UI refresh to ensure the indicator change is visible

        # Function to clear all input fields
        def clearText():
            ent_course_category_name.delete(0, END)
            ent_english_course_category_name.delete(0, END)

        # Validation functions for input fields
        def validate50(value):
            return len(value) <= 50

        # Function to register a new job
        def registerCourseCategory():

            # Gather data from the input fields
            courseCategoryName = ent_course_category_name.get()
            englishCourseCategoryName = ent_english_course_category_name.get()


            # CourseCategoryName validation
            if not courseCategoryName :
                showinfo('Error', 'Please enter the CourseCategory\'s name')
                course_category_form.focus_force()
                return False

            # englishCourseCategoryName validation
            if not englishCourseCategoryName :
                showinfo('Error', 'Please enter the EnglishCourseCategory\'s name')
                course_category_form.focus_force()
                return False

            # Create a new CourseCategory object
            new_course_category = CourseCategory(course_category_name=courseCategoryName, english_course_category_name = englishCourseCategoryName)
            # Insert the course_category into the database
            course_category_business_logic = CourseCategoryBusinessLogic(new_course_category)
            course_category_id = course_category_business_logic.insertCourseCategory()  # Get the new course_category ID
            if course_category_id:  # Check if the course_category was inserted successfully
                showinfo('Success', 'CourseCategory registered successfully')
                course_category_form.focus_force()
                # Clear the tree view
                for item in tree.get_children():
                    tree.delete(item)
                # Insert the new course_category into the tree view
                tree.insert("", 'end', values=(course_category_id, courseCategoryName,englishCourseCategoryName))  # Insert the new course_category directly into the tree
                clearText()  # Clear the input fields
            else:
                showerror('Error', 'Failed to register CourseCategory. Please try again.')

        def updateCourseCategory():
            courseCategoryName = ent_course_category_name.get()
            englishCourseCategoryName = ent_english_course_category_name.get()

            # CourseCategoryName validation
            if not courseCategoryName :
                showinfo('Error', 'Please enter the CourseCategory\'s name')
                course_category_form.focus_force()
                return False

            # englishCourseCategoryName validation
            if not englishCourseCategoryName :
                showinfo('Error', 'Please enter the EnglishCourseCategory\'s name')
                course_category_form.focus_force()
                return False

            # Create a CourseCategory object with the updated title
            courseCategoryObject = CourseCategory(course_category_id=self.UpdateID,
                                            course_category_name=courseCategoryName,
                                            english_course_category_name = englishCourseCategoryName)
            courseCategoryBusinessLogic = CourseCategoryBusinessLogic(courseCategoryObject)
            # Update the certificate in the database
            courseCategoryBusinessLogic.updateCourseCategory(self.UpdateID)
            showinfo('Success', 'CourseCategory updated successfully.')
            course_category_form.focus_force()

            # Clear the tree view
            for item in tree.get_children():
                tree.delete(item)
            # Insert the updated CourseCategory directly into the tree view
            tree.insert("", 'end', values=(self.UpdateID, courseCategoryName, englishCourseCategoryName))  # Insert the updated CourseCategory
            clearText()  # Clear the input fields

        # Function to delete a selected courseCategory
        def deleteCourseCategory():
            courseCategoryObject = CourseCategoryIdDelete(course_category_id=self.DeleteID)
            courseCategoryBusinessLogic = CourseCategoryBusinessLogic(courseCategoryObject)
            courseCategoryBusinessLogic.deleteCourseCategory(self.DeleteID)
            showinfo('Success', 'CourseCategory deleted successfully.')
            course_category_form.focus_force()
            for i in tree.get_children():
                tree.delete(i)
            courseCategoryBusinessLogic = CourseCategoryBusinessLogic()
            courseCategoryBusinessLogic.getCourseCategoryList()
            self.GetData = courseCategoryBusinessLogic.AllDataCourseCategory

            for item in self.GetData:
                tree.insert("", 'end', values=item)
            clearText()

        # Function to select all CourseCategories and populate the tree view
        def selectAllCourseCategories():
            # Clear existing tree data
            for item in tree.get_children():
                tree.delete(item)

            # Fetch all course categories from database
            courseCategoryBL = CourseCategoryBusinessLogic()
            courseCategoryBL.getAllCourseCategories()  # Fetch all course categories
            self.GetData = courseCategoryBL.AllDataCourseCategory

            # Insert all records into treeview
            for item in self.GetData:
                tree.insert("", "end",values=(item[0], item[1],item[2]))





        # endregion
        frame =ctk.CTkFrame(course_category_form, width=900, height=200)
        frame_button = ctk.CTkFrame(course_category_form, width=900, height=50)
        frame_grid = ctk.CTkFrame(course_category_form, width=900, height=80)

        frame.grid(row=0, column=0, padx=10,sticky='nsew')
        frame_button.grid(row=1, column=0, padx=10,sticky='nsew')
        frame_grid.grid(row=2, column=0, padx=10,sticky='nsew')

        vcmd_50 = (course_category_form.register(validate50), '%P')

        # Label: CourseCategoryName
        lbl_course_category_name = ctk.CTkLabel(frame, text='CourseCategory Name: ')
        lbl_course_category_name.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        ent_course_category_name = ctk.CTkEntry(frame, placeholder_text="Enter CourseCategory Name", width=200)
        ent_course_category_name.configure(validate="key", validatecommand=vcmd_50)
        ent_course_category_name.grid(row=0, column=1, padx=10, pady=5, sticky='e')
        # Label: EnglishCourseCategoryName
        lbl_english_course_category_name = ctk.CTkLabel(frame, text='EnglishCourseCategory Name: ')
        lbl_english_course_category_name.grid(row=0, column=2, padx=20, pady=5, sticky='w')
        ent_english_course_category_name = ctk.CTkEntry(frame, placeholder_text="Enter EnglishCourseCategory Name", width=200)
        ent_english_course_category_name.configure(validate="key", validatecommand=vcmd_50)
        ent_english_course_category_name.grid(row=0, column=3, padx=10, pady=5, sticky='e')

        # frameButton: clearCourseCategory
        btn_clear_course_category = ctk.CTkButton(frame_button, text='Clear', command=clearText, width=120)
        btn_clear_course_category.grid(row=7, column=0, padx=5, pady=10, sticky='w')
        btn_select_all = ctk.CTkButton(frame_button, text='Select All', command=selectAllCourseCategories, width=120)
        btn_select_all.grid(row=7, column=1, padx=5, pady=10, sticky='w')
        # frameButton: insertCourseCategory
        btn_insert_course_category = ctk.CTkButton(frame_button, text='Insert', command=registerCourseCategory,
                                                   width=120)
        btn_insert_course_category.grid(row=7, column=2, padx=5, pady=10, sticky='e')
        # frameButton: updateCourseCategory
        btn_update_course_category = ctk.CTkButton(frame_button, text='Update', command=updateCourseCategory, width=120)
        btn_update_course_category.grid(row=7, column=3, padx=5, pady=10, sticky='w')
        # frameButton: deleteCourseCategory
        btn_delete_course_category = ctk.CTkButton(frame_button, text='Delete', command=deleteCourseCategory, width=120)
        btn_delete_course_category.grid(row=7, column=4, padx=5, pady=10, sticky='w')
        # frameButton: closeCourseCategory
        btn_backToMain_job = ctk.CTkButton(frame_button, text='BackToMain', command=destroyForm, width=120)
        btn_backToMain_job.grid(row=7, column=5, padx=5, pady=10, sticky='w')

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

        columns = ("course_category_id","course_category_name","english_course_category_name")
        tree = ttk.Treeview(frame_grid, columns=columns, show='headings')

        tree.heading("course_category_id", text="CourseCategoryID", anchor=W)
        tree.heading("course_category_name", text="CourseCategoryName", anchor=W)
        tree.heading("english_course_category_name", text="EnglishCourseCategoryName", anchor=W)

        # Set column widths
        tree.column("course_category_id", width=120, minwidth=120, stretch=NO)
        tree.column("course_category_name", width=350, minwidth=350, stretch=NO)
        tree.column("english_course_category_name", width=350, minwidth=350, stretch=NO)


        for item in self.GetData:
            tree.insert("", 'end', values=item)

        def item_selected(event):
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                record = item['values']

                ent_course_category_name.delete(0, END)
                ent_course_category_name.insert(0, record[1])  ## Set the course category name in the entry field

                ent_english_course_category_name.delete(0, END)
                ent_english_course_category_name.insert(0,record[2])


                self.DeleteID = record[0]  ## Store the course category ID for deletion
                self.UpdateID = record[0]  ## Store the course category ID for updating

        tree.bind('<<TreeviewSelect>>', item_selected)

        tree.grid(row=0, column=0, sticky='nsew')
        treeYScroll = ttk.Scrollbar(frame_grid, orient=VERTICAL)
        treeXScroll = ttk.Scrollbar(frame_grid, orient=HORIZONTAL)
        treeXScroll.configure(command=tree.xview)



        frame_grid.grid(column=0, row=3, sticky=(N, S, E, W))
        tree.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
        treeXScroll.grid(column=0, row=2, columnspan=3, sticky=W + E)

        course_category_form.columnconfigure(0, weight=1)
        course_category_form.rowconfigure(0, weight=1)
        frame_grid.columnconfigure(0, weight=3)
        frame_grid.columnconfigure(1, weight=3)
        frame_grid.columnconfigure(2, weight=3)
        frame_grid.columnconfigure(3, weight=1)
        frame_grid.columnconfigure(4, weight=1)
        frame_grid.rowconfigure(1, weight=1)


        course_category_form.mainloop()