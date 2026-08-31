# Import necessary libraries for GUI, image handling, and date management
import os
import customtkinter as ctk
from PIL import Image

from tkinter import messagebox as msg
from tkinter import ttk, filedialog, PhotoImage
from tkinter.messagebox import showinfo, showerror
from datetime import datetime, timedelta
from tkcalendar.dateentry import DateEntry


from BusinessLogicLayer.JobBusinessLogic import JobBusinessLogic
from Model.UserModule import UserModel
from Model.JobModel import Job, JobIdDelete

ctk.set_appearance_mode("Dark")  # Or "Dark"/"Light"
ctk.set_default_color_theme("green")  # Or your preferred theme

#
class JobFormClass:
    # Initialize the JobFormClass with user and main form references
    def __init__(self, userparam: UserModel, main_form, switch_indication_func=None, home_indicator=None):
        self.User = userparam
        self.main_form = main_form  # Store the reference to main_form
        self.switch_indication = switch_indication_func  # Store the function
        self.home_btn_indicator = home_indicator  # Store the indicator
        self.GetData = []
        self.DeleteID = 0
        self.UpdateID = 0
        self.SearchID = 0

    # Load the job form
    def job_form_load(self, userparam: UserModel):
        job_form = ctk.CTkToplevel(self.main_form)
        # job_form = ctk.CTk()
        job_form.tk.call('tk', 'scaling', 1.5)
        job_form.title('JobForm...')
        job_form.resizable(0, 0)  # Disable resizing of the window
        job_form.geometry('840x320')  # Set the window size
        x = int(job_form.winfo_screenwidth() / 2 - 840 / 2)
        y = int(job_form.winfo_screenheight() / 2 - 320 / 2)
        job_form.geometry('+{}+{}'.format(x, y))
        job_form.iconbitmap('images/ImagesJobForm/Job.ico')  # Set the window icon


        # Function to close the job form and show the main form
        def destroyForm():
            job_form.withdraw()
            # job_form.destroy()  # Close the job form
            self.main_form.deiconify()  # Show the main form FIRST
            self.main_form.update()  # Force a UI refresh to ensure changes are visible
            if self.switch_indication and self.home_btn_indicator:  # Check if home indicator is available (fixed condition)
                self.switch_indication(
                    indicator_lb=self.home_btn_indicator)  # Activate home indicator AFTER showing the form
                self.main_form.update()  # Force another UI refresh to ensure the indicator change is visible

        # Function to clear all input fields
        def clearText():
            ent_job_title.delete(0, ctk.END)

        # Validation functions for input fields
        def validate50(value):
            return len(value) <= 50

        # Function to register a new job
        def registerJob():
            # Gather data from the input fields
            jobTitle = ent_job_title.get()

            # JobTitle validation
            if not jobTitle:
                showinfo('Error', 'Please enter the job\'s title')
                job_form.focus_force()
                return False

            # Create a new Job object
            new_job = Job(job_title=jobTitle)
            # Insert the job into the database
            job_business_logic = JobBusinessLogic(new_job)
            job_id = job_business_logic.insertJob()  # Get the new job ID
            if job_id:  # Check if the job was inserted successfully
                showinfo('Success', 'Job registered successfully')
                job_form.focus_force()
                # Clear the tree view
                for item in tree.get_children():
                    tree.delete(item)
                # Insert the new job into the tree view
                tree.insert("", 'end', values=(job_id, jobTitle))  # Insert the new job directly into the tree
                clearText()  # Clear the input fields
            else:
                showerror('Error', 'Failed to register job. Please try again.')

        def updateJob():
            jobTitle = ent_job_title.get()

            # JobTitle validation
            if not jobTitle:
                showinfo('Error', 'Please enter the job\'s title')
                job_form.focus_force()
                return False

            # Create a Job object with the updated title
            jobObject = Job(job_id=self.UpdateID, job_title=jobTitle)
            jobBusinessLogic = JobBusinessLogic(jobObject)
            # Update the job in the database
            jobBusinessLogic.updateJob(self.UpdateID)
            showinfo('Success', 'Job updated successfully.')
            job_form.focus_force()

            # Clear the tree view
            for item in tree.get_children():
                tree.delete(item)
            # Insert the updated job directly into the tree view
            tree.insert("", 'end', values=(self.UpdateID, jobTitle))  # Insert the updated job
            clearText()  # Clear the input fields

        # Function to delete a selected job
        def deleteJob():
            jobObject = JobIdDelete(job_id=self.DeleteID)
            jobBusinessLogic = JobBusinessLogic(jobObject)
            jobBusinessLogic.deleteJob(self.DeleteID)
            showinfo('Success', 'Job deleted successfully.')
            job_form.focus_force()
            for i in tree.get_children():
                tree.delete(i)
            jobBusinessLogic = JobBusinessLogic()
            jobBusinessLogic.getJobList()
            self.GetData = jobBusinessLogic.AllDataJob

            for item in self.GetData:
                tree.insert("", 'end', values=item)
            clearText()

        # Function to select all Jobs and populate the tree view
        def selectAllJobs():
            # Clear existing tree data
            for item in tree.get_children():
                tree.delete(item)

            # Fetch all jobs from database
            jobBL = JobBusinessLogic()
            jobBL.getAllJobs()  # Fetch all jobs
            self.GetData = jobBL.AllDataJob

            # Insert all records into treeview
            for item in self.GetData:
                tree.insert("", "end", values=(item[0], item[1]))  # Use empty string if no image

        # endregion
        # CustomTkinter does not have LabelFrame; using CTkFrame with a label inside for similar effect
        frame = ctk.CTkFrame(job_form, width=750, height=300)
        frame_button = ctk.CTkFrame(job_form, width=750, height=80)
        frame_grid = ctk.CTkScrollableFrame(job_form, width=750, height=90)  # Using CTkScrollableFrame for scrollable content

        frame.pack(pady=10)
        frame_button.pack(pady=10)
        frame_grid.pack(pady=10)

        # Label: JobTitle - Moved to row 1 to avoid overlap with frame_label
        lbl_job_title = ctk.CTkLabel(frame, text='Job Title: ')
        lbl_job_title.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        ent_job_title = ctk.CTkEntry(frame, width=400)  # Adjusted width for CTkEntry
        ent_job_title.grid(row=1, column=1, padx=10, pady=10, sticky='ew')  # Changed sticky to 'ew' for better expansion

        # Note: Validation for CTkEntry might need custom implementation; removed for simplicity
        # ent_job_title.config(validate="key", validatecommand=(ent_job_title.register(validate50), "%P"))
        def validate_job_title(event):
            current_text = ent_job_title.get()
            key = event.char
            if key and key != '\x08':
                proposed_text = current_text + key
                if len(proposed_text) > 50:
                    showinfo('Input Limit', 'Job title cannot exceed 50 characters.')
                    return "break"
            return None

        ent_job_title.bind("<Key>", validate_job_title)
        # frameButton: clearJob - All buttons remain gridded for consistency
        btn_clear_job = ctk.CTkButton(frame_button, text='Clear', command=clearText, width=120)
        btn_clear_job.grid(row=1, column=0, padx=10, pady=10, sticky='w')  # Moved to row 1

        btn_select_all = ctk.CTkButton(frame_button, text='Select All', command=selectAllJobs, width=120)
        btn_select_all.grid(row=1, column=1, padx=10, pady=10, sticky='w')  # Moved to row 1

        # frameButton: insertJob
        btn_insert_job = ctk.CTkButton(frame_button, text='Insert', command=registerJob, width=120)
        btn_insert_job.grid(row=1, column=2, padx=10, pady=10, sticky='w')  # Moved to row 1

        # frameButton: updateJob
        btn_update_job = ctk.CTkButton(frame_button, text='Update', command=updateJob, width=120)
        btn_update_job.grid(row=1, column=3, padx=10, pady=10, sticky='w')  # Moved to row 1

        # frameButton: deleteJob
        btn_delete_job = ctk.CTkButton(frame_button, text='Delete', command=deleteJob, width=120)
        btn_delete_job.grid(row=1, column=4, padx=10, pady=10, sticky='w')  # Moved to row 1

        # frameButton: closeJob
        btn_backToMain_job = ctk.CTkButton(frame_button, text='BackToMain', command=destroyForm, width=120)
        btn_backToMain_job.grid(row=1, column=5, padx=10, pady=10, sticky='w')  # Moved to row 1

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

        columns = ("job_id", "job_title")
        tree = ttk.Treeview(frame_grid, columns=columns, show='headings')

        tree.heading("job_id", text="JobID", anchor='w')
        tree.heading("job_title", text="JobTitle", anchor='w')

        for item in self.GetData:
            tree.insert("", 'end', values=item)

        def item_selected(event):
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                record = item['values']

                ent_job_title.delete(0, ctk.END)
                ent_job_title.insert(0, record[1])  ## Set the job title in the entry field

                self.DeleteID = record[0]  ## Store the job ID for deletion
                self.UpdateID = record[0]  ## Store the job ID for updating

        tree.bind('<<TreeviewSelect>>', item_selected)

        tree.pack(fill='both', expand=True)  # Kept pack() - consistent with frame_grid_label

        job_form.mainloop()
