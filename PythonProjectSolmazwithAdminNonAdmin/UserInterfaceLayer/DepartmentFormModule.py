# Import necessary libraries for GUI, image handling, and date management
import tkinter
import customtkinter as ctk
from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo, showerror
from tkinter import Tk
from datetime import datetime, timedelta
from tkcalendar.dateentry import DateEntry

from BusinessLogicLayer.DepartmentBusinessLogic import DepartmentBusinessLogic
from Model.UserModule import UserModel
from Model.DepartmentModel import Department,DepartmentIdDelete

#
class DepartmentFormClass:
    # Initialize the DepartmentFormClass with user and main form references
    def __init__(self,userparam : UserModel, main_form, switch_indication_func=None, home_indicator=None):
        self.User = userparam
        self.main_form = main_form  # Store the reference to main_form
        self.switch_indication = switch_indication_func  # Store the function
        self.home_btn_indicator = home_indicator  # Store the indicator
        self.GetData = []
        self.DeleteID = 0
        self.UpdateID = 0
        self.SearchID = 0


    # Load the department form
    def department_form_load(self,userparam : UserModel):
        ctk.set_appearance_mode("Dark")  # Set appearance mode (optional, for modern look)
        ctk.set_default_color_theme("green")  # Set default color theme (optional)
        department_form = ctk.CTkToplevel(self.main_form)
        # department_form = ctk.CTk()
        department_form.title('DepartmentForm...')
        department_form.resizable(0, 0) # Disable resizing of the window
        department_form.geometry('860x360')   # Set the window size
        x = int(department_form.winfo_screenwidth() / 2 - 860 / 2)
        y = int(department_form.winfo_screenheight() / 2 - 360 / 2)
        department_form.geometry('+{}+{}'.format(x, y))
        department_form.iconbitmap('images/ImagesDepartmentForm/Department.ico')  # Set the window icon

        # Function to close the department form and show the main form
        def destroyForm():
            department_form.withdraw()  # Close the department form
            self.main_form.deiconify()  # Show the main form FIRST
            self.main_form.update()  # Force a UI refresh to ensure changes are visible
            if self.switch_indication and self.home_btn_indicator:  # Check if home indicator is available (fixed condition)
                self.switch_indication(
                    indicator_lb=self.home_btn_indicator)  # Activate home indicator AFTER showing the form
                self.main_form.update()  # Force another UI refresh to ensure the indicator change is visible

        # Function to clear all input fields
        def clearText():
            ent_department_name.delete(0, END)

        # Validation functions for input fields
        def validate50(value):
            return len(value) <= 50

        # Function to register a new job
        def registerDepartment():

            # Gather data from the input fields
            departmentName = ent_department_name.get()

            # DepartmentTitle validation
            if not departmentName :
                showinfo('Error', 'Please enter the department\'s title')
                department_form.focus_force()
                return False

            # Create a new Department object
            new_department = Department(department_name=departmentName)
            # Insert the department into the database
            department_business_logic = DepartmentBusinessLogic(new_department)
            department_id = department_business_logic.insertDepartment()  # Get the new department ID
            if department_id:  # Check if the department was inserted successfully
                showinfo('Success', 'Department registered successfully')
                department_form.focus_force()
                # Clear the tree view
                for item in tree.get_children():
                    tree.delete(item)
                # Insert the new department into the tree view
                tree.insert("", 'end', values=(department_id, departmentName))  # Insert the new department directly into the tree
                clearText()  # Clear the input fields
            else:
                showerror('Error', 'Failed to register job. Please try again.')

        def updateDepartment():
            departmentName = ent_department_name.get()

            # DepartmentName validation
            if not departmentName :
                showinfo('Error', 'Please enter the department\'s title')
                department_form.focus_force()
                return False

            # Create a Department object with the updated title
            departmentObject = Department(department_id=self.UpdateID, department_name=departmentName)
            departmentBusinessLogic = DepartmentBusinessLogic(departmentObject)
            # Update the department in the database
            departmentBusinessLogic.updateDepartment(self.UpdateID)
            showinfo('Success', 'Department updated successfully.')
            department_form.focus_force()

            # Clear the tree view
            for item in tree.get_children():
                tree.delete(item)
            # Insert the updated department directly into the tree view
            tree.insert("", 'end', values=(self.UpdateID, departmentName))  # Insert the updated department
            clearText()  # Clear the input fields

        # Function to delete a selected department
        def deleteDepartment():
            departmentObject = DepartmentIdDelete(department_id=self.DeleteID)
            departmentBusinessLogic = DepartmentBusinessLogic(departmentObject)
            departmentBusinessLogic.deleteDepartment(self.DeleteID)
            showinfo('Success', 'Department deleted successfully.')
            department_form.focus_force()
            for i in tree.get_children():
                tree.delete(i)
            departmentBusinessLogic = DepartmentBusinessLogic()
            departmentBusinessLogic.getDepartmentList()
            self.GetData = departmentBusinessLogic.AllDataDepartment

            for item in self.GetData:
                tree.insert("", 'end', values=item)
            clearText()

        # Function to select all Departments and populate the tree view
        def selectAllDepartments():
            # Clear existing tree data
            for item in tree.get_children():
                tree.delete(item)

            # Fetch all jobs from database
            departmentBL = DepartmentBusinessLogic()
            departmentBL.getAllDepartments()  # Fetch all departments
            self.GetData = departmentBL.AllDataDepartment

            # Insert all records into treeview
            for item in self.GetData:
                tree.insert("", "end",values=(item[0], item[1])) # Use empty string if no image




        # endregion
        frame = ctk.CTkFrame(department_form,  width=800, height=150)
        frame_button = ctk.CTkFrame(department_form, width=800, height=50)
        frame_grid = ctk.CTkFrame(department_form,  width=800, height=90)

        frame.grid(row=0, column=0, padx=10,sticky='nsew')
        frame_button.grid(row=1, column=0, padx=10,sticky='nsew')
        frame_grid.grid(row=2, column=0, padx=10,sticky='nsew')

        vcmd_50 = (department_form.register(validate50), '%P')

        # Label : DepartmentName
        lbl_department_name = ctk.CTkLabel(frame, text='Department Name: ')
        lbl_department_name.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        ent_department_name = ctk.CTkEntry(frame, width=300)
        ent_department_name.configure(validate="key", validatecommand=vcmd_50)
        ent_department_name.grid(row=0, column=1, padx=10, pady=10, sticky='e')

        # frameButton : clearDepartment
        btn_clear_department = ctk.CTkButton(frame_button, text='Clear', command=clearText, width=120)
        btn_clear_department.grid(row=7, column=0, padx=10, pady=10, sticky='w')
        #
        btn_select_all = ctk.CTkButton(frame_button, text='Select All', command=selectAllDepartments, width=120)
        btn_select_all.grid(row=7, column=1, padx=10, pady=10, sticky='w')
        # frameButton : insertDepartment
        btn_insert_department = ctk.CTkButton(frame_button, text='Insert', command=registerDepartment, width=120)
        btn_insert_department.grid(row=7, column=2, padx=10, pady=10, sticky='e')
        #
        # frameButton : updateDepartment
        btn_update_department = ctk.CTkButton(frame_button, text='Update', command=updateDepartment, width=120)
        btn_update_department.grid(row=7, column=3, padx=10, pady=10, sticky='w')
        #
        # frameButton : deleteDepartment
        btn_delete_department = ctk.CTkButton(frame_button, text='Delete', command=deleteDepartment, width=120)
        btn_delete_department.grid(row=7, column=4, padx=10, pady=10, sticky='w')
        #
        # frameButton : closeDepartment
        btn_backToMain_department = ctk.CTkButton(frame_button, text='BackToMain', command=destroyForm, width=120)
        btn_backToMain_department.grid(row=7, column=5, padx=10, pady=10, sticky='w')
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

        columns = ("department_id","department_name")
        tree = ttk.Treeview(frame_grid, columns=columns, show='headings')

        tree.heading("department_id", text="DepartmentID", anchor=W)
        tree.heading("department_name", text="DepartmentName", anchor=W)


        for item in self.GetData:
            tree.insert("", 'end', values=item)

        def item_selected(event):
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                record = item['values']

                ent_department_name.delete(0, END)
                ent_department_name.insert(0, record[1])  ## Set the department name in the entry field


                self.DeleteID = record[0]  ## Store the job ID for deletion
                self.UpdateID = record[0]  ## Store the job ID for updating

        tree.bind('<<TreeviewSelect>>', item_selected)

        tree.grid(row=0, column=0, sticky='nsew')
        treeYScroll = ttk.Scrollbar(frame_grid, orient=VERTICAL)
        treeXScroll = ttk.Scrollbar(frame_grid, orient=HORIZONTAL)
        treeXScroll.configure(command=tree.xview)
        tree.configure(xscrollcommand=treeXScroll.set , yscrollcommand=treeYScroll)

        frame_grid.grid(column=0, row=3, sticky=(N, S, E, W))
        tree.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
        treeXScroll.grid(column=0, row=2, columnspan=3, sticky=W + E)

        department_form.columnconfigure(0, weight=1)
        department_form.rowconfigure(0, weight=1)
        frame_grid.columnconfigure(0, weight=3)
        frame_grid.columnconfigure(1, weight=3)
        # frame_grid.columnconfigure(2, weight=3)
        # frame_grid.columnconfigure(3, weight=1)
        # frame_grid.columnconfigure(4, weight=1)
        frame_grid.rowconfigure(1, weight=1)




        department_form.mainloop()