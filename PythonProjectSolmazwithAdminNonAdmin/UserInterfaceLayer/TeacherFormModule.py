# Import necessary libraries for GUI, image handling, and date management
import customtkinter as ctk  # Changed from tkinter

from customtkinter import CTkImage

import tkinter
import io
from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo, showerror
from tkinter import Toplevel  # Import Toplevel
from customtkinter import CTkToplevel
from PIL import Image, ImageTk,ImageDraw, ImageFont
from datetime import datetime, timedelta
from tkcalendar.dateentry import DateEntry
from openpyxl import Workbook  # Added for Excel export


from BusinessLogicLayer.TeacherBusinessLogic import TeacherBusinessLogic
from Model.UserModule import UserModel
from Model.TeacherModel import Teacher,TeacherUpdate,TeacherIdDelete

# Set CustomTkinter appearance (add this for modern look)
ctk.set_appearance_mode("Dark")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue", "green", "dark-blue"



class TeacherFormClass:
    # Initialize the StudentFormClass with user and main form references
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
        self.student_photos = {}  # Dictionary to hold student photos
        self.photo_cache = {}  # For storing loaded images
        self.uploaded_photo = None  # Initialize uploaded_photo attribute
        self.current_photo_data = None


    # Fetch education levels from the business logic layer
    def fetchEducationLevels(self):
        teacher_business_logic = TeacherBusinessLogic()
        education_levels = teacher_business_logic.getEducationList()  # Fetch education levels
        return education_levels


    # #
    # Fetch certificate levels from the business logic layer
    def fetchCertificateLevels(self):
        teacher_business_logic = TeacherBusinessLogic()
        certificate_levels = teacher_business_logic.getCertificateList()  # Fetch certificate levels
        return certificate_levels



    # Load the student form
    def teacher_form_load(self,userparam : UserModel):
        #teacher_form =Tk()
        teacher_form = ctk.CTkToplevel()  # Use Toplevel instead of Tk for a new window
        teacher_form.title('TeacherForm...')
        teacher_form.resizable(0, 0)
        if userparam.IsAdmin:
            teacher_form.geometry('900x735')   # Set the window size
        else:
            teacher_form.geometry('900x520')  # Set the window size

        # teacher_form.geometry('930x745')
        x = int(teacher_form.winfo_screenwidth() / 2 - 900 / 2)
        y = int(teacher_form.winfo_screenheight() / 2 - 735 / 2)
        teacher_form.geometry('+{}+{}'.format(x, y))
        teacher_form.iconbitmap('images/ImagesTeacherForm/Teacher.ico')

        # Function to upload a photo
        def upload_photo():
            try:
                f_types = [('Jpg Files', '*.jpg'), ('All Files', '*.*')]
                filename = filedialog.askopenfilename(filetypes=f_types)
                if filename:
                    # Load the image
                    pil_img = Image.open(filename)
                    pil_img = pil_img.resize((100, 100), Image.LANCZOS)  # Resize image to fit in the label
                    image = CTkImage(pil_img, size=(100, 100))

                    # Display the image in the label
                    photo_label.configure(image=image)
                    photo_label.image = image  # Keep a reference to avoid garbage collection

                    # Store the image data in an instance variable
                    self.uploaded_photo = pil_img  # Store the PIL image for later use
            except Exception as e:
                msg.showerror("Error", f"An error occurred while uploading the photo: {e}")

        # Function to close the teacher form and show the main form
        def destroyForm():
            teacher_form.withdraw()  # Close the teacher form
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
            ent_national_code.delete(0, END)   # Clear the national code
            txt_gender.set('')  # Reset gender selection
            ent_address.delete(0,END)
            ent_mobile.delete(0, END)  # Clear the mobile number
            photo_label.configure(image=None)  # Clear the image
            photo_label.image = None  # Clear the reference to avoid garbage collection
            comb_education_id.set('')  # Clear the combobox
            ent_teacher_code.delete(0,END)
            # Reset marital_status selection
            txt_marital_status.set('')  # or set to a default value if needed
            ent_date_start_date.set_date(datetime.now().date())  # Set to current date
            ent_insurance_number.delete(0,END)
            ent_account_number.delete(0,END)# Clear the account_number
            comb_certificate_id.set('')
            ent_date_expiration_date.set_date(datetime.now().date())
            ent_res_id.delete(0,END)


        # Validation functions for input fields
        def validate_national_code(value):
            if value == "":
                return True # Allow empty input
            return value.isdigit() and  len(value) <= 10   # Allow only digits and up to 10 digits
        def validate_mobile(value):
            if value == "":
                return True # Allow empty input
            return value.isdigit() and len(value) <= 11  # Allow only digits and up to 11 digits

        def validate_insurance_number(value):
            if value == "":
                return True  # Allow empty input if it's optional
            return value.isdigit() and len(value) <= 16  # Adjust length as needed

        def validate_account_number(value):
            if value == "":
                return True # Allow empty input
            return value.isdigit() and len(value) <= 16  # Allow only digits and up to 16 digits

        def validate_res_id(value):
            return len(value) <= 50

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
                ws.title = "Teachers"

                # Define headers (excluding 'photo' as it's binary; we'll add a 'Photo Exists?' column)
                headers = ['PersonID', 'FirstName', 'LastName', 'BirthDate', 'NationalCode', 'Gender', 'Address',
                           'Mobile', 'Photo Exists?', 'EducationID', 'TeacherCode', 'MaritalStatus', 'StartDate',
                           'InsuranceNumber', 'AccountNumber', 'CertificateID', 'ExpirationDate', 'ResID']
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
        def registerTeacher():
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
                showinfo('Error', 'Please upload a photo of the teacher.')
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
                teacher_form.focus_force()
                return False
            # LastName validation
            if not lastName or not lastName.isalpha():
                showinfo('Error', 'LastName is required and must contain only letters')
                teacher_form.focus_force()
                return False
            # NationalCode validation
            if not nationalCode or not nationalCode.isdigit() or len(nationalCode) != 10:
                showinfo('Error', 'NationalCode must be 10 digits')
                teacher_form.focus_force()
                return False
            # Gender validation
            if not gender_string:
                showinfo('Error', 'Please select the teacher\'s gender')
                teacher_form.focus_force()
                return False

            # Address validation
            address_value = ent_address.get()
            if not address_value:
                showinfo('Error', 'Please enter the teacher\'s address')
                teacher_form.focus_force()
                return False


            # Mobile validation
            mobile_value = ent_mobile.get()
            if not mobile_value or not mobile_value.isdigit()or len(mobile_value) != 11:
                showinfo('Error', 'Mobile must be 11 digits')
                teacher_form.focus_force()
                return False

            # EducationID validation
            selected_education = comb_education_id.get()
            # Get selected education ID from the combobox
            if selected_education:
                education_id = int(selected_education.split(" - ")[0])  # Extract ID from the selected value
            else:
                showinfo('Error', 'Please select the teacher\'s education')
                return False

            # TeacherCode validation
            teacherCode_value = ent_teacher_code.get()
            if not teacherCode_value or not teacherCode_value.isdigit():
                showinfo('Error', 'TeacherCode is required and must contain only digits')
                teacher_form.focus_force()
                return False

            # MaritalStatus validation
            if not marital_status_string:
                showinfo('Error', 'Please select the teacher\'s marital_status')
                teacher_form.focus_force()
                return False

            # InsuranceNumber validation
            insuranceNumber_value = ent_insurance_number.get()
            if not insuranceNumber_value or not insuranceNumber_value.isdigit():
                showinfo('Error', 'InsuranceNumber is required and must contain only digits')
                teacher_form.focus_force()
                return False

            # AccountNumber validation
            account_number_value = ent_account_number.get()
            if not account_number_value or not account_number_value.isdigit()or len(account_number_value) != 16:
                showinfo('Error', 'AccountNumber must be 16 digits')
                teacher_form.focus_force()
                return False

            # CertificateID validation
            selected_certificate = comb_certificate_id.get()
            # Get selected certificate ID from the combobox
            if selected_certificate:
                certificate_id = int(selected_certificate.split(" - ")[0])  # Extract ID from the selected value
            else:
                showinfo('Error', 'Please select the teacher\'s certificate')
                return False

            # ResID validation
            res_id_value = ent_res_id.get()
            if not res_id_value :
                showinfo('Error', 'Please select the Certificate\'s ResID')
                teacher_form.focus_force()
                return False


            # Check if the national code already exists
            teacher_business_logic = TeacherBusinessLogic()
            if teacher_business_logic.checkNationalCodeExists(nationalCode):
                showinfo('Error', 'This National Code has already been registered.')
                #teacher_form.focus_force()
                ent_national_code.focus_force()
                return False

            # Create a new Teacher object
            new_teacher = Teacher(
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
                teacher_code=teacherCode_value,
                marital_status= marital_status_string,
                start_date = ent_date_start_date.get_date().strftime('%Y-%m-%d'),  # Format date
                insurance_number= insuranceNumber_value,
                account_number= account_number_value,
                certificate_id = certificate_id,
                expiration_date =ent_date_expiration_date.get_date().strftime('%Y-%m-%d'),
                res_id = res_id_value)
            # Insert the teacher into the database
            teacher_business_logic.insertTeacher(new_teacher)
            showinfo('Success', 'Teacher registered successfully')
            teacher_form.focus_force()
            # Clear the tree view (only if admin and tree is visible)
            if userparam.IsAdmin:
                for i in tree.get_children():
                    tree.delete(i)

                # Get the person_id from the newly inserted teacher
                person_id = new_teacher.person_id  # Assuming you have a way to get the person_id from the new_teacher object
                # Call getTeacherList with the person_id
                teacher_business_logic.getNewTeacherList(person_id)
                self.GetData = teacher_business_logic.AllDataTeacher
                for item in self.GetData:
                    tree.insert("",'end',values=( item[0],item[1], item[2], item[3], item[4], item[5], item[6], item[7], "", item[9], item[10],item[11],
                                                               item[12],item[13],item[14],item[15],item[16],item[17]))
                clearText() # Clear form for admins
                # For non-admins, do NOT clear the form so they can generate a card immediately





        # Function to update an existing teacher
        # Function to update an existing teacher (admin only)
        def updateTeacher():
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
                # Otherwise, get the photo from the currently selected teacher
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
                showinfo('Error', 'Please upload a photo of the teacher.')
                return False

            # FirstName validation
            if not firstName or not firstName.isalpha():
                showinfo('Error', 'FirstName is required and must contain only letters')
                teacher_form.focus_force()
                return False

            # LastName validation
            if not lastName or not lastName.isalpha():
                showinfo('Error', 'LastName is required and must contain only letters')
                teacher_form.focus_force()
                return False
            # NationalCode validation
            if not nationalCode or not nationalCode.isdigit() or len(nationalCode) != 10:
                showinfo('Error', 'NationalCode must be 10 digits')
                teacher_form.focus_force()
                return False
            # Gender validation
            if not gender_string:
                showinfo('Error', 'Please select the teacher\'s gender')
                teacher_form.focus_force()
                return False

            # Address validation
            address_value = ent_address.get()
            if not address_value:
                showinfo('Error', 'Please enter the teacher\'s address')
                teacher_form.focus_force()
                return False

            # Mobile validation
            mobile_value = ent_mobile.get()
            if not mobile_value or not mobile_value.isdigit()or len(mobile_value) != 11:
                showinfo('Error', 'Mobile must be 11 digits')
                teacher_form.focus_force()
                return False
            # EducationID validation
            selected_education = comb_education_id.get()
            # Get selected education ID from the combobox
            if selected_education:
                education_id = int(selected_education.split(" - ")[0])  # Extract ID from the selected value
            else:
                showinfo('Error', 'Please select the teacher\'s education')
                return False

            # teacherCode validation
            teacherCode_value = ent_teacher_code.get()
            if not teacherCode_value or not teacherCode_value.isdigit():
                showinfo('Error', 'TeacherCode is required and must contain only digits')
                teacher_form.focus_force()
                return False

            # MaritalStatus validation
            if not marital_status_string:
                showinfo('Error', 'Please select the teacher\'s marital_status')
                teacher_form.focus_force()
                return False

            # InsuranceNumber validation
            insuranceNumber_value = ent_insurance_number.get()
            if not insuranceNumber_value or not insuranceNumber_value.isdigit():
                showinfo('Error', 'InsuranceNumber is required and must contain only digits')
                teacher_form.focus_force()
                return False

            # AccountNumber validation
            account_number_value = ent_account_number.get()
            if not account_number_value or not account_number_value.isdigit()or len(account_number_value) != 16:
                showinfo('Error', 'AccountNumber must be 16 digits')
                teacher_form.focus_force()
                return False

            # CertificateID validation
            selected_certificate = comb_certificate_id.get()
            # Get selected certificate ID from the combobox
            if selected_certificate:
                certificate_id = int(selected_certificate.split(" - ")[0])  # Extract ID from the selected value
            else:
                showinfo('Error', 'Please select the teacher\'s certificate')
                return False

            # ResID validation
            res_id_value = ent_res_id.get()
            if not res_id_value :
                showinfo('Error', 'Please select the Certificate\'s ResID')
                teacher_form.focus_force()
                return False




            # Create a Teacher object with updated data
            updated_teacher = TeacherUpdate(
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
                teacher_code=teacherCode_value,
                marital_status= marital_status_string,
                start_date = ent_date_start_date.get_date().strftime('%Y-%m-%d'),  # Format date
                insurance_number= insuranceNumber_value,
                account_number= account_number_value,
                certificate_id = certificate_id,
                expiration_date =ent_date_expiration_date.get_date().strftime('%Y-%m-%d'),
                res_id = res_id_value)


            # Call business logic to update the teacher
            teacherBL = TeacherBusinessLogic(teacher_update=updated_teacher)
            teacherBL.updateTeacher()
            showinfo("Success", "Teacher updated successfully")
            teacher_form.focus_force()  # Bring the form to focus
            for i in tree.get_children():
                tree.delete(i)
            teacherBL = TeacherBusinessLogic()
            teacherBL.getNewTeacherList(person_id=self.UpdateID)
            self.GetData = teacherBL.AllDataTeacher

            for item in self.GetData:
                tree.insert("", 'end', values=item)
            clearText()


        # Function to delete a selected teacher
        # Function to delete a selected teacher (admin only)
        def deleteTeacher():
            if not self.DeleteID:
                showerror("Error", "No teacher selected for deletion")
                return
            # Confirm deletion
            if not msg.askyesno("Confirm", "Delete this teacher?"):
                return
            deleted_teacher = TeacherIdDelete(person_id=self.DeleteID)
            teacherBL = TeacherBusinessLogic(teacher_delete=deleted_teacher)
            teacherBL.deleteTeacher(deleted_teacher)

            showinfo("Success", "Teacher deleted successfully")
            populate_treeview()  # Refresh the tree
            clearText()



        # Function to select all teachers and populate the tree view
        # Function to select all teachers and populate the tree view (admin only)
        def selectAllTeachers():
            # Clear existing tree data
            for item in tree.get_children():
                tree.delete(item)

            # Fetch all teachers from database
            teacherBL = TeacherBusinessLogic()
            teacherBL.getNewAllTeachers()  # Fetch all teachers
            self.GetData = teacherBL.AllDataTeacher

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

        # Function to search for a teacher by national code
        # Function to search for a teacher by national code (admin only)
        def searchTeacher():
            national_code = ent_search_national_code.get().strip()

            # Validate input
            if not national_code:
                showinfo('Error', 'Please enter a NationalCode to search.')
                return
            # Validate national code
            if not national_code.isdigit() or len(national_code) != 10:
                showinfo('Error', 'NationalCode must be 10 digits.')
                return

            try:
                # Fetch teacher data based on national code
                teacher_business_logic = TeacherBusinessLogic()
                teacher_business_logic.getNewTeacherListByNationalCode(national_code)

                self.GetData = teacher_business_logic.AllDataTeacher

                if not self.GetData:
                    showinfo('Error', 'No teacher found with this NationalCode.')
                    return

                # Clear existing tree data
                for item in tree.get_children():
                    tree.delete(item)

                # Populate the tree view with the fetched teacher data
                for item in self.GetData:
                    photo_thumb = create_thumbnail_15x15(item[8]) if item[8] else None
                    tree.insert("", "end",
                                values=(item[0], item[1], item[2], item[3], item[4],
                                        item[5], item[6], item[7], "",
                                        item[9], item[10], item[11],item[12],item[13],item[14],item[15],item[16],item[17]),
                                image=photo_thumb)

            except Exception as e:
                showerror("Error", f"An error occurred during search: {str(e)}")

        # Function to generate a teacher identification card
        def generate_teacher_card():
            # Check if user is admin and has a selection
            if userparam.IsAdmin:
                selected_item = tree.focus()
                if not selected_item:
                    msg.showinfo("Error", "Please select a teacher from the list.")
                    return

                # Get teacher data from the selected item
                record = tree.item(selected_item)['values']

            else:
                # For non-admin, use current form data (assuming it's filled for the newly registered teacher)
                first_name = ent_first_name.get()
                last_name = ent_last_name.get()
                birthdate = ent_date_birthdate.get_date().strftime('%d/%m/%Y') if ent_date_birthdate.get_date() else ""
                national_code = ent_national_code.get()
                gender = "Male" if txt_gender.get() == "1" else "Female" if gender_radiogroup.get() == "2" else ""
                mobile = ent_mobile.get()
                teacher_code = ent_teacher_code.get()
                photo_data = self.uploaded_photo  # Use uploaded photo
                if not all([first_name, last_name, birthdate, national_code, gender, mobile, teacher_code, photo_data]):
                    msg.showinfo("Error", "Please fill in all required fields and upload a photo to generate the card.")
                    return
                record = [None, first_name, last_name, birthdate, national_code, gender, None, mobile, photo_data, None,
                          teacher_code, None]


            # Create a new Toplevel window for the teacher card
            card_window = Toplevel()
            card_window.title("Teacher Identification Card") # Set the title of the card window
            card_window.geometry("600x475")  # Set the size of the card window
            card_window.resizable(False, False) # Disable resizing of the card window

            # Style the card window
            card_window.configure(bg='#f0f0f0')

            # Extract data from record
            first_name = record[1]
            last_name = record[2]
            birthdate = record[3]
            national_code = record[4]
            gender = record[5]
            mobile = record[7]
            teacher_code = record[10]
            photo_data = record[8]  # Photo binary data



            # Main card frame to hold all elements
            card_frame = Frame(card_window, bg='white', bd=2, relief='groove', padx=20, pady=20)
            card_frame.pack(pady=20, padx=20)

            # Card header
            header_frame = Frame(card_frame, bg='#1E90FF')
            header_frame.pack(fill='x', pady=(0, 20))
            # Title label for the card
            lbl_title = Label(header_frame,
                              text="TEACHER IDENTIFICATION CARD",
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

            ### Teacher information labels
            # School name label
            lbl_school = Label(info_frame,
                                   text="SEMATEC INSTITUTE",
                               font=('Arial', 14, 'bold'),
                               anchor='w')
            lbl_school.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky='w')

            # Function to create a row of teacher information
            def create_info_row(parent, row, label, value):
                lbl = Label(parent, text=label, font=('Arial', 10, 'bold'), anchor='w') # Label for the field
                lbl.grid(row=row, column=0, sticky='w', pady=2)
                val = Label(parent, text=value, font=('Arial', 10), anchor='w') # Label for the value
                val.grid(row=row, column=1, sticky='w', pady=2, padx=(10, 0))

            # Add teacher information to the card
            create_info_row(info_frame, 1, "Teacher ID:", teacher_code)
            create_info_row(info_frame, 2, "Full Name:", f"{first_name} {last_name}")
            create_info_row(info_frame, 3, "Date of Birth:", birthdate)
            create_info_row(info_frame, 4, "National Code:", national_code)
            create_info_row(info_frame, 5, "Gender:", gender)
            create_info_row(info_frame, 8, "Contact:", mobile)


            # Footer with teacher signature
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

            # Function to save the teacher card as an image
            def save_teacher_card():
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                    initialfile=f"teacher_card_{teacher_code}"
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
                        draw.text((100, 25), "TEACHER IDENTIFICATION CARD", font=font, fill='black')
                        font = ImageFont.truetype("arial.ttf", 18) # Load font for school name
                        draw.text((220, 90), "SEMATEC INSTITUTE", font=font, fill='black')

                        font = ImageFont.truetype("arial.ttf", 14) # Load font for student info
                        info_y = 130  # Starting Y position for info
                        draw.text((220, info_y), f"Teacher ID: {teacher_code}", font=font, fill='black')
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
                        msg.showinfo("Success", f"teacher card saved as:\n{file_path}")
                    except Exception as e:
                        msg.showerror("Error", f"Failed to save card: {str(e)}")

            # Buttons for saving and closing the card window
            btn_save = ttk.Button(btn_frame, text="Save Card", command=save_teacher_card)
            btn_save.pack(side='left', padx=5)
            btn_close = ttk.Button(btn_frame, text="Close", command=card_window.destroy)
            btn_close.pack(side='left', padx=5)
            # Auto-refresh the card window
            card_window.update()


        #frame
        frame = ctk.CTkFrame(teacher_form, width = 880,height= 660)
        frame_button  = ctk.CTkFrame(teacher_form,width = 880 , height= 20)
        frame_grid = ctk.CTkFrame(teacher_form,width= 880,height=10)


        frame.grid(row=0,column=0, padx= 10,pady = 5,sticky='nsew')
        frame_button.grid(row=1,column=0 , padx=10 ,pady = 5,sticky='nsew' )
        frame_grid.grid(row=2,column=0, sticky='nsew',pady = 5 , padx = 10)
        ##


        #Photo section - top left
        photo_container = ctk.CTkFrame(frame)
        photo_container.grid(row=0, column=0, padx=10, pady=5, sticky="nw")

        #Photo frame with border
        photo_frame=ctk.CTkFrame(photo_container, width =105, height = 105 , border_width=3,
                                   border_color='green')
        photo_frame.pack_propagate(0)  # Prevent the frame from resizing to fit the contents
        photo_frame.pack(side=ctk.LEFT)  # Pack the photo_frame into the photo_container
        # Create a label to display the photo
        photo_label = ctk.CTkLabel(photo_frame, text="", width=100, height=100)
        photo_label.pack(side=ctk.LEFT)

        # Update the button to call the upload_photo function
        btn_UploadPhoto = ctk.CTkButton(frame, text='Upload Photo', command=upload_photo)
        btn_UploadPhoto.grid(row=0, column=1,  padx=10, pady=40, sticky='nw')

        #new section - top Right
        new_section = ctk.CTkFrame(frame)
        new_section.grid(row=0, column=2, padx=10, pady=5, sticky="nw")

        new_section.grid_rowconfigure(0, minsize = 35)
        new_section.grid_rowconfigure(1, minsize = 35)
        new_section.grid_rowconfigure(2, minsize = 35)

        # Register validation functions
        vcmd_national_code = (teacher_form.register(validate_national_code), '%P')
        vcmd_mobile = (teacher_form.register(validate_mobile), '%P')
        vcmd_insurance_number = (teacher_form.register(validate_insurance_number), '%P')
        vcmd_account_number = (teacher_form.register(validate_account_number), '%P')
        vcmd_res_id = (teacher_form.register(validate_res_id), '%P')
        vcmd_20 = (teacher_form.register(validate20), '%P')
        vcmd_30 = (teacher_form.register(validate30), '%P')
        vcmd_40 = (teacher_form.register(validate40), '%P')

        # Label : FirstName
        lbl_first_name = ctk.CTkLabel(frame, text='FirstName: ')
        lbl_first_name.grid(row=1, column=0, padx=10, pady=3, sticky='w')
        # Entry : FirstName
        ent_first_name = ctk.CTkEntry(frame, width=200, placeholder_text="Enter first name")
        ent_first_name.configure(validate="key", validatecommand=vcmd_20)
        ent_first_name.grid(row=1, column=1, padx=10, pady=3, sticky='e')
        # Label : LastName
        lbl_last_name = ctk.CTkLabel(frame, text='LastName: ')
        lbl_last_name.grid(row=1, column=2, padx=50, pady=3, sticky='w')
        # Entry : LastName
        ent_last_name = ctk.CTkEntry(frame, width=200, placeholder_text="Enter last name")
        ent_last_name.configure(validate="key", validatecommand=vcmd_30)
        ent_last_name.grid(row=1, column=2, padx=90, pady=3, sticky='ne')
        #
        # Birthdate
        lbl_birthdate = ctk.CTkLabel(frame, text='Birthdate: (dd/mm/yyyy) ')
        lbl_birthdate.grid(row=2, column=0, padx=10, pady=3, sticky='w')
        # Entry : Birthdate
        date_frame = ctk.CTkFrame(frame)
        date_frame.grid(row=2, column=1, padx=10, pady=3, sticky='e')
        ent_date_birthdate = DateEntry(date_frame, width=26, date_pattern='dd/mm/yyyy')
        ent_date_birthdate.pack()
        # Label : NationalCode
        lbl_national_code = ctk.CTkLabel(frame, text='NationalCode: ')
        lbl_national_code.grid(row=2, column=2, padx=50, pady=3, sticky='w')
        # Entry : NationalCode
        ent_national_code = ctk.CTkEntry(frame, width=200, placeholder_text="Enter 10-digit code")
        ent_national_code.configure(validate="key", validatecommand=vcmd_national_code)
        ent_national_code.grid(row=2, column=2, padx=90, pady=3, sticky='ne')
        #
        # Label : Gender
        lbl_gender = ctk.CTkLabel(frame, text='Gender: ')
        lbl_gender.grid(row=3, column=0, padx=10, pady=3, sticky='w')
        # Radiobutton :
        txt_gender = ctk.StringVar()
        rb_gender_male = ctk.CTkRadioButton(frame, text='Male', variable=txt_gender, value=1)
        rb_gender_male.grid(row=3, column=1, padx=10, pady=3, sticky='w')
        rb_gender_female = ctk.CTkRadioButton(frame, text='Female', variable=txt_gender, value=2)
        rb_gender_female.grid(row=3, column=1, padx=10, pady=3, sticky='e')
        # Label : Address
        lbl_address = ctk.CTkLabel(frame, text='Address: ')
        lbl_address.grid(row=3, column=2, padx=50, pady=3, sticky='w')
        # Entry : Address
        ent_address = ctk.CTkEntry(frame, width=200, placeholder_text="Enter address")
        ent_address.configure(validate="key", validatecommand=vcmd_40)
        ent_address.grid(row=3, column=2, padx=90, pady=3, sticky='ne')
        #
        # Label : Mobile
        lbl_mobile = ctk.CTkLabel(frame, text='Mobile: ')
        lbl_mobile.grid(row=4, column=0, padx=10, pady=3, sticky='w')
        # Entry : Mobile
        ent_mobile = ctk.CTkEntry(frame, width=200, placeholder_text="Enter mobile")
        ent_mobile.configure(validate="key", validatecommand=vcmd_mobile)
        ent_mobile.grid(row=4, column=1, padx=10, pady=3, sticky='e')
        # Label : Education
        lbl_education_id = ctk.CTkLabel(frame, text='EducationID: ')
        lbl_education_id.grid(row=4, column=2, padx=50, pady=3, sticky='w')
        comb_education_id = ctk.CTkComboBox(frame, width=200)
        comb_education_id.grid(row=4, column=2, padx=90, pady=3, sticky='ne')
        # Fetch education levels and populate the combobox
        education_levels = self.fetchEducationLevels()
        comb_education_id.configure(values=[f"{level[0]} - {level[1]}" for level in education_levels])
        comb_education_id.set("Select EducationID")

        # Label : TeacherCode
        lbl_teacher_code = ctk.CTkLabel(frame, text='TeacherCode')
        lbl_teacher_code.grid(row=5, column=0, padx=10, pady=3, sticky='w')
        # Entry : TeacherCode
        ent_teacher_code = ctk.CTkEntry(frame, width=200, placeholder_text="Enter teacher code")
        ent_teacher_code.grid(row=5, column=1, padx=10, pady=3, sticky='e')
        # Label : MaritalStatus
        lbl_marital_status = ctk.CTkLabel(frame, text='MaritalStatus: ')
        lbl_marital_status.grid(row=5, column=2, padx=50, pady=3, sticky='w')
        # Radiobutton : MaritalStatus (using CustomTkinter radiogroup)
        txt_marital_status = ctk.StringVar()
        rb_gender_married = ctk.CTkRadioButton(frame, text='Married', variable=txt_marital_status, value=1)
        rb_gender_married.grid(row=5, column=2, padx=230, pady=3, sticky='w')
        rb_gender_single = ctk.CTkRadioButton(frame, text='Single', variable=txt_marital_status, value=2)
        rb_gender_single.grid(row=5, column=2, padx=70, pady=3, sticky='e')

        #
        # StartDate
        lbl_start_date = ctk.CTkLabel(frame, text='StartDate: (dd/mm/yyyy) ')
        lbl_start_date.grid(row=6, column=0, padx=10, pady=3, sticky='w')
        # Entry : StartDate
        ent_date_start_date = DateEntry(frame, width=26, date_pattern='dd/mm/yyyy')
        ent_date_start_date.grid(row=6, column=1, padx=10, pady=3, sticky='e')
        # Label : InsuranceNumber
        lbl_insurance_number = ctk.CTkLabel(frame, text='InsuranceNumber')
        lbl_insurance_number.grid(row=6, column=2, padx=50, pady=3, sticky='w')
        # Entry : InsuranceNumber
        ent_insurance_number = ctk.CTkEntry(frame, width=200, placeholder_text="Enter insurance number")
        ent_insurance_number.configure(validate="key", validatecommand=vcmd_insurance_number)
        ent_insurance_number.grid(row=6, column=2, padx=90, pady=3, sticky='ne')
        #
        # Label : AccountNumber
        lbl_account_number = ctk.CTkLabel(frame, text='AccountNumber: ')
        lbl_account_number.grid(row=7, column=0, padx=10, pady=3, sticky='w')
        # Entry : AccountNumber
        ent_account_number = ctk.CTkEntry(frame, width=200, placeholder_text="Enter account number")
        ent_account_number.configure(validate="key", validatecommand=vcmd_account_number)
        ent_account_number.grid(row=7, column=1, padx=10, pady=3, sticky='e')
        # Label : CertificateID
        lbl_certificate_id = ctk.CTkLabel(new_section, text='CertificateID: ')
        lbl_certificate_id.grid(row=0, column=2, padx=40, pady=3, sticky='w')
        comb_certificate_id = ctk.CTkComboBox(new_section, width=200)
        comb_certificate_id.grid(row=0, column=3, padx=10, pady=3, sticky='w')
        # Fetch certificate levels and populate the combobox
        certificate_levels = self.fetchCertificateLevels()
        comb_certificate_id.configure(values=[f"{level[0]} - {level[1]}" for level in certificate_levels])
        comb_certificate_id.set("Select CertificateID")

        # ExpirationDate
        lbl_expiration_date = ctk.CTkLabel(new_section, text='ExpirationDate: (dd/mm/yyyy) ')
        lbl_expiration_date.grid(row=1, column=2, padx=40, pady=3, sticky='w')
        # Entry : ExpirationDate
        ent_date_expiration_date = DateEntry(new_section, width=27, date_pattern='dd/mm/yyyy')
        ent_date_expiration_date.grid(row=1, column=3, padx=10, pady=3, sticky='w')
        # Label : ResID
        lbl_res_id = ctk.CTkLabel(new_section, text='ResID: ')
        lbl_res_id.grid(row=2, column=2, padx=40, pady=3, sticky='w')
        # Entry : ResID
        ent_res_id = ctk.CTkEntry(new_section, width=200, placeholder_text="Enter ResID")
        ent_res_id.configure(validate="key", validatecommand=vcmd_res_id)
        ent_res_id.grid(row=2, column=3, padx=10, pady=3, sticky='w')# frameButton : updateTeacher

        # Buttons (shift to row=1)
        btn_clear_teacher = ctk.CTkButton(frame_button, text='Clear', command=clearText, width=150)
        btn_clear_teacher.grid(row=9, column=0, padx=10, pady=3, sticky='w')  # Changed row from 7 to 1

        btn_select_all = ctk.CTkButton(frame_button, text='Select All', command=selectAllTeachers, width=150)
        btn_select_all.grid(row=9, column=1, padx=10, pady=3, sticky='w')  # Changed row from 7 to 1

        btn_insert_teacher = ctk.CTkButton(frame_button, text='Insert', command=registerTeacher, width=150)
        btn_insert_teacher.grid(row=9, column=2, padx=10, pady=3, sticky='e')  # Changed row from 7 to 1

        btn_update_teacher = ctk.CTkButton(frame_button, text='Update', command=updateTeacher, width=150)
        btn_update_teacher.grid(row=9, column=3, padx=10, pady=3, sticky='w')
        # frameButton : deleteTeacher
        btn_delete_teacher = ctk.CTkButton(frame_button, text='Delete', command=deleteTeacher, width=150)
        btn_delete_teacher.grid(row=9, column=4, padx=10, pady=3, sticky='w')

        # frameButton : closeTeacher
        btn_backToMain_teacher = ctk.CTkButton(frame_button, text='BackToMain', command=destroyForm, width=150)
        btn_backToMain_teacher.grid(row=10, column=4, padx=10, pady=3, sticky='w')
        # Label: Search by National Code
        lbl_search_national_code = ctk.CTkLabel(frame_button, text='Search By NationalCode: ')
        lbl_search_national_code.grid(row=10, column=0, padx=10, pady=3, sticky='w')
        # Entry: Search National Code
        ent_search_national_code = ctk.CTkEntry(frame_button, width=150, placeholder_text="Enter NationalCode")
        ent_search_national_code.grid(row=10, column=1, padx=10, pady=3, sticky='w')
        # Button: Search
        btn_search_teacher = ctk.CTkButton(frame_button, text='Search', command=searchTeacher, width=150)
        btn_search_teacher.grid(row=10, column=2, padx=10, pady=3, sticky='e')
        # Add the Generate Teacher Card button
        btn_generate_card = ctk.CTkButton(frame_button, text='Generate Teacher Card', command=generate_teacher_card, width=150)
        btn_generate_card.grid(row=10, column=3, padx=10, pady=3, sticky='w')

        # frameButton : Export to Excel
        btn_export_excel = ctk.CTkButton(frame_button, text='Export to Excel', command=export_to_excel, width=150)
        btn_export_excel.grid(row=11, column=0, padx=10, pady=3, sticky='w')

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
        columns = ('person_id','first_name','last_name','birthdate','national_code','gender','address','mobile','photo','education_id','teacher_code','marital_status',
                   'start_date','insurance_number','account_number','certificate_id','expiration_date','res_id')
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
        tree.heading('teacher_code', text='TeacherCode', anchor='w')
        tree.heading('marital_status', text='MaritalStatus', anchor='w')
        tree.heading('start_date', text='StartDate', anchor='w')
        tree.heading('insurance_number', text='InsuranceNumber', anchor='w')
        tree.heading('account_number', text='AccountNumber', anchor='w')
        tree.heading('certificate_id', text='CertificateID', anchor='w')
        tree.heading('expiration_date', text='ExpirationDate', anchor='w')
        tree.heading('res_id', text='ResID', anchor='w')

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
            teacherBusinessLogic = TeacherBusinessLogic()
            teacherBusinessLogic.getNewTeacherList(userparam.IsAdmin) # PersonID
            self.GetData = teacherBusinessLogic.AllDataTeacher

            for item in self.GetData:
                photo_thumb = create_thumbnail_15x15(item[8])
                if photo_thumb:
                    self.photo_cache[item[0]] = photo_thumb
                    tree.insert("", "end",
                                values=(item[0], item[1], item[2], item[3], item[4],
                                        item[5], item[6], item[7], "",
                                        item[9], item[10], item[11],item[12],item[13],item[14],item[15],item[16],item[17]),
                                image=photo_thumb)
                else:
                    tree.insert("", "end",
                                values=(item[0], item[1], item[2], item[3], item[4],
                                        item[5], item[6], item[7], "No Photo",
                                        item[9], item[10], item[11],item[12],item[13],item[14],item[15],item[16],item[17]))

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

            ent_teacher_code.delete(0, END)
            ent_teacher_code.insert(0, record[10])
            # Set the maritalStatus radio button
            if record[11] == "M":  # Check if the maritalStatus is "Married"
                txt_marital_status.set(1) # Set to 1 for Married
            elif record[11] == "S":  # Check if the maritalStatus is "Single"
                txt_marital_status.set(2)  # Set to 2 for Single
            else:
                txt_marital_status.set(0)  # Clear selection if maritalStatus is not recognized

            # Handle the date conversion
            try:
                # Check if record[12] is a string or a date object
                if isinstance(record[12], str):
                    start_date = datetime.strptime(record[12], '%Y-%m-%d').date()  # Convert to date object
                else:
                    start_date = record[12]  # Assume it's already a date object
                ent_date_start_date.set_date(start_date)  # Set the date in the DateEntry
            except ValueError as e:
                print(f"Error converting date: {e}")
                ent_date_start_date.set_date('')  # Clear the date entry if there's an error

            ent_insurance_number.delete(0, END)
            ent_insurance_number.insert(0, record[13])
            ent_account_number.delete(0,END)
            ent_account_number.insert(0, record[14])
            comb_certificate_id.set(record[15])  # Set the selected value for the combobox
            # Handle the date conversion
            try:
                # Check if record[16] is a string or a date object
                if isinstance(record[16], str):
                    expiration_date = datetime.strptime(record[16], '%Y-%m-%d').date()  # Convert to date object
                else:
                    expiration_date = record[16]  # Assume it's already a date object
                ent_date_expiration_date.set_date(expiration_date)  # Set the date in the DateEntry
            except ValueError as e:
                print(f"Error converting date: {e}")
                ent_date_expiration_date.set_date('')  # Clear the date entry if there's an error

            ent_res_id.delete(0,END)
            ent_res_id.insert(0, record[17])





            # ========== PHOTO HANDLING SECTION ==========
            # Handle photo display
            photo_data = next((x[8] for x in self.GetData if x[0] == record[0]), None)

            # Clear current photo
            photo_label.configure(image=None)
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
        teacher_form.columnconfigure(0, weight=1)
        teacher_form.rowconfigure(0, weight=1)
        frame_grid.columnconfigure(0, weight=3)
        frame_grid.columnconfigure(1, weight=3)
        frame_grid.columnconfigure(2, weight=3)
        frame_grid.columnconfigure(3, weight=1)
        frame_grid.columnconfigure(4, weight=1)
        frame_grid.rowconfigure(1, weight=1)

        # Access control for non-admin users
        if not userparam.IsAdmin:
            # Disable admin-only buttons
            btn_update_teacher.configure(state='disabled')
            btn_delete_teacher.configure(state='disabled')
            btn_select_all.configure(state='disabled')
            btn_search_teacher.configure(state='disabled')
            btn_export_excel.configure(state='disabled')  # Disable export for non-admins
            # btn_generate_card.configure(state='disabled')

            # Hide search-related widgets
            lbl_search_national_code.grid_forget()
            ent_search_national_code.grid_forget()

            # Optionally hide the data grid (treeview) to avoid showing an empty table
            frame_grid.grid_forget()

            # Note: btn_clear_teacher, btn_insert_teacher,btn_generate_card and btn_backToMain_teacher remain enabled









        teacher_form.mainloop()


