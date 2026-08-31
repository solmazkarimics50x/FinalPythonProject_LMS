# Import necessary libraries for GUI, image handling, and date management
import customtkinter as ctk
from customtkinter import CTkImage

import tkinter
import io
from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo, showerror
# from tkinter import Toplevel  # Import Toplevel
from customtkinter import CTkToplevel
from PIL import Image, ImageTk,ImageDraw, ImageFont
from datetime import datetime, timedelta
from tkcalendar.dateentry import DateEntry
from openpyxl import Workbook  # Added for Excel export


from BusinessLogicLayer.EmployeeBusinessLogic import EmployeeBusinessLogic
from Model.UserModule import UserModel
from Model.EmployeeModel import Employee,EmployeeUpdate,EmployeeIdDelete

# Set CustomTkinter appearance (add this for modern look)
ctk.set_appearance_mode("Dark")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("green")


class EmployeeFormClass:
    # Initialize the EmployeeFormClass with user and main form references
    def __init__(self,userparam = UserModel,main_form=None, switch_indication_func=None, home_indicator=None):
        self.User = userparam
        self.uploaded_photo = None  # Initialize uploaded_photo attribute
        self.main_form = main_form  # Store the reference to main_form
        self.switch_indication = switch_indication_func  # Store the function
        self.home_btn_indicator = home_indicator  # Store the indicator
        self.GetData = []
        self.DeleteID = 0
        self.UpdateID = 0
        self.SearchID = 0
        self.img = None  # Initialize image holder
        self.employee_photos = {}  # Dictionary to hold student photos
        self.photo_cache = {}  # For storing loaded images
        self.uploaded_photo = None  # Initialize uploaded_photo attribute
        self.current_photo_data = None

    #Fetch education levels from the business logic layer
    def fetchEducationLevels(self):
        employee_business_logic = EmployeeBusinessLogic()
        education_levels = employee_business_logic.getEducationList()  # Fetch education levels
        return education_levels

    # Fetch job levels from the business logic layer
    def fetchJobLevels(self):
        employee_business_logic = EmployeeBusinessLogic()
        job_levels = employee_business_logic.getJobList()  # Fetch job levels
        return job_levels

    # Fetch department levels from the business logic layer
    def fetchDepartmentLevels(self):
        employee_business_logic = EmployeeBusinessLogic()
        department_levels = employee_business_logic.getDepartmentList()  # Fetch department levels
        return department_levels


    def fetchManagerLevels(self):
        employee_business_logic = EmployeeBusinessLogic()
        employee_business_logic.getAllEmployees()  # Fetch all employees
        # print("Fetched Managers:", employee_business_logic.AllDataEmployee)  # Debugging line
        return employee_business_logic.AllDataEmployee  # Return the fetched data


    # Load the employee form
    def employee_form_load(self,userparam : UserModel):
        #employee_form =Tk()
        # employee_form = Toplevel()  # Use Toplevel instead of Tk for a new window
        employee_form = CTkToplevel()
        employee_form.tk.call('tk', 'scaling', 1.5)
        employee_form.title('EmployeeForm...')
        employee_form.resizable(0, 0)
        if userparam.IsAdmin:
            employee_form.geometry('885x780')   # Set the window size
        else:
            employee_form.geometry('885x520')  # Set the window size

        # employee_form.geometry('930x730')
        x = int(employee_form.winfo_screenwidth() / 2 - 885 / 2)
        y = int(employee_form.winfo_screenheight() / 2 - 780 / 2)
        employee_form.geometry('+{}+{}'.format(x, y))
        employee_form.iconbitmap('images/ImagesEmployeeForm/Employee.ico')

        # Function to upload a photo
        def upload_photo():
            try:
                f_types = [('Jpg Files', '*.jpg'), ('All Files', '*.*')]
                filename = filedialog.askopenfilename(filetypes=f_types)
                if filename:
                    # Load the image
                    pil_img = Image.open(filename)
                    pil_img = pil_img.resize((100, 100), Image.LANCZOS)  # Resize image to fit in the label
                    # Use CustomTkinter's CTkImage for better integration
                    image = CTkImage(pil_img, size=(100, 100))
                    # Display the image in the label
                    photo_label.configure(image=image)
                    photo_label.image = image  # Keep a reference to avoid garbage collection

                    # Store the image data in an instance variable
                    self.uploaded_photo = pil_img  # Store the PIL image for later use
            except Exception as e:
                msg.showerror("Error", f"An error occurred while uploading the photo: {e}")

        # Function to close the employee form and show the main form
        def destroyForm():
            employee_form.withdraw()  # Close the employee form
            self.main_form.deiconify()  # Show the main form FIRST
            self.main_form.update()  # Force a UI refresh to ensure changes are visible
            if self.switch_indication and self.home_btn_indicator:  # Check if home indicator is available (fixed condition)
                self.switch_indication(
                    indicator_lb=self.home_btn_indicator)  # Activate home indicator AFTER showing the form
                self.main_form.update()  # Force another UI refresh to ensure the indicator change is visible

        # Function to clear all input fields
        def clearText():
            ent_first_name.delete(0,END)
            ent_last_name.delete(0,END)
            ent_date_birthdate.set_date(datetime.now().date()) # Set to current date
            ent_national_code.delete(0, END)  # Clear the national code
            txt_gender.set('')  # Reset gender selection
            ent_address.delete(0,END)
            ent_mobile.delete(0, END)  # Clear the mobile number
            photo_label.configure(image=None)  # Clear the image
            photo_label.image = None  # Clear the reference to avoid garbage collection
            comb_education_id.set('')  # Clear the combobox
            ent_employee_id.delete(0,END)
            # Reset marital_status selection
            txt_marital_status.set('')  # or set to a default value if needed
            comb_job_id.set('')  # Clear the combobox
            comb_department_id.set('')  # Clear the combobox
            ent_date_hire_date.set_date(datetime.now().date())  # Set to current date
            ent_insurance_number.delete(0,END)
            ent_account_number.delete(0,END)# Clear the account_number
            comb_manager_id.set('') # Clear the combobox


        # Validation functions for input fields
        def validate_national_code(value):
            if value == "":
                return True # Allow empty input
            return value.isdigit() and  len(value) <= 10   # Allow only digits and up to 10 digits
        def validate_mobile(value):
            if value == "":
                return True # Allow empty input
            return value.isdigit() and len(value) <= 11  # Allow only digits and up to 11 digits
        def validate_account_number(value):
            if value == "":
                return True # Allow empty input
            return value.isdigit() and len(value) <= 16  # Allow only digits and up to 16 digits

        def validate_insurance_number(value):
            if value == "":
                return True  # Allow empty input if it's optional
            return value.isdigit() and len(value) <= 16  # Adjust length as needed

        def validate20(value):
            return  len(value) <= 20
        def validate30(value):
            return  len(value) <= 30
        def validate40(value):
            return  len(value) <= 40

            # Function to export Treeview data to Excel

        def export_to_excel():
            try:
                # Get all items from the Treeview
                items = tree.get_children()
                if not items:
                    showerror("Error", "No data available to export.")
                    return

                # Create a new Excel workbook and sheet
                wb = Workbook()
                ws = wb.active
                ws.title = "Employees"

                # Define headers (excluding 'photo' as it's binary; we'll add a 'Photo Exists?' column)
                headers = ['PersonID', 'FirstName', 'LastName', 'BirthDate', 'NationalCode', 'Gender', 'Address',
                           'Mobile', 'Photo Exists?', 'EducationID', 'EmployeeID', 'MaritalStatus', 'JobID',
                           'DepartmentID', 'HireDate', 'InsuranceNumber', 'AccountNumber', 'ManagerID']
                ws.append(headers)

                # Iterate through each item in the Treeview
                for item in items:
                    values = tree.item(item, 'values')
                    # Prepare row data: skip the photo column (index 8) and add a photo existence check
                    photo_exists = "Yes" if next((x[8] for x in self.GetData if x[0] == values[0]), None) else "No"
                    row_data = list(values[:8]) + [photo_exists] + list(values[9:])  # Insert photo check at index 8
                    ws.append(row_data)

                # Prompt user to save the file
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                    title="Save Excel File"
                )
                if file_path:
                    wb.save(file_path)
                    showinfo("Success", f"Data exported successfully to {file_path}")
            except Exception as e:
                showerror("Error", f"Failed to export data: {str(e)}")



        # Function to register a new teacher
        def registerEmployee():
            # Gather data from the input fields
            firstName = ent_first_name.get()
            lastName = ent_last_name.get()
            nationalCode = ent_national_code.get()
            # Convert gender from number to string
            gender_value = txt_gender.get()
            gender_string = "Male" if gender_value == "1" else "Female" if gender_value == "2" else None

            # Convert marital_status from number to string
            marital_status_value = txt_marital_status.get()
            marital_status_string = "M" if marital_status_value == "1" else "S" if marital_status_value == "2" else None


            # Photo validation # Check if an image was uploaded
            if not self.uploaded_photo:
                showinfo('Error', 'Please upload a photo of the employee.')
                return False

            # Convert the uploaded photo to binary data
            if self.uploaded_photo:
                with io.BytesIO() as output:
                    self.uploaded_photo.save(output, format='JPEG')  # Save the image in JPEG format
                    photo_data = output.getvalue()  # Get the binary data
            else:
                photo_data = None  # Handle case where no photo is uploaded

            ### Validation for input fields
            # FirstName validation
            if not firstName or not firstName.isalpha():
                showinfo('Error', 'FirstName is required and must contain only letters')
                employee_form.focus_force()
                return False
            # LastName validation
            if not lastName or not lastName.isalpha():
                showinfo('Error', 'LastName is required and must contain only letters')
                employee_form.focus_force()
                return False
            # NationalCode validation
            if not nationalCode or not nationalCode.isdigit() or len(nationalCode) != 10:
                showinfo('Error', 'NationalCode must be 10 digits')
                employee_form.focus_force()
                return False
            # Gender validation
            if not gender_string:
                showinfo('Error', 'Please select the employee\'s gender')
                employee_form.focus_force()
                return False

            # Address validation
            address_value = ent_address.get()
            if not address_value:
                showinfo('Error', 'Please enter the employee\'s address')
                employee_form.focus_force()
                return False


            # Mobile validation
            mobile_value = ent_mobile.get()
            if not mobile_value or not mobile_value.isdigit()or len(mobile_value) != 11:
                showinfo('Error', 'Mobile must be 11 digits')
                employee_form.focus_force()
                return False

            # EducationID validation
            selected_education = comb_education_id.get()
            # Get selected education ID from the combobox
            if selected_education:
                education_id = int(selected_education.split(" - ")[0])  # Extract ID from the selected value
            else:
                showinfo('Error', 'Please select the employee\'s education')
                return False

            # EmployeeID validation
            employeeId_value = ent_employee_id.get()
            if not employeeId_value or not employeeId_value.isdigit():
                showinfo('Error', 'EmployeeID is required and must contain only digits')
                employee_form.focus_force()
                return False

            # MaritalStatus validation
            if not marital_status_string:
                showinfo('Error', 'Please select the employee\'s marital_status')
                employee_form.focus_force()
                return False

            # JobID validation
            selected_job = comb_job_id.get()
            # Get selected job ID from the combobox
            if selected_job:
                job_id = int(selected_job.split(" - ")[0])  # Extract ID from the selected value
            else:
                showinfo('Error', 'Please select the employee\'s job')
                return False

            # DepartmentID validation
            selected_department = comb_department_id.get()
            # Get selected department ID from the combobox
            if selected_department:
                department_id = int(selected_department.split(" - ")[0])  # Extract ID from the selected value
            else:
                showinfo('Error', 'Please select the employee\'s department')
                return False

            # InsuranceNumber validation
            insuranceNumber_value = ent_insurance_number.get()
            if not insuranceNumber_value or not insuranceNumber_value.isdigit():
                showinfo('Error', 'InsuranceNumber is required and must contain only digits')
                employee_form.focus_force()
                return False

            # AccountNumber validation
            account_number_value = ent_account_number.get()
            if not account_number_value or not account_number_value.isdigit()or len(account_number_value) != 16:
                showinfo('Error', 'AccountNumber must be 16 digits')
                employee_form.focus_force()
                return False

            # Manager ID handling - allows NULL for boss-level employees
            selected_manager = comb_manager_id.get()
            manager_id = None  # Default to None

            # Only try to parse if an actual manager is selected
            if selected_manager and selected_manager != "None - No Manager":
                try:
                    manager_id = int(selected_manager.split(" - ")[0])
                except (ValueError, IndexError):
                    showinfo('Error', 'Invalid manager selection format')
                    return False


            # Check if the national code already exists
            employee_business_logic = EmployeeBusinessLogic()
            if employee_business_logic.checkNationalCodeExists(nationalCode):
                showinfo('Error', 'This National Code has already been registered.')
                #employee_form.focus_force()
                ent_national_code.focus_force()
                return False

            # Create a new Employee object
            new_employee = Employee(
                first_name=firstName,
                last_name=lastName,
                birthdate=ent_date_birthdate.get_date().strftime('%Y-%m-%d'),  # Format date
                national_code=nationalCode,
                gender=gender_string,  # Use the string representation of gender
                address=address_value,
                mobile=mobile_value,
                photo=photo_data,  #Pass the binary photo data
                education_id=education_id,  # Use the selected education ID
                #education_id=int(comb_education_id.get()),
                employee_id=employeeId_value,
                marital_status= marital_status_string,
                job_id=job_id,  # Use the selected job ID
                department_id=department_id,  # Use the selected department ID
                hire_date = ent_date_hire_date.get_date().strftime('%Y-%m-%d'),  # Format date
                insurance_number= insuranceNumber_value,
                account_number= account_number_value,
                manager_id = manager_id)  # Use the selected manager ID and # Can be None for boss-level employees
            # Insert the employee into the database
            employee_business_logic.insertEmployee(new_employee)
            showinfo('Success', 'Employee registered successfully')
            employee_form.focus_force()

            # Clear the tree view (only if admin and tree is visible)
            if userparam.IsAdmin:
                for i in tree.get_children():
                    tree.delete(i)

                # Get the person_id from the newly inserted employee
                person_id = new_employee.person_id  # Assuming you have a way to get the person_id from the new_employee object
                # Call getEmployeeList with the person_id
                employee_business_logic.getEmployeeList(person_id)
                self.GetData = employee_business_logic.AllDataEmployee
                for item in self.GetData:
                    tree.insert("",'end',values=( item[0],item[1], item[2], item[3], item[4], item[5], item[6], item[7], "", item[9], item[10],item[11],
                                                               item[12],item[13],item[14],item[15],item[16],item[17]))
                clearText() # Clear form for admins
                # For non-admins, do NOT clear the form so they can generate a card immediately



        # Function to update an existing employee
        # Function to update an existing employee (admin only)
        def updateEmployee():
            # Gather data from the input fields
            firstName = ent_first_name.get()
            lastName = ent_last_name.get()
            nationalCode = ent_national_code.get()
            gender_value = txt_gender.get()
            gender_string = "Male" if gender_value == "1" else "Female" if gender_value == "2" else None

            # Convert marital_status from number to string
            marital_status_value = txt_marital_status.get()
            marital_status_string = "M" if marital_status_value == "1" else "S" if marital_status_value == "2" else None



            # Get the current photo data (either newly uploaded or existing)
            photo_data = None
            if self.uploaded_photo:
                # If new photo was uploaded, use it
                with io.BytesIO() as output:
                    self.uploaded_photo.save(output, format='JPEG')
                    photo_data = output.getvalue()
            else:
                # Otherwise, get the photo from the currently selected employee
                selected_item = tree.focus()
                if selected_item:
                    item = tree.item(selected_item)
                    record = item['values']
                    student_id = record[0]
                    for student in self.GetData:
                        if student[0] == student_id:
                            photo_data = student[8]  # Photo data is at index 8
                            break

            #### Validation for input fields
            # Validation for photo upload
            if not photo_data:
                showinfo('Error', 'Please upload a photo of the employee.')
                return False

            # FirstName validation
            if not firstName or not firstName.isalpha():
                showinfo('Error', 'FirstName is required and must contain only letters')
                employee_form.focus_force()
                return False

            # LastName validation
            if not lastName or not lastName.isalpha():
                showinfo('Error', 'LastName is required and must contain only letters')
                employee_form.focus_force()
                return False
            # NationalCode validation
            if not nationalCode or not nationalCode.isdigit() or len(nationalCode) != 10:
                showinfo('Error', 'NationalCode must be 10 digits')
                employee_form.focus_force()
                return False
            # Gender validation
            if not gender_string:
                showinfo('Error', 'Please select the employee\'s gender')
                employee_form.focus_force()
                return False

            # Address validation
            address_value = ent_address.get()
            if not address_value:
                showinfo('Error', 'Please enter the employee\'s address')
                employee_form.focus_force()
                return False

            # Mobile validation
            mobile_value = ent_mobile.get()
            if not mobile_value or not mobile_value.isdigit()or len(mobile_value) != 11:
                showinfo('Error', 'Mobile must be 11 digits')
                employee_form.focus_force()
                return False
            # EducationID validation
            selected_education = comb_education_id.get()
            # Get selected education ID from the combobox
            if selected_education:
                education_id = int(selected_education.split(" - ")[0])  # Extract ID from the selected value
            else:
                showinfo('Error', 'Please select the employee\'s education')
                return False

            # teacherCode validation
            employeeId_value = ent_employee_id.get()
            if not employeeId_value or not employeeId_value.isdigit():
                showinfo('Error', 'EmployeeID is required and must contain only digits')
                employee_form.focus_force()
                return False

            # MaritalStatus validation
            if not marital_status_string:
                showinfo('Error', 'Please select the employee\'s marital_status')
                employee_form.focus_force()
                return False

            # JobID validation
            selected_job = comb_job_id.get()
            # Get selected job ID from the combobox
            if selected_job:
                job_id = int(selected_job.split(" - ")[0])  # Extract ID from the selected value
            else:
                showinfo('Error', 'Please select the employee\'s job')
                return False

            # DepartmentID validation
            selected_department = comb_department_id.get()
            # Get selected department ID from the combobox
            if selected_department:
                department_id = int(selected_department.split(" - ")[0])  # Extract ID from the selected value
            else:
                showinfo('Error', 'Please select the employee\'s department')
                return False

            # InsuranceNumber validation
            insuranceNumber_value = ent_insurance_number.get()
            if not insuranceNumber_value or not insuranceNumber_value.isdigit():
                showinfo('Error', 'InsuranceNumber is required and must contain only digits')
                employee_form.focus_force()
                return False

            # AccountNumber validation
            account_number_value = ent_account_number.get()
            if not account_number_value or not account_number_value.isdigit()or len(account_number_value) != 16:
                showinfo('Error', 'AccountNumber must be 16 digits')
                employee_form.focus_force()
                return False

            # ManagerID handling (skip validation if no manager)
            selected_manager = comb_manager_id.get()
            manager_id = None  # Default to None

            if selected_manager and selected_manager != 'None':
                manager_id = int(selected_manager.split(" - ")[0])  # Extract ID if manager exists


            # Create a Employee object with updated data
            updated_employee = EmployeeUpdate(
                person_id=self.UpdateID,  # Use the stored UpdateID
                first_name=firstName,
                last_name=lastName,
                birthdate=ent_date_birthdate.get_date().strftime('%Y-%m-%d'),
                national_code=nationalCode,
                gender=gender_string,
                address=address_value,
                mobile=mobile_value,
                photo=photo_data, # Use either existing or new photo
                education_id=education_id,  # Use the selected education ID
                #education_id=int(comb_education_id.get()),
                employee_id=employeeId_value,
                marital_status= marital_status_string,
                job_id= job_id,
                department_id= department_id,
                hire_date = ent_date_hire_date.get_date().strftime('%Y-%m-%d'),  # Format date
                insurance_number= insuranceNumber_value,
                account_number= account_number_value,
                manager_id= manager_id)  # Can be None

            # Check if the updated employee is a boss
            if updated_employee.manager_id is None:
                # This is a boss-level employee
                showinfo('Info', 'You are updating a boss-level employee.')
            else:
                # This is a regular employee
                showinfo('Info', 'You are updating a regular employee.')


            # Call business logic to update the employee
            employeeBL = EmployeeBusinessLogic(employee_update=updated_employee)
            employeeBL.updateEmployee()
            showinfo("Success", "Employee updated successfully")
            employee_form.focus_force()  # Bring the form to focus
            for i in tree.get_children():
                tree.delete(i)
            employeeBL = EmployeeBusinessLogic()
            employeeBL.getEmployeeList(person_id=self.UpdateID)
            self.GetData = employeeBL.AllDataEmployee

            for item in self.GetData:
                tree.insert("", 'end', values=item)

            clearText()


        # Function to delete a selected employee
        # Function to delete a selected employee (admin only)
        def deleteEmployee():
            if not self.DeleteID:
                showerror("Error", "No employee selected for deletion")
                return
            # Confirm deletion
            if not msg.askyesno("Confirm", "Delete this employee?"):
                return
            deleted_employee = EmployeeIdDelete(person_id=self.DeleteID)
            employeeBL = EmployeeBusinessLogic(employee_delete=deleted_employee)
            employeeBL.deleteEmployee(deleted_employee)

            showinfo("Success", "Employee deleted successfully")
            populate_treeview()  # Refresh the tree
            clearText()

        # Function to select all employees and populate the tree view
        # Function to select all employees and populate the tree view (admin only)
        def selectAllEmployees():
            # Clear existing tree data
            for item in tree.get_children():
                tree.delete(item)

            # Fetch all employees from database
            employeeBL = EmployeeBusinessLogic()
            employeeBL.getAllEmployees()  # Fetch all employees
            self.GetData = employeeBL.AllDataEmployee

            # Insert all records into treeview
            for item in self.GetData:
                #print(f"Processing item: {item}")  # Debugging line
                photo_thumb = create_thumbnail_15x15(item[8]) if item[8] else None
                #print(f"Thumbnail created: {photo_thumb}")  # Debugging line
                tree.insert("", "end",
                            values=(item[0], item[1], item[2], item[3], item[4],
                                    item[5], item[6], item[7], "",
                                    item[9], item[10], item[11],item[12],item[13],item[14],item[15],item[16],item[17]),
                            image=photo_thumb if photo_thumb else "") # Use empty string if no image

        # Function to search for a employee by national code
        # Function to search for a employee by national code (admin only)
        def searchEmployee():
            national_code = txt_search_national_code.get().strip()

            # Validate input
            if not national_code:
                showinfo('Error', 'Please enter a NationalCode to search.')
                return
            # Validate national code
            if not national_code.isdigit() or len(national_code) != 10:
                showinfo('Error', 'NationalCode must be 10 digits.')
                return

            try:
                # Fetch employee data based on national code
                employee_business_logic = EmployeeBusinessLogic()
                employee_business_logic.getEmployeeListByNationalCode(national_code)

                self.GetData = employee_business_logic.AllDataEmployee

                if not self.GetData:
                    showinfo('Error', 'No employee found with this NationalCode.')
                    return

                # Clear existing tree data
                for item in tree.get_children():
                    tree.delete(item)

                # Populate the tree view with the fetched employee data
                for item in self.GetData:
                    photo_thumb = create_thumbnail_15x15(item[8]) if item[8] else None
                    tree.insert("", "end",
                                values=(item[0], item[1], item[2], item[3], item[4],
                                        item[5], item[6], item[7], "",
                                        item[9], item[10], item[11],item[12],item[13],item[14],item[15],item[16],item[17]),
                                image=photo_thumb)

            except Exception as e:
                showerror("Error", f"An error occurred during search: {str(e)}")


        # Function to generate a employee identification card
        def generate_employee_card():
            # Check if user is admin and has a selection
            if userparam.IsAdmin:
                selected_item = tree.focus()
                if not selected_item:
                    msg.showinfo("Error", "Please select a employee from the list.")
                    return

                # Get employee data from the selected item
                record = tree.item(selected_item)['values']

            else:
                # For non-admin, use current form data (assuming it's filled for the newly registered employee)
                first_name = ent_first_name.get()
                last_name = ent_last_name.get()
                birthdate = ent_date_birthdate.get_date().strftime('%d/%m/%Y') if ent_date_birthdate.get_date() else ""
                national_code = ent_national_code.get()
                gender = "Male" if txt_gender.get() == "1" else "Female" if txt_gender.get() == "2" else ""
                mobile = ent_mobile.get()
                employee_id = ent_employee_id.get()
                photo_data = self.uploaded_photo  # Use uploaded photo
                if not all([first_name, last_name, birthdate, national_code, gender, mobile, employee_id, photo_data]):
                    msg.showinfo("Error", "Please fill in all required fields and upload a photo to generate the card.")
                    return
                record = [None, first_name, last_name, birthdate, national_code, gender, None, mobile, photo_data, None,
                          employee_id, None]


            # Create a new Toplevel window for the employee card
            card_window = Toplevel()
            card_window.title("Employee Identification Card") # Set the title of the card window
            card_window.geometry("600x475")  # Set the size of the card window
            card_window.resizable(False, False) # Disable resizing of the card window

            # Style the card window
            card_window.configure(bg='#f0f0f0')


            first_name = record[1]
            last_name = record[2]
            birthdate = record[3]
            national_code = record[4]
            gender = record[5]
            mobile = record[7]
            photo_data = record[8]  # Photo binary data
            employee_id = record[10]



            # Main card frame to hold all elements
            card_frame = Frame(card_window, bg='white', bd=2, relief='groove', padx=20, pady=20)
            card_frame.pack(pady=20, padx=20)

            # Card header
            header_frame = Frame(card_frame, bg='#1E90FF')
            header_frame.pack(fill='x', pady=(0, 20))
            # Title label for the card
            lbl_title = Label(header_frame,
                              text="EMPLOYEE IDENTIFICATION CARD",
                              font=('Arial', 16, 'bold'),
                              bg='#1E90FF',
                              fg='white')
            lbl_title.pack(pady=10)

            # Card content frame
            content_frame = Frame(card_frame)
            content_frame.pack(fill='both', expand=True)
            # Photo frame (left side of the card)
            photo_frame = Frame(content_frame)
            photo_frame.pack(side='left', padx=20)  # Pack to the left with padding
            # Display the uploaded photo if available
            if self.uploaded_photo:
                try:
                    pil_img = self.uploaded_photo.resize((100, 100), Image.LANCZOS)  # Resize photo to fit
                    photo_img = ImageTk.PhotoImage(pil_img)  # Convert to PhotoImage for display
                    lbl_photo = Label(photo_frame, image=photo_img, bd=1, relief='solid') # Create label for photo
                    lbl_photo.image = photo_img  # Keep reference to avoid garbage collection
                    lbl_photo.pack()  # Pack the photo label

                    # Add "Valid until" date below the photo
                    valid_date = datetime.now().replace(year=datetime.now().year + 2)  # Valid for 2 years
                    lbl_valid = Label(photo_frame,
                                      text=f"Valid until: {valid_date.strftime('%d/%m/%Y')}",
                                      font=('Arial', 8))  # Smaller font for validity date
                    lbl_valid.pack(pady=(10, 0))  # Add padding
                except Exception as e:
                    print(f"Error displaying photo: {e}")  # Log error if photo display fails
                    lbl_photo = Label(photo_frame, text="No photo available", width=20, height=10) # Placeholder
                    lbl_photo.pack()
            else:
                lbl_photo = Label(photo_frame, text="No photo available", width=20, height=10) # Placeholder if no photo
                lbl_photo.pack()
            # Information frame (right side of the card)
            info_frame = Frame(content_frame)
            info_frame.pack(side='left', fill='both', expand=True)

            ### Employee information labels
            # School name label
            lbl_school = Label(info_frame,
                                   text="SEMATEC INSTITUTE",
                               font=('Arial', 14, 'bold'),
                               anchor='w')
            lbl_school.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky='w')

            # Function to create a row of employee information
            def create_info_row(parent, row, label, value):
                lbl = Label(parent, text=label, font=('Arial', 10, 'bold'), anchor='w') # Label for the field
                lbl.grid(row=row, column=0, sticky='w', pady=2)
                val = Label(parent, text=value, font=('Arial', 10), anchor='w') # Label for the value
                val.grid(row=row, column=1, sticky='w', pady=2, padx=(10, 0))

            # Add employee information to the card
            create_info_row(info_frame, 1, "Employee ID:", employee_id)
            create_info_row(info_frame, 2, "Full Name:", f"{first_name} {last_name}")
            create_info_row(info_frame, 3, "Date of Birth:", birthdate)
            create_info_row(info_frame, 4, "National Code:", national_code)
            create_info_row(info_frame, 5, "Gender:", gender)
            create_info_row(info_frame, 8, "Contact:", mobile)


            # Footer with employee signature
            footer_frame = Frame(card_frame)
            footer_frame.pack(fill='x', pady=(20, 0)) # Fill horizontally with padding
            # Signature label
            lbl_signature = Label(footer_frame, text="SEMATEC INSTITUTE:No. 1,Corner of Fourth Alley,West Shahid Ghandi Street,North Sohrevardi,Tehran", font=('Arial', 8))
            lbl_signature.pack(anchor='w')

            # Placeholder for signature line
            signature_line = Canvas(footer_frame, width=200, height=2, bg='black')
            signature_line.pack(anchor='w', pady=(0, 10))

            # Button frame at the bottom of the card
            btn_frame = Frame(card_window)
            btn_frame.pack(pady=(10, 0))

            # Function to save the employee card as an image
            def save_employee_card():
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                    initialfile=f"employee_card_{employee_id}"
                )
                if file_path:
                    try:
                        # Create the card image to save
                        card_img = Image.new('RGB', (550, 450), 'white') # Create a new white image
                        draw = ImageDraw.Draw(card_img) # Create a drawing context

                        #photo_data
                        # Draw all elements on the card
                        if self.uploaded_photo:
                            teacher_photo = self.uploaded_photo.resize((150, 150), Image.LANCZOS) # resize photo for card
                            card_img.paste(teacher_photo, (50, 115))  # paste photo onto card

                        # Draw blue header
                        draw.rectangle([(0, 0), (550, 80)], fill='#1E90FF') # Blue rectangle for header

                        # Draw text on the card
                        font = ImageFont.truetype("arial.ttf", 23) # Load font for title
                        draw.text((100, 25), "EMPLOYEE IDENTIFICATION CARD", font=font, fill='black')
                        font = ImageFont.truetype("arial.ttf", 18) # Load font for school name
                        draw.text((220, 90), "SEMATEC INSTITUTE", font=font, fill='black')

                        font = ImageFont.truetype("arial.ttf", 14) # Load font for student info
                        info_y = 130  # Starting Y position for info
                        draw.text((220, info_y), f"Employee ID: {employee_id}", font=font, fill='black')
                        draw.text((220, info_y + 30), f"Full Name: {first_name} {last_name}", font=font, fill='black')
                        draw.text((220, info_y + 60), f"Date of Birth: {birthdate}", font=font, fill='black')
                        draw.text((220, info_y + 90), f"National Code: {national_code}", font=font, fill='black')
                        draw.text((220, info_y + 120), f"Gender: {gender}", font=font, fill='black')
                        draw.text((220, info_y + 150), f"Contact: {mobile}", font=font, fill='black')

                        # Add footer
                        card_width = 550
                        card_height= 450

                        footer_text_line1 = "SEMATEC INSTITUTE: No. 1, Corner of Fourth Alley,"
                        footer_text_line2 = "West Shahid Ghandi Street, North Sohrevardi, Tehran"
                        footer_y = card_height - 50  # Adjusted for two lines
                        # Draw footer rectangle
                        draw.rectangle([(0, footer_y - 10), (card_width, card_height)], fill='#1E90FF',
                                       outline='#1E90FF')
                        draw.text((card_width // 2 , footer_y + 5), footer_text_line1, font=font, fill='white',
                                  anchor='mm')
                        draw.text((card_width // 2 , footer_y + 25), footer_text_line2, font=font, fill='white',
                                  anchor='mm')
                        # # Add validity date
                        valid_date = (datetime.now() + timedelta(days=365 * 2)).strftime("%d/%m/%Y") # Validity date
                        draw.text((card_width - 150, footer_y - 25), f"Valid until: {valid_date}", font=font,
                                  fill='black')
                        # Add signature line
                        info_x = 115
                        draw.line([(info_x, footer_y - 30), (info_x + 200, footer_y - 30)], fill='black', width=2) # signature line
                        draw.text((info_x + 100, footer_y - 15), "Authorized Signature", font=font, fill='black',
                                  anchor='mm')

                        # save the card Image
                        card_img.save(file_path) # Save the image to the specified file path
                        msg.showinfo("Success", f"employee card saved as:\n{file_path}")
                    except Exception as e:
                        msg.showerror("Error", f"Failed to save card: {str(e)}")

            # Buttons for saving and closing the card window
            btn_save = ttk.Button(btn_frame, text="Save Card", command=save_employee_card)
            btn_save.pack(side='left', padx=5)
            btn_close = ttk.Button(btn_frame, text="Close", command=card_window.destroy)
            btn_close.pack(side='left', padx=5)
            # Auto-refresh the card window
            card_window.update()




        # frame
        frame = ctk.CTkFrame(employee_form, width = 880,height= 770)
        frame_button = ctk.CTkFrame(employee_form,width = 880 , height= 20)
        frame_grid = ctk.CTkFrame(employee_form,width= 880,height=10)

        frame.grid(row=0, column=0, padx=10, sticky='nsew')
        frame_button.grid(row=1, column=0, padx=10, sticky='nsew')
        frame_grid.grid(row=2, column=0, sticky='nsew', padx=10)
        # Photo section - top left
        photo_container = ctk.CTkFrame(frame)
        photo_container.grid(row=0, column=0, padx=10, pady=5, sticky="nw")

        # Photo frame with border (using CTkFrame with border)
        photo_frame = ctk.CTkFrame(photo_container, width=105, height=105, border_width=3,
                                   border_color='green')
        photo_frame.pack_propagate(0)  # Prevent the frame from resizing to fit the contents
        photo_frame.pack(side='left')  # Pack the photo_frame into the photo_container
        # Create a label to display the photo
        photo_label = ctk.CTkLabel(photo_frame, text='', width=100, height=100)
        photo_label.pack(side='left')
        # Update the button to call the upload_photo function
        btn_UploadPhoto = ctk.CTkButton(frame, text='Upload Photo', command=upload_photo)
        btn_UploadPhoto.grid(row=0, column=1, padx=10, pady=40, sticky='nw')
        # new section - top Right
        new_section = ctk.CTkFrame(frame)
        new_section.grid(row=0, column=2, padx=10, pady=5, sticky="nw")

        new_section.grid_rowconfigure(0, minsize=30)
        new_section.grid_rowconfigure(1, minsize=30)
        new_section.grid_rowconfigure(2, minsize=30)
        new_section.grid_rowconfigure(3, minsize=30)

        # Register validation functions
        vcmd_national_code = (employee_form.register(validate_national_code), '%P')
        vcmd_mobile = (employee_form.register(validate_mobile), '%P')
        vcmd_insurance_number = (employee_form.register(validate_insurance_number), '%P')
        vcmd_account_number = (employee_form.register(validate_account_number), '%P')
        vcmd_20 = (employee_form.register(validate20), '%P')
        vcmd_30 = (employee_form.register(validate30), '%P')
        vcmd_40 = (employee_form.register(validate40), '%P')


        # Label : FirstName
        lbl_first_name = ctk.CTkLabel(frame, text='FirstName: ')
        lbl_first_name.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        # Entry : FirstName
        ent_first_name = ctk.CTkEntry(frame, width=200, placeholder_text="Enter first name")
        ent_first_name.configure(validate="key", validatecommand = vcmd_20 )
        ent_first_name.grid(row=1, column=1, padx=10, pady=5, sticky='e')

        # Label : LastName
        lbl_last_name = ctk.CTkLabel(frame, text='LastName: ')
        lbl_last_name.grid(row=1, column=2, padx=40, pady=5, sticky='w')
        # Entry : LastName
        ent_last_name = ctk.CTkEntry(frame, width=200, placeholder_text="Enter last name")
        ent_last_name.configure(validate="key", validatecommand=vcmd_30)
        ent_last_name.grid(row=1, column=2, padx=120, pady=5, sticky='ne')
        # Birthdate
        lbl_birthdate = ctk.CTkLabel(frame, text='Birthdate: (dd/mm/yyyy) ')
        lbl_birthdate.grid(row=2, column=0, padx=10, pady=5, sticky='w')
        # Entry : Birthdate
        date_frame = ctk.CTkFrame(frame)
        date_frame.grid(row=2, column=1, padx=10, pady=5, sticky='e')
        ent_date_birthdate = DateEntry(date_frame, width=26,
                                       date_pattern='dd/mm/yyyy')  # Keep DateEntry as is, since tkcalendar doesn't have a direct CTk equivalent
        ent_date_birthdate.pack()
        #
        # Label : NationalCode
        lbl_national_code = ctk.CTkLabel(frame, text='NationalCode: ')
        lbl_national_code.grid(row=2, column=2, padx=40, pady=5, sticky='w')

        # Entry : NationalCode
        ent_national_code = ctk.CTkEntry(frame, width=200, placeholder_text="Enter 10-digit code")
        ent_national_code.configure(validate="key",
                                    validatecommand= vcmd_national_code)
        ent_national_code.grid(row=2, column=2, padx=120, pady=5, sticky='ne')
        # Label : Gender
        lbl_gender = ctk.CTkLabel(frame, text='Gender: ')
        lbl_gender.grid(row=3, column=0, padx=10, pady=5, sticky='w')
        # Radiobutton : Gender
        txt_gender = ctk.StringVar()
        # gender: male
        rb_gender_male = ctk.CTkRadioButton(frame, text='Male', variable=txt_gender, value=1)
        rb_gender_male.grid(row=3, column=1, padx=10, pady=5, sticky='w')
        # gender : female
        rb_gender_female = ctk.CTkRadioButton(frame, text='Female', variable=txt_gender, value=2)
        rb_gender_female.grid(row=3, column=1, padx=10, pady=5, sticky='e')
        #
        # Label : Address
        lbl_address = ctk.CTkLabel(frame, text='Address: ')
        lbl_address.grid(row=3, column=2, padx=40, pady=5, sticky='w')
        # Entry : Address

        ent_address = ctk.CTkEntry(frame, width=200, placeholder_text="Enter address")
        ent_address.configure(validate="key", validatecommand=vcmd_40)
        ent_address.grid(row=3, column=2, padx=120, pady=5, sticky='ne')
        # Label : Mobile
        lbl_mobile = ctk.CTkLabel(frame, text='Mobile: ')
        lbl_mobile.grid(row=4, column=0, padx=10, pady=5, sticky='w')
        # Entry : Mobile

        ent_mobile = ctk.CTkEntry(frame, width=200, placeholder_text="Enter mobile")
        ent_mobile.configure(validate="key", validatecommand=vcmd_mobile)
        ent_mobile.grid(row=4, column=1, padx=10, pady=5, sticky='e')

        # Label : Education
        lbl_education_id = ctk.CTkLabel(frame, text='EducationID: ')
        lbl_education_id.grid(row=4, column=2, padx=40, pady=5, sticky='w')
        comb_education_id = ctk.CTkComboBox(frame, width=200)
        comb_education_id.grid(row=4, column=2, padx=120, pady=5, sticky='ne')
        # Fetch education levels and populate the combobox
        education_levels = self.fetchEducationLevels()
        comb_education_id.configure(values=[f"{level[0]} - {level[1]}" for level in
                                            education_levels])# Assuming level[0] is ID and level[1] is Name
        comb_education_id.set("Select EducationID")
        # Label : EmployeeID
        lbl_employee_id = ctk.CTkLabel(frame, text='EmployeeID')
        lbl_employee_id.grid(row=5, column=0, padx=10, pady=5, sticky='w')
        # Entry : EmployeeID
        ent_employee_id = ctk.CTkEntry(frame, placeholder_text="Enter Employee ID", width=200)
        ent_employee_id.grid(row=5, column=1, padx=10, pady=5, sticky='e')

        # Label : MaritalStatus
        lbl_marital_status = ctk.CTkLabel(frame, text='MaritalStatus: ')
        lbl_marital_status.grid(row=5, column=2, padx=40, pady=5, sticky='w')
        # Radiobutton : MaritalStatus (using CustomTkinter radiogroup)
        txt_marital_status = ctk.StringVar()
        rb_gender_married = ctk.CTkRadioButton(frame, text='Married', variable=txt_marital_status, value=1)
        rb_gender_married.grid(row=5, column=2, padx=230, pady=5, sticky='w')
        rb_gender_single = ctk.CTkRadioButton(frame, text='Single', variable=txt_marital_status, value=2)
        rb_gender_single.grid(row=5, column=2, padx=110, pady=5, sticky='e')
        # Label : Job
        lbl_job_id = ctk.CTkLabel(frame, text='JobID: ')
        lbl_job_id.grid(row=6, column=0, padx=10, pady=5, sticky='w')
        comb_job_id = ctk.CTkComboBox(frame, width=200)
        comb_job_id.grid(row=6, column=1, padx=10, pady=5, sticky='e')
        # Fetch job levels and populate the combobox
        job_levels = self.fetchJobLevels()
        comb_job_id.configure(
            values=[f"{level[0]} - {level[1]}" for level in job_levels])  # Assuming level[0] is ID and level[1] is Name
        comb_job_id.set("Select JobID")

        # Label : DepartmentID
        lbl_department_id = ctk.CTkLabel(frame, text='DepartmentID: ')
        lbl_department_id.grid(row=6, column=2, padx=40, pady=5, sticky='w')
        comb_department_id = ctk.CTkComboBox(frame, width=200)
        comb_department_id.grid(row=6, column=2, padx=120, pady=5, sticky='ne')

        # Fetch department levels and populate the combobox
        department_levels = self.fetchDepartmentLevels()
        comb_department_id.configure(values=[f"{level[0]} - {level[1]}" for level in
                                             department_levels])  # Assuming level[0] is ID and level[1] is Name
        comb_department_id.set("Select DepartmentID")

        # HireDate
        lbl_hire_date = ctk.CTkLabel(new_section, text='HireDate: (dd/mm/yyyy) ')
        lbl_hire_date.grid(row=0, column=2, padx=30, pady=5, sticky='w')
        # Entry : HireDate
        ent_date_hire_date = DateEntry(new_section, width=27,
                                       date_pattern='dd/mm/yyyy')  # Keep DateEntry
        ent_date_hire_date.grid(row=0, column=3, padx=22, pady=5, sticky='e')
        # Label : InsuranceNumber
        lbl_insurance_number = ctk.CTkLabel(new_section, text='InsuranceNumber')
        lbl_insurance_number.grid(row=1, column=2, padx=30, pady=5, sticky='w')
        # Entry : InsuranceNumber
        ent_insurance_number = ctk.CTkEntry(new_section, placeholder_text="Enter insurance number", width=200)

        ent_insurance_number.configure(validate="key",
                                       validatecommand=vcmd_insurance_number)
        ent_insurance_number.grid(row=1, column=3, padx=30, pady=5, sticky='w')
        #

        # Label : AccountNumber
        lbl_account_number = ctk.CTkLabel(new_section, text='AccountNumber: ')
        lbl_account_number.grid(row=2, column=2, padx=30, pady=5, sticky='w')
        # Entry : AccountNumber

        ent_account_number = ctk.CTkEntry(new_section, width=200, placeholder_text="Enter account number")
        ent_account_number.configure(validate="key",
                                     validatecommand=vcmd_account_number)
        ent_account_number.grid(row=2, column=3, padx=30, pady=5, sticky='w')
        # Label : ManagerID
        lbl_manager_id = ctk.CTkLabel(new_section, text='ManagerID: ')
        lbl_manager_id.grid(row=3, column=2, padx=30, pady=5, sticky='w')
        comb_manager_id = ctk.CTkComboBox(new_section, width=200)
        comb_manager_id.grid(row=3, column=3, padx=30, pady=5, sticky='w')

        # In the employee_form_load method, populate the combobox
        # Fetch managers and add "No Manager" option
        managers = self.fetchManagerLevels()
        comb_manager_id.configure(values=["None - No Manager"] + [f"{emp[0]} - {emp[1]} {emp[2]}" for emp in
                                                                  managers])  # Assuming emp[0] is ID, emp[1] is FirstName, emp[2] is LastName
        comb_manager_id.set("Select ManagerID")


        # frameButton : clearEmployee
        btn_clear_employee = ctk.CTkButton(frame_button, text='Clear', command=clearText, width=150)
        btn_clear_employee.grid(row=7, column=0, padx=10, pady=3, sticky='w')
        btn_select_all = ctk.CTkButton(frame_button, text='Select All', command=selectAllEmployees, width=150)
        btn_select_all.grid(row=7, column=1, padx=10, pady=3, sticky='w')
        # frameButton : insertEmployee
        btn_insert_employee = ctk.CTkButton(frame_button, text='Insert', command=registerEmployee, width=150)
        btn_insert_employee.grid(row=7, column=2, padx=10, pady=3, sticky='e')
        # frameButton : updateEmployee
        btn_update_employee = ctk.CTkButton(frame_button, text='Update', command=updateEmployee, width=150)
        btn_update_employee.grid(row=7, column=3, padx=10, pady=3, sticky='w')
        # frameButton : deleteEmployee
        btn_delete_employee = ctk.CTkButton(frame_button, text='Delete', command=deleteEmployee, width=150)
        btn_delete_employee.grid(row=7, column=4, padx=10, pady=3, sticky='w')
        # frameButton : closeEmployee
        btn_backToMain_employee = ctk.CTkButton(frame_button, text='BackToMain', command=destroyForm, width=150)
        btn_backToMain_employee.grid(row=8, column=4, padx=10, pady=3, sticky='w')
        #
        # Label: Search by National Code
        lbl_search_national_code = ctk.CTkLabel(frame_button, text='Search By NationalCode: ')
        lbl_search_national_code.grid(row=8, column=0, padx=10, pady=3, sticky='w')
        # Entry: Search National Code
        txt_search_national_code = ctk.StringVar()
        ent_search_national_code = ctk.CTkEntry(frame_button, width=150, textvariable=txt_search_national_code)
        ent_search_national_code.grid(row=8, column=1, padx=10, pady=3, sticky='e')
        # Button: Search
        btn_search_employee = ctk.CTkButton(frame_button, text='Search', command=searchEmployee, width=150)
        btn_search_employee.grid(row=8, column=2, padx=10, pady=3, sticky='e')
        # Add the Generate Employee Card button
        btn_generate_card = ctk.CTkButton(frame_button, text='Generate Employee Card', command=generate_employee_card,
                                          width=150)
        btn_generate_card.grid(row=8, column=3, padx=10, pady=3, sticky='w')

        btn_export_excel = ctk.CTkButton(frame_button, text='Export to Excel', command=export_to_excel, width=150)
        btn_export_excel.grid(row=9, column=0, padx=10, pady=3, sticky='w')

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
        columns = ('person_id','first_name','last_name','birthdate','national_code','gender','address','mobile','photo','education_id','employee_id','marital_status',
                   'job_id','department_id','hire_date','insurance_number','account_number','manager_id')
        tree = ttk.Treeview(frame_grid, columns = columns , show = 'headings')
        # Set up headings for the Treeview
        tree.heading('person_id', text='PersonID', anchor='w')
        tree.heading('first_name',text='FirstName',anchor='w')
        tree.heading('last_name', text='LastName', anchor='w')
        tree.heading('birthdate', text='BirthDate', anchor='w')
        tree.heading('national_code', text='NationalCode', anchor='w')
        tree.heading('gender', text='Gender', anchor='w')
        tree.heading('address', text='Address', anchor='w')
        tree.heading('mobile', text='Mobile', anchor='w')
        tree.heading('photo', text='Photo', anchor='w')
        tree.heading('education_id', text='EducationID', anchor='w')
        tree.heading('employee_id', text='EmployeeID', anchor='w')
        tree.heading('marital_status', text='MaritalStatus', anchor='w')
        tree.heading('job_id', text='JobID', anchor='w')
        tree.heading('department_id', text='DepartmentID', anchor='w')
        tree.heading('hire_date', text='HireDate', anchor='w')
        tree.heading('insurance_number', text='InsuranceNumber', anchor='w')
        tree.heading('account_number', text='AccountNumber', anchor='w')
        tree.heading('manager_id', text='ManagerID', anchor='w')

        # Set the width of each column
        column_width = 150  # Set a common width for all columns
        for col in columns:
            tree.column(col, width=column_width)  # Set the width for each column


        # Image handling functions (updated for 15x15)
        def create_thumbnail_15x15(photo_data):
            """Create a 15x15 thumbnail from binary photo data"""
            if not photo_data:
                return None
            try:
                pil_img = Image.open(io.BytesIO(photo_data))
                pil_img = pil_img.resize((15, 15), Image.LANCZOS)  # Resize to exact dimensions
                return ImageTk.PhotoImage(pil_img)
            except Exception as e:
                print(f"Error creating thumbnail: {e}")
                return None

        # Configure Treeview for small images
        style = ttk.Style()
        style.configure("Treeview", rowheight=20)  # Set row height to 24 pixels
        #
        # Populate the Treeview
        def populate_treeview():
            tree.delete(*tree.get_children())
            employeeBusinessLogic = EmployeeBusinessLogic()
            employeeBusinessLogic.getEmployeeList(userparam.IsAdmin) # PersonID
            self.GetData = employeeBusinessLogic.AllDataEmployee

            for item in self.GetData:
                photo_thumb = create_thumbnail_15x15(item[8])
                if photo_thumb:
                    self.photo_cache[item[0]] = photo_thumb
                    tree.insert("", "end",
                                values=(item[0], item[1], item[2], item[3], item[4],
                                        item[5], item[6], item[7], "",
                                        item[9], item[10], item[11],item[12],item[13],item[14],
                                        item[15],item[16],item[17]),
                                image=photo_thumb)
                else:
                    tree.insert("", "end",
                                values=(item[0], item[1], item[2], item[3], item[4],
                                        item[5], item[6], item[7], "No Photo",
                                        item[9], item[10], item[11],item[12],item[13],item[14],
                                        item[15].item[16],item[17]))




        def item_selected(event):
            # Get the selected item from the tree
            selected_item = tree.focus()
            if not selected_item:  # If nothing is selected, exit
                return

            item = tree.item( selected_item)
            record = item['values']

            # Store the current photo data
            self.current_photo_data = next((x[8] for x in self.GetData if x[0] == record[0]), None)

            # Populate the fields with the selected record
            ent_first_name.delete(0, END)
            ent_first_name.insert(0, record[1])
            ent_last_name.delete(0, END)
            ent_last_name.insert(0, record[2])
            # Handle the date conversion
            try:
                # Check if record[3] is a string or a date object
                if isinstance(record[3], str):
                    birthdate = datetime.strptime(record[3], '%Y-%m-%d').date()  # Convert to date object
                else:
                    birthdate = record[3]  # Assume it's already a date object
                ent_date_birthdate.set_date(birthdate)  # Set the date in the DateEntry
            except ValueError as e:
                print(f"Error converting date: {e}")
                ent_date_birthdate.set_date('')  # Clear the date entry if there's an error
            # ent_date_birthdate.set_date(record[3])  # Assuming record[3] is a date object
            ent_national_code.delete(0, END)
            ent_national_code.insert(0, record[4])
            # Set the gender radio button
            if record[5] == "Male":  # Check if the gender is "Male"
                txt_gender.set(1) # Set to 1 for Male
            elif record[5] == "Female":  # Check if the gender is "Female"
                txt_gender.set(2)  # Set to 2 for Female
            else:
                txt_gender.set(0)  # Clear selection if gender is not recognized
            ent_address.delete(0, END)
            ent_address.insert(0, record[6])
            ent_mobile.delete(0,END)
            ent_mobile.insert(0, record[7])
            comb_education_id.set(record[9])  # Set the selected value for the combobox

            # # Set the education name in the appropriate section
            # education_name = record[12] # Assuming the education name is at index 12
            # comb_education_id.set(education_name) # Set the selected value for the combobox

            ent_employee_id.delete(0, END)
            ent_employee_id.insert(0, record[10])
            # Set the maritalStatus radio button
            if record[11] == "M":  # Check if the maritalStatus is "Married"
                txt_marital_status.set(1) # Set to 1 for Married
            elif record[11] == "S":  # Check if the maritalStatus is "Single"
                txt_marital_status.set(2)  # Set to 2 for Single
            else:
                txt_marital_status.set(0)  # Clear selection if maritalStatus is not recognized

            comb_job_id.set(record[12])  # Set the selected value for the combobox
            comb_department_id.set(record[13])  # Set the selected value for the combobox


            # Handle the date conversion
            try:
                # Check if record[14] is a string or a date object
                if isinstance(record[14], str):
                    hire_date = datetime.strptime(record[14], '%Y-%m-%d').date()  # Convert to date object
                else:
                    hire_date = record[14]  # Assume it's already a date object
                ent_date_hire_date.set_date(hire_date)  # Set the date in the DateEntry
            except ValueError as e:
                print(f"Error converting date: {e}")
                ent_date_hire_date.set_date('')  # Clear the date entry if there's an error

            ent_insurance_number.delete(0, END)
            ent_insurance_number.insert(0, record[15])
            ent_account_number.delete(0,END)
            ent_account_number.insert(0, record[16])

            comb_manager_id.set(record[17])  # Set the selected value for the combobox



            # ========== PHOTO HANDLING SECTION ==========
            # Handle photo display
            photo_data = next((x[8] for x in self.GetData if x[0] == record[0]), None)

            # Clear current photo
            (photo_label.configure(image=None))
            photo_label.image = None

            # Display new photo if exists
            if photo_data:
                try:
                    pil_img = Image.open(io.BytesIO(photo_data))
                    pil_img = pil_img.resize((100, 100), Image.LANCZOS)
                    tk_img = CTkImage(pil_img, size=(100, 100))

                    photo_label.configure(image=tk_img)
                    photo_label.image = tk_img  # Keep reference
                except Exception as e:
                    print(f"Error displaying photo: {e}")
            # Store IDs for operations
            self.DeleteID = record[0]
            self.UpdateID = record[0]

        # Bind selection event
        tree.bind('<<TreeviewSelect>>', item_selected)

        # Initial population
        populate_treeview()


        #
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
        employee_form.columnconfigure(0, weight=1)
        employee_form.rowconfigure(0, weight=1)
        frame_grid.columnconfigure(0, weight=3)
        frame_grid.columnconfigure(1, weight=3)
        frame_grid.columnconfigure(2, weight=3)
        frame_grid.columnconfigure(3, weight=1)
        frame_grid.columnconfigure(4, weight=1)
        frame_grid.rowconfigure(1, weight=1)

        # Access control for non-admin users
        if not userparam.IsAdmin:
            # Disable admin-only buttons
            btn_update_employee.configure(state='disabled')
            btn_delete_employee.configure(state='disabled')
            btn_select_all.configure(state='disabled')
            btn_search_employee.configure(state='disabled')
            btn_export_excel.configure(state='disabled')
            # btn_generate_card.configure(state= 'disabled')

            # Hide search-related widgets
            lbl_search_national_code.grid_forget()
            ent_search_national_code.grid_forget()

            # Optionally hide the data grid (treeview) to avoid showing an empty table
            frame_grid.grid_forget()

            # Note: btn_clear_employee, btn_insert_employee,btn_generate_card and btn_backToMain_employee remain enabled




        employee_form.mainloop()


