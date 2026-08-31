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

from BusinessLogicLayer.EducationBusinessLogic import EducationBusinessLogic
from Model.UserModule import UserModel
from Model.EducationModel import Education,EducationIdDelete

ctk.set_appearance_mode("Dark")  # Set appearance mode (optional, for modern look)
ctk.set_default_color_theme("green")  # Set default color theme (optional)


class EducationFormClass:
    # Initialize the EducationFormClass with user and main form references
    def __init__(self,userparam : UserModel, main_form, switch_indication_func=None, home_indicator=None):
        self.User = userparam
        self.main_form = main_form  # Store the reference to main_form
        self.switch_indication = switch_indication_func  # Store the function
        self.home_btn_indicator = home_indicator  # Store the indicator
        self.GetData = []
        self.DeleteID = 0
        self.UpdateID = 0
        self.SearchID = 0


    # Load the education form
    def education_form_load(self,userparam : UserModel):
        # education_form = ctk.CTk()
        education_form = ctk.CTkToplevel(self.main_form)
        education_form.title('EducationForm...')
        education_form.resizable(0, 0) # Disable resizing of the window
        education_form.geometry('860x320')   # Set the window size
        x = int(education_form.winfo_screenwidth() / 2 - 860 / 2)
        y = int(education_form.winfo_screenheight() / 2 - 320 / 2)
        education_form.geometry('+{}+{}'.format(x, y))
        education_form.iconbitmap('images/ImagesEducationForm/Education.ico')  # Set the window icon

        # Function to close the education form and show the main form
        def destroyForm():
            education_form.withdraw()  # Close the education form
            self.main_form.deiconify()  # Show the main form FIRST
            self.main_form.update()  # Force a UI refresh to ensure changes are visible
            if self.switch_indication and self.home_btn_indicator:  # Check if home indicator is available (fixed condition)
                self.switch_indication(
                    indicator_lb=self.home_btn_indicator)  # Activate home indicator AFTER showing the form
                self.main_form.update()  # Force another UI refresh to ensure the indicator change is visible

        # Function to clear all input fields
        def clearText():
            ent_education.delete(0, END)

        # Validation functions for input fields
        def validate50(value):
            return len(value) <= 50

        # Function to register a new education
        def registerEducation():

            # Gather data from the input fields
            educationTitle = ent_education.get()

            # JobTitle validation
            if not educationTitle :
                showinfo('Error', 'Please enter the education\'s title')
                education_form.focus_force()
                return False

            # Create a new Education object
            new_education = Education(education=educationTitle)
            # Insert the job into the database
            education_business_logic = EducationBusinessLogic(new_education)
            education_id = education_business_logic.insertEducation()  # Get the new education ID
            if education_id:  # Check if the job was inserted successfully
                showinfo('Success', 'Education registered successfully')
                education_form.focus_force()
                # Clear the tree view
                for item in tree.get_children():
                    tree.delete(item)
                # Insert the new job into the tree view
                tree.insert("", 'end', values=(education_id, educationTitle))  # Insert the new education directly into the tree
                clearText()  # Clear the input fields
            else:
                showerror('Error', 'Failed to register education. Please try again.')

        def updateEducation():
            educationTitle = ent_education.get()

            # Education validation
            if not educationTitle :
                showinfo('Error', 'Please enter the education\'s title')
                education_form.focus_force()
                return False

            # Create a Education object with the updated title
            educationObject = Education(education_id=self.UpdateID, education=educationTitle)
            educationBusinessLogic = EducationBusinessLogic(educationObject)
            # Update the education in the database
            educationBusinessLogic.updateEducation(self.UpdateID)
            showinfo('Success', 'Education updated successfully.')
            education_form.focus_force()

            # Clear the tree view
            for item in tree.get_children():
                tree.delete(item)
            # Insert the updated education directly into the tree view
            tree.insert("", 'end', values=(self.UpdateID, educationTitle))  # Insert the updated education
            clearText()  # Clear the input fields


        # Function to delete a selected education
        def deleteEducation():
            educationObject = EducationIdDelete(education_id=self.DeleteID)
            educationBusinessLogic = EducationBusinessLogic(educationObject)
            educationBusinessLogic.deleteEducation(self.DeleteID)
            showinfo('Success', 'Education deleted successfully.')
            education_form.focus_force()
            for i in tree.get_children():
                tree.delete(i)
            educationBusinessLogic = EducationBusinessLogic()
            educationBusinessLogic.getEducationList()
            self.GetData = educationBusinessLogic.AllDataEducation

            for item in self.GetData:
                tree.insert("", 'end', values=item)
            clearText()


        # Function to select all Educations and populate the tree view
        def selectAllEducations():
            # Clear existing tree data
            for item in tree.get_children():
                tree.delete(item)

            # Fetch all educations from database
            educationBL = EducationBusinessLogic()
            educationBL.getAllEducations()  # Fetch all educations
            self.GetData = educationBL.AllDataEducation

            # Insert all records into treeview
            for item in self.GetData:
                tree.insert("", "end",values=(item[0], item[1])) # Use empty string if no image


        # endregion
        frame = ctk.CTkFrame(education_form, width=800, height=150)
        frame_button = ctk.CTkFrame(education_form,  width=800, height=50)
        frame_grid =ctk.CTkScrollableFrame(education_form,  width=800, height=80)

        # frame.pack(pady=10)
        # frame_button.pack(pady=10)
        # frame_grid.pack(pady=10)

        frame.grid(row=0, column=0, padx=10,sticky='nsew')
        frame_button.grid(row=1, column=0, padx=10,sticky='nsew')
        frame_grid.grid(row=2, column=0, padx=10,sticky='nsew')

        vcmd_50 = (education_form.register(validate50), '%P')

        # Label : Education
        lbl_education = ctk.CTkLabel(frame, text='Education: ')
        lbl_education.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        ent_education = ctk.CTkEntry(frame, width=300)
        ent_education.configure(validate="key", validatecommand=vcmd_50)
        ent_education.grid(row=0, column=1, padx=10, pady=10, sticky='e')

        # frameButton : clearEducation
        btn_clear_education = ctk.CTkButton(frame_button, text='Clear', command=clearText, width=120)
        btn_clear_education.grid(row=7, column=0, padx=10, pady=10, sticky='w')
        #
        btn_select_all = ctk.CTkButton(frame_button, text='Select All', command=selectAllEducations, width=120)
        btn_select_all.grid(row=7, column=1, padx=10, pady=10, sticky='w')
        # frameButton : insertEducation
        btn_insert_education = ctk.CTkButton(frame_button, text='Insert', command=registerEducation, width=120)
        btn_insert_education.grid(row=7, column=2, padx=10, pady=10, sticky='e')
        #
        # frameButton : updateEducation
        btn_update_education = ctk.CTkButton(frame_button, text='Update', command=updateEducation, width=120)
        btn_update_education.grid(row=7, column=3, padx=10, pady=10, sticky='w')
        #
        # frameButton : deleteEducationeducation
        btn_delete_education = ctk.CTkButton(frame_button, text='Delete', command=deleteEducation, width=120)
        btn_delete_education.grid(row=7, column=4, padx=10, pady=10, sticky='w')
        #
        # frameButton : closeEducationeducation
        btn_backToMain_education = ctk.CTkButton(frame_button, text='BackToMain', command=destroyForm, width=120)
        btn_backToMain_education.grid(row=7, column=5, padx=10, pady=10, sticky='w')
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

        columns = ("education_id","education")
        tree = ttk.Treeview(frame_grid, columns=columns, show='headings')

        tree.heading("education_id", text="EducationID", anchor=W)
        tree.heading("education", text="Education", anchor=W)




        for item in self.GetData:
            tree.insert("", 'end', values=item)

        def item_selected(event):
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                record = item['values']

                ent_education.delete(0, END)
                ent_education.insert(0, record[1])  ## Set the education in the entry field


                self.DeleteID = record[0]  ## Store the education ID for deletion
                self.UpdateID = record[0]  ## Store the education ID for updating

        tree.bind('<<TreeviewSelect>>', item_selected)

        tree.grid(row=0, column=0, sticky='nsew')
        treeYScroll = ttk.Scrollbar(frame_grid, orient=VERTICAL)
        treeXScroll = ttk.Scrollbar(frame_grid, orient=HORIZONTAL)
        treeXScroll.configure(command=tree.xview)
        tree.configure(xscrollcommand=treeXScroll.set , yscrollcommand=treeYScroll)

        frame_grid.grid(column=0, row=3, sticky=(N, S, E, W))
        tree.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
        treeXScroll.grid(column=0, row=2, columnspan=3, sticky=W + E)

        education_form.columnconfigure(0, weight=1)
        education_form.rowconfigure(0, weight=1)
        frame_grid.columnconfigure(0, weight=3)
        frame_grid.columnconfigure(1, weight=3)
        # frame_grid.columnconfigure(2, weight=0)
        # frame_grid.columnconfigure(3, weight=0)
        # frame_grid.columnconfigure(4, weight=0)
        frame_grid.rowconfigure(1, weight=1)



        education_form.mainloop()