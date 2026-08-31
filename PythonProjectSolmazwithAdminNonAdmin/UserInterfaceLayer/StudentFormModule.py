# Import necessary libraries for GUI, image handling, and date management
import customtkinter as ctk  # Changed from tkinter

from customtkinter import CTkImage
import io
from openpyxl import Workbook  # Added for Excel export



from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo, showerror
from customtkinter import CTkToplevel
from tkinter import Toplevel  # Import Toplevel
from PIL import Image, ImageTk,ImageDraw, ImageFont
from datetime import datetime, timedelta
from tkcalendar.dateentry import DateEntry



from BusinessLogicLayer.StudentBusinessLogic import StudentBusinessLogic
from Model.UserModule import UserModel
from Model.StudentModel import Student, StudentUpdate, StudentIdDelete


# Set CustomTkinter appearance (add this for modern look)
ctk.set_appearance_mode("Dark")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue", "green", "dark-blue"


##
class StudentFormClass:
    # Initialize the StudentFormClass with user and main form references
    def __init__(self,userparam : UserModel, main_form, switch_indication_func=None, home_indicator=None):
        self.User = userparam
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
        student_business_logic = StudentBusinessLogic()
        education_levels = student_business_logic.getEducationList()  # Fetch education levels
        return education_levels

    # Fetch education levels from the business logic layer
    def student_form_load(self, userparam: UserModel):
        student_form = ctk.CTkToplevel()  # Changed from Toplevel
        student_form.tk.call('tk', 'scaling', 1.5)
        student_form.title('StudentForm...')
        student_form.resizable(0, 0)
        if userparam.IsAdmin:
            student_form.geometry('770x690')
        else:
            student_form.geometry('770x450')
        x = int(student_form.winfo_screenwidth() / 2 - 770 / 2)
        y = int(student_form.winfo_screenheight() / 2 - 690 / 2)
        student_form.geometry('+{}+{}'.format(x, y))
        student_form.iconbitmap('images/ImagesStudentForm/Student1.ico')

        # Function to create a thumbnail from binary photo data
        def create_photo_thumbnail(photo_data):
            """Create a thumbnail from binary photo data"""
            if not photo_data:
                return None
            try:
                # Convert bytes to image
                pil_image = Image.open(io.BytesIO(photo_data))
                pil_image.thumbnail((100, 100))  # Resize to thumbnail
                return ImageTk.PhotoImage(pil_image)
            except Exception as e:
                print(f"Error creating thumbnail: {e}")
                return None

        # Function to close the student form and show the main form
        def destroyForm():
            student_form.withdraw()  # Close the student form
            self.main_form.deiconify()  # Show the main form FIRST
            self.main_form.update()  # Force a UI refresh to ensure changes are visible
            if self.switch_indication and self.home_btn_indicator:  # Check if home indicator is available (fixed condition)
                self.switch_indication(
                    indicator_lb=self.home_btn_indicator)  # Activate home indicator AFTER showing the form
                self.main_form.update()  # Force another UI refresh to ensure the indicator change is visible

        # Function to clear all input fields
        def clearText():
            ent_first_name.delete(0, END)
            ent_last_name.delete(0, END)
            ent_date_birthdate.set_date(datetime.now().date())  # Set to current date
            ent_national_code.delete(0, END)  # Changed from txt_search_national_code.set('')
            txt_gender.set('')  # Reset gender selection
            ent_address.delete(0, END)
            ent_mobile.delete(0, END)  # Assuming this is a CTkEntry; if it's a StringVar, use set('')
            photo_label.configure(image=None)  # Changed from config(image='') to configure(image=None)
            photo_label.image = None  # Clear the reference to avoid garbage collection
            comb_education_id.set('')  # Clear the combobox
            ent_student_code.delete(0, END)
            ent_job.delete(0, END)

        # Validation functions for input fields
        # for ent_national_code
        def validate_national_code(value):
            if value == "":
                return True  # Allow empty input
            return value.isdigit() and len(value) <= 10  # Allow only digits and up to 10 digits

        def validate_mobile(value):
            if value == "":
                return True  # Allow empty input
            return value.isdigit() and len(value) <= 11  # Allow only digits and up to 11 digits
        # for ent_first_name
        def validate20(value):
            return len(value) <= 20
        # for ent_last_name
        def validate30(value):
            return len(value) <= 30
        # for ent_address
        def validate40(value):
            return len(value) <= 40

        # Function to upload a photo
        def upload_photo():
            try:
                f_types = [('Jpg Files', '*.jpg'), ('All Files', '*.*')]
                filename = filedialog.askopenfilename(filetypes=f_types)
                if filename:
                    # Load the image
                    pil_img = Image.open(filename)
                    pil_img = pil_img.resize((100, 100), Image.LANCZOS)  # Resize image to fit in the label
                    image = CTkImage(pil_img, size=(100, 100))  # Use CTkImage instead of ImageTk.PhotoImage

                    # Display the image in the label
                    photo_label.configure(image=image)  # Changed from config to configure
                    photo_label.image = image  # Keep a reference to avoid garbage collection

                    # Store the image data in an instance variable
                    self.uploaded_photo = pil_img  # Store the PIL image for later use
            except Exception as e:
                msg.showerror("Error", f"An error occurred while uploading the photo: {e}")

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
                ws.title = "Students"
                # Define headers (excluding 'photo' as it's binary; we'll add a 'Photo Exists?' column)
                headers = ['PersonID', 'FirstName', 'LastName', 'BirthDate', 'NationalCode', 'Gender', 'Address',
                           'Mobile', 'Photo Exists?', 'EducationID', 'StudentCode', 'Job']
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

        # Function to register a new student
        def registerStudent():
            # Gather data from the input fields
            firstName = ent_first_name.get()
            lastName = ent_last_name.get()
            nationalCode = ent_national_code.get()
            # Convert gender from number to string
            gender_value = txt_gender.get()
            gender_string = "Male" if gender_value == "1" else "Female" if gender_value == "2" else None

            # Photo validation # Check if an image was uploaded
            if not self.uploaded_photo:
                showinfo('Error', 'Please upload a photo of the student.')
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
                student_form.focus_force()
                return False
            # LastName validation
            if not lastName or not lastName.isalpha():
                showinfo('Error', 'LastName is required and must contain only letters')
                student_form.focus_force()
                return False
            # NationalCode validation
            if not nationalCode or not nationalCode.isdigit() or len(nationalCode) != 10:
                showinfo('Error', 'NationalCode must be 10 digits')
                student_form.focus_force()
                return False
            # Gender validation
            if not gender_string:
                showinfo('Error', 'Please select the student\'s gender')
                student_form.focus_force()
                return False

            # Address validation
            address_value = ent_address.get()
            if not address_value:
                showinfo('Error', 'Please enter the student\'s address')
                student_form.focus_force()
                return False

            # Mobile validation
            mobile_value = ent_mobile.get()
            if not mobile_value or not mobile_value.isdigit() or len(mobile_value) != 11:
                showinfo('Error', 'Mobile must be 11 digits')
                student_form.focus_force()
                return False

            # EducationID validation
            selected_education = comb_education_id.get()
            # Get selected education ID from the combobox
            if selected_education:
                education_id = int(selected_education.split(" - ")[0])  # Extract ID from the selected value
            else:
                showinfo('Error', 'Please select the student\'s education')
                return False

            # StudentCode validation
            studentCode_value = ent_student_code.get()
            if not studentCode_value or not studentCode_value.isdigit():
                showinfo('Error', 'StudentCode is required and must contain only digits')
                student_form.focus_force()
                return False

            # Job validation
            job_value = ent_job.get()
            if not job_value or not job_value.isalpha():
                showinfo('Error', 'Job is required and must contain only letters')
                student_form.focus_force()
                return False

            # Check if the national code already exists
            student_business_logic = StudentBusinessLogic()
            if student_business_logic.checkNationalCodeExists(nationalCode):
                showinfo('Error', 'This National Code has already been registered.')
                # student_form.focus_force()
                ent_national_code.focus_force()
                return False

            # Create a new Student object
            new_student = Student(
                first_name=firstName,
                last_name=lastName,
                birthdate=ent_date_birthdate.get_date().strftime('%Y-%m-%d'),  # Format date
                national_code=nationalCode,
                gender=gender_string,  # Use the string representation of gender
                address=address_value,
                mobile=mobile_value,
                photo=photo_data,  # Pass the binary photo data
                education_id=education_id,  # Use the selected education ID
                # education_id=int(comb_education_id.get()),
                student_code=studentCode_value,
                job=job_value)

            # Insert the student into the database
            student_business_logic.insertStudent(new_student)
            showinfo('Success', 'Student registered successfully')
            student_form.focus_force()
            # Clear the tree view (only if admin and tree is visible)
            if userparam.IsAdmin:
                for i in tree.get_children():
                    tree.delete(i)
                # Get the person_id from the newly inserted student
                person_id = new_student.person_id  # Assuming you have a way to get the person_id from the new_student object
                # Call getStudentList with the person_id
                student_business_logic.getStudentList(person_id)
                self.GetData = student_business_logic.AllDataStudent
                for item in self.GetData:
                    tree.insert("", 'end',
                                values=(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], "", item[9],
                                        item[10], item[11]))
                clearText()  # Clear form for admins
                # For non-admins, do NOT clear the form so they can generate a card immediately

        # Function to update an existing student
        # Function to update an existing student (admin only)
        def updateStudent():
            # Gather data from the input fields
            firstName = ent_first_name.get()
            lastName = ent_last_name.get()
            nationalCode = ent_national_code.get()
            gender_value = txt_gender.get()
            gender_string = "Male" if gender_value == "1" else "Female" if gender_value == "2" else None

            # Get the current photo data (either newly uploaded or existing)
            photo_data = None
            if self.uploaded_photo:
                # If new photo was uploaded, use it
                with io.BytesIO() as output:
                    self.uploaded_photo.save(output, format='JPEG')
                    photo_data = output.getvalue()
            else:
                # Otherwise, get the photo from the currently selected student
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
                showinfo('Error', 'Please upload a photo of the student.')
                return False

            # FirstName validation
            if not firstName or not firstName.isalpha():
                showinfo('Error', 'FirstName is required and must contain only letters')
                student_form.focus_force()
                return False

            # LastName validation
            if not lastName or not lastName.isalpha():
                showinfo('Error', 'LastName is required and must contain only letters')
                student_form.focus_force()
                return False
            # NationalCode validation
            if not nationalCode or not nationalCode.isdigit() or len(nationalCode) != 10:
                showinfo('Error', 'NationalCode must be 10 digits')
                student_form.focus_force()
                return False
            # Gender validation
            if not gender_string:
                showinfo('Error', 'Please select the student\'s gender')
                student_form.focus_force()
                return False

            # Address validation
            address_value = ent_address.get()
            if not address_value:
                showinfo('Error', 'Please enter the student\'s address')
                student_form.focus_force()
                return False

            # Mobile validation
            mobile_value = ent_mobile.get()
            if not mobile_value or not mobile_value.isdigit() or len(mobile_value) != 11:
                showinfo('Error', 'Mobile must be 11 digits')
                student_form.focus_force()
                return False
            # EducationID validation
            selected_education = comb_education_id.get()
            # Get selected education ID from the combobox
            if selected_education:
                education_id = int(selected_education.split(" - ")[0])  # Extract ID from the selected value
            else:
                showinfo('Error', 'Please select the student\'s education')
                return False

            # StudentCode validation
            studentCode_value = ent_student_code.get()
            if not studentCode_value or not studentCode_value.isdigit():
                showinfo('Error', 'StudentCode is required and must contain only digits')
                student_form.focus_force()
                return False

            # Job validation
            job_value = ent_job.get()
            if not job_value or not job_value.isalpha():
                showinfo('Error', 'Job is required and must contain only letters')
                student_form.focus_force()
                return False

            # Create a Student object with updated data
            updated_student = StudentUpdate(
                person_id=self.UpdateID,  # Use the stored UpdateID
                first_name=firstName,
                last_name=lastName,
                birthdate=ent_date_birthdate.get_date().strftime('%Y-%m-%d'),
                national_code=nationalCode,
                gender=gender_string,
                address=address_value,
                mobile=mobile_value,
                photo=photo_data,  # Use either existing or new photo
                education_id=education_id,  # Use the selected education ID
                # education_id=int(comb_education_id.get()),
                student_code=studentCode_value,
                job=job_value
            )

            # Call business logic to update the student
            studentBL = StudentBusinessLogic(student_update=updated_student)
            studentBL.updateStudent()
            showinfo("Success", "Student updated successfully")
            student_form.focus_force()  # Bring the form to focus
            for i in tree.get_children():
                tree.delete(i)
            studentBL = StudentBusinessLogic()
            studentBL.getStudentList(person_id=self.UpdateID)
            self.GetData = studentBL.AllDataStudent

            for item in self.GetData:
                tree.insert("", 'end', values=item)
            clearText()

        # Function to delete a selected student
        # Function to delete a selected student (admin only)
        def deleteStudent():
            if not self.DeleteID:
                showerror("Error", "No student selected for deletion")
                return
            # Confirm deletion
            if not msg.askyesno("Confirm", "Delete this student?"):
                return
            deleted_student = StudentIdDelete(person_id=self.DeleteID)
            studentBL = StudentBusinessLogic(student_delete=deleted_student)
            studentBL.deleteStudent(deleted_student)

            showinfo("Success", "Student deleted successfully")
            populate_treeview()  # Refresh the tree
            clearText()

        # Function to select all students and populate the tree view
        # Function to select all students and populate the tree view (admin only)
        def selectAllStudents():
            # Clear existing tree data
            for item in tree.get_children():
                tree.delete(item)

            # Fetch all students from database
            studentBL = StudentBusinessLogic()
            studentBL.getAllStudents()  # Fetch all students
            self.GetData = studentBL.AllDataStudent

            # Insert all records into treeview
            for item in self.GetData:
                # print(f"Processing item: {item}")  # Debugging line
                photo_thumb = create_thumbnail_15x15(item[8]) if item[8] else None
                # print(f"Thumbnail created: {photo_thumb}")  # Debugging line
                tree.insert("", "end",
                            values=(item[0], item[1], item[2], item[3], item[4],
                                    item[5], item[6], item[7], "",
                                    item[9], item[10], item[11]),
                            image=photo_thumb if photo_thumb else "")  # Use empty string if no image

        # Function to search for a student by national code
        # Function to search for a student by national code (admin only)
        def searchStudent():

            national_code = ent_search_national_code.get()

            # Validate input
            if not national_code:
                showinfo('Error', 'Please enter a NationalCode to search.')
                return
            # Validate national code
            if not national_code.isdigit() or len(national_code) != 10:
                showinfo('Error', 'NationalCode must be 10 digits.')
                return

            try:
                # Fetch student data based on national code
                student_business_logic = StudentBusinessLogic()
                student_business_logic.getStudentListByNationalCode(national_code)

                self.GetData = student_business_logic.AllDataStudent

                if not self.GetData:
                    showinfo('Error', 'No student found with this NationalCode.')
                    return

                # Clear existing tree data
                for item in tree.get_children():
                    tree.delete(item)

                # Populate the tree view with the fetched student data
                for item in self.GetData:
                    photo_thumb = create_thumbnail_15x15(item[8]) if item[8] else None
                    tree.insert("", "end",
                                values=(item[0], item[1], item[2], item[3], item[4],
                                        item[5], item[6], item[7], "",
                                        item[9], item[10], item[11]),
                                image=photo_thumb)

            except Exception as e:
                showerror("Error", f"An error occurred during search: {str(e)}")

        # Function to generate a student identification card
        def generate_student_card():
            # Check if user is admin and has a selection
            if userparam.IsAdmin:
                selected_item = tree.focus()
                if not selected_item:
                    msg.showinfo("Error", "Please select a student from the list.")
                    return
                # Get data from selected item
                record = tree.item(selected_item)['values']
            else:
                # For non-admin, use current form data (assuming it's filled for the newly registered student)
                first_name = ent_first_name.get()
                last_name = ent_last_name.get()
                birthdate = ent_date_birthdate.get_date().strftime('%d/%m/%Y') if ent_date_birthdate.get_date() else ""
                national_code = ent_national_code.get()
                gender = "Male" if txt_gender.get() == "1" else "Female" if txt_gender.get() == "2" else ""
                mobile = ent_mobile.get()
                student_code = ent_student_code.get()
                photo_data = self.uploaded_photo  # Use uploaded photo
                if not all([first_name, last_name, birthdate, national_code, gender, mobile, student_code, photo_data]):
                    msg.showinfo("Error", "Please fill in all required fields and upload a photo to generate the card.")
                    return
                record = [None, first_name, last_name, birthdate, national_code, gender, None, mobile, photo_data, None,
                          student_code, None]
            # Create a new Toplevel window for the student card
            card_window = Toplevel()
            card_window.title("Student Identification Card")
            card_window.geometry("600x475")
            card_window.resizable(False, False)
            # Style the card window
            card_window.configure(bg='#f0f0f0')
            # Extract data from record
            first_name = record[1]
            last_name = record[2]
            birthdate = record[3]
            national_code = record[4]
            gender = record[5]
            mobile = record[7]
            student_code = record[10]
            photo_data = record[8]
            # Main card frame to hold all elements
            card_frame = Frame(card_window, bg='white', bd=2, relief='groove', padx=20, pady=20)
            card_frame.pack(pady=20, padx=20)
            # Card header
            header_frame = Frame(card_frame, bg='#1E90FF')
            header_frame.pack(fill='x', pady=(0, 20))
            # Title label for the card
            lbl_title = Label(header_frame,
                              text="STUDENT IDENTIFICATION CARD",
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
                    lbl_photo = Label(photo_frame, image=photo_img, bd=1, relief='solid')  # Create label for photo
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
                    lbl_photo = Label(photo_frame, text="No photo available", width=20, height=10)  # Placeholder
                    lbl_photo.pack()
            else:
                lbl_photo = Label(photo_frame, text="No photo available", width=20,
                                  height=10)  # Placeholder if no photo
                lbl_photo.pack()
            # Information frame (right side of the card)
            info_frame = Frame(content_frame)
            info_frame.pack(side='left', fill='both', expand=True)
            ### Student information labels
            # School name label
            lbl_school = Label(info_frame,
                               text="SEMATEC INSTITUTE",
                               font=('Arial', 14, 'bold'),
                               anchor='w')
            lbl_school.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky='w')

            # Function to create a row of student information
            def create_info_row(parent, row, label, value):
                lbl = Label(parent, text=label, font=('Arial', 10, 'bold'), anchor='w')  # Label for the field
                lbl.grid(row=row, column=0, sticky='w', pady=2)
                val = Label(parent, text=value, font=('Arial', 10), anchor='w')  # Label for the value
                val.grid(row=row, column=1, sticky='w', pady=2, padx=(10, 0))

            # Add student information to the card
            create_info_row(info_frame, 1, "Student ID:", student_code)
            create_info_row(info_frame, 2, "Full Name:", f"{first_name} {last_name}")
            create_info_row(info_frame, 3, "Date of Birth:", birthdate)
            create_info_row(info_frame, 4, "National Code:", national_code)
            create_info_row(info_frame, 5, "Gender:", gender)
            create_info_row(info_frame, 8, "Contact:", mobile)

            # Footer with student signature
            footer_frame = Frame(card_frame)
            footer_frame.pack(fill='x', pady=(20, 0))  # Fill horizontally with padding
            # Signature label
            lbl_signature = Label(footer_frame,
                                  text="SEMATEC INSTITUTE:No. 1,Corner of Fourth Alley,West Shahid Ghandi Street,North Sohrevardi,Tehran",
                                  font=('Arial', 8))
            lbl_signature.pack(anchor='w')
            # Placeholder for signature line
            signature_line = Canvas(footer_frame, width=200, height=2, bg='black')
            signature_line.pack(anchor='w', pady=(0, 10))
            # Button frame at the bottom of the card
            btn_frame = Frame(card_window)
            btn_frame.pack(pady=(10, 0))

            # Function to save the student card as an image
            def save_student_card():
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                    initialfile=f"student_card_{student_code}"
                )
                if file_path:
                    try:
                        # Create the card image to save
                        card_img = Image.new('RGB', (550, 450), 'white')  # Create a new white image
                        draw = ImageDraw.Draw(card_img)  # Create a drawing context
                        # Draw all elements on the card
                        if self.uploaded_photo:
                            student_photo = self.uploaded_photo.resize((150, 150),
                                                                       Image.LANCZOS)  # resize photo for card
                            card_img.paste(student_photo, (50, 115))  # paste photo onto card
                        # Draw blue header
                        draw.rectangle([(0, 0), (550, 80)], fill='#1E90FF')  # Blue rectangle for header
                        # Draw text on the card
                        font = ImageFont.truetype("arial.ttf", 23)  # Load font for title
                        draw.text((100, 25), "STUDENT IDENTIFICATION CARD", font=font, fill='black')
                        font = ImageFont.truetype("arial.ttf", 18)  # Load font for school name
                        draw.text((220, 90), "SEMATEC INSTITUTE", font=font, fill='black')
                        font = ImageFont.truetype("arial.ttf", 14)  # Load font for student info
                        info_y = 130  # Starting Y position for info
                        draw.text((220, info_y), f"Student ID: {student_code}", font=font, fill='black')
                        draw.text((220, info_y + 30), f"Full Name: {first_name} {last_name}", font=font, fill='black')
                        draw.text((220, info_y + 60), f"Date of Birth: {birthdate}", font=font, fill='black')
                        draw.text((220, info_y + 90), f"National Code: {national_code}", font=font, fill='black')
                        draw.text((220, info_y + 120), f"Gender: {gender}", font=font, fill='black')
                        draw.text((220, info_y + 150), f"Contact: {mobile}", font=font, fill='black')
                        # Add footer
                        card_width = 550
                        card_height = 450
                        footer_text_line1 = "SEMATEC INSTITUTE: No. 1, Corner of Fourth Alley,"
                        footer_text_line2 = "West Shahid Ghandi Street, North Sohrevardi, Tehran"
                        footer_y = card_height - 50  # Adjusted for two lines
                        # Draw footer rectangle
                        draw.rectangle([(0, footer_y - 10), (card_width, card_height)], fill='#1E90FF',
                                       outline='#1E90FF')
                        draw.text((card_width // 2, footer_y + 5), footer_text_line1, font=font, fill='white',
                                  anchor='mm')
                        draw.text((card_width // 2, footer_y + 25), footer_text_line2, font=font, fill='white',
                                  anchor='mm')
                        # Add validity date
                        valid_date = (datetime.now() + timedelta(days=365 * 2)).strftime("%d/%m/%Y")  # Validity date
                        draw.text((card_width - 150, footer_y - 25), f"Valid until: {valid_date}", font=font,
                                  fill='black')
                        # Add signature line
                        info_x = 115
                        draw.line([(info_x, footer_y - 30), (info_x + 200, footer_y - 30)], fill='black',
                                  width=2)  # signature line
                        draw.text((info_x + 100, footer_y - 15), "Authorized Signature", font=font, fill='black',
                                  anchor='mm')
                        # save the card Image
                        card_img.save(file_path)  # Save the image to the specified file path
                        msg.showinfo("Success", f"Student card saved as:\n{file_path}")
                    except Exception as e:
                        (
                            msg.showerror("Error", f"Failed to save card: {str(e)}"))

            # Buttons for saving and closing the card window
            btn_save = ttk.Button(btn_frame, text="Save Card", command=save_student_card)
            btn_save.pack(side='left', padx=5)
            btn_close = ttk.Button(btn_frame, text="Close", command=card_window.destroy)
            btn_close.pack(side='left', padx=5)
            # Auto-refresh the card window
            card_window.update()

        # Frame for the main student form
        frame = ctk.CTkFrame(student_form, width=320, height=300)#, fg_color='#73C2FB'
        # frame_label = ctk.CTkLabel(frame, text='Field...', font=('Arial', 12, 'bold'))
        # frame_label.grid(row=0, column=0, columnspan=4, pady=(10, 5), sticky='w')  # Use grid instead of pack; span 4 columns (adjust based on your layout)
        frame_button = ctk.CTkFrame(student_form, width=285, height=10)#, fg_color='#95C8D8'
        # frame_button_label = ctk.CTkLabel(frame_button, text='Operation...', font=('Arial', 12, 'bold'))
        # frame_button_label.grid(row=0, column=0, columnspan=6, pady=(10, 5), sticky='w')  # Span 6 columns for buttons
        frame_grid = ctk.CTkFrame(student_form, width=320, height=9)#, fg_color='#98CEEE'
        # frame_grid_label = ctk.CTkLabel(frame_grid, text='Data...', font=('Arial', 12, 'bold'))
        # frame_grid_label.grid(row=0, column=0, pady=(10, 5), sticky='w')  # Grid at top
        # Grid layout for frames (unchanged)
        frame.grid(row=0, column=0, padx=10,pady = 5 ,  sticky='nsew')
        frame_button.grid(row=1, column=0, padx=10,pady = 5,  sticky='nsew')
        frame_grid.grid(row=2, column=0, sticky='nsew', padx=10 , pady = 5 )

        style = ttk.Style()
        style.theme_use("default")  # Force default theme
        style.configure("Treeview", background="gray", rowheight=10)

        # Photo section - top left (shift to row=1)
        photo_container = ctk.CTkFrame(frame)
        photo_container.grid(row=1, column=0, padx=10, pady=10, sticky="nw")  # Changed row from 0 to 1

        photo_frame = ctk.CTkFrame(photo_container, width=105, height=105, border_width=3,
                                   border_color='green')#, fg_color='white',#3498db'
        photo_frame.pack_propagate(0)
        photo_frame.pack(side=ctk.LEFT)

        photo_label = ctk.CTkLabel(photo_frame, text="", width=100, height=100)#, fg_color='white'
        photo_label.pack(side=ctk.LEFT)

        btn_UploadPhoto = ctk.CTkButton(frame, text='Upload Photo', command=upload_photo)
        btn_UploadPhoto.grid(row=1, column=1, padx=10, pady=40, sticky='nw')  # Changed row from 0 to 1

        # ========== ACTIVATE VALIDATION FUNCTIONS ==========
        # Register validation functions
        vcmd_national_code = (student_form.register(validate_national_code), '%P')
        vcmd_mobile = (student_form.register(validate_mobile), '%P')
        vcmd_20 = (student_form.register(validate20), '%P')
        vcmd_30 = (student_form.register(validate30), '%P')
        vcmd_40 = (student_form.register(validate40), '%P')


        # Label: FirstName (shift to row=2)
        lbl_first_name = ctk.CTkLabel(frame, text='FirstName: ')#, fg_color='#73C2FB'
        lbl_first_name.grid(row=2, column=0, padx=10, pady=5, sticky='w')  # Changed row from 1 to 2
        ent_first_name = ctk.CTkEntry(frame, width=200, placeholder_text="Enter first name")
        ent_first_name.configure(validate='key', validatecommand=vcmd_20)
        ent_first_name.grid(row=2, column=1, padx=10, pady=5, sticky='e')  # Changed row from 1 to 2

        # Label: LastName (shift to row=2)
        lbl_last_name = ctk.CTkLabel(frame, text='LastName: ')#, fg_color='#73C2FB'
        lbl_last_name.grid(row=2, column=2, padx=10, pady=5, sticky='w')  # Changed row from 1 to 2
        ent_last_name = ctk.CTkEntry(frame, width=200, placeholder_text="Enter last name")
        ent_last_name.configure(validate='key', validatecommand=vcmd_30)
        ent_last_name.grid(row=2, column=3, padx=10, pady=5, sticky='e')  # Changed row from 1 to 2

        # Label: Birthdate (shift to row=3)
        lbl_birthdate = ctk.CTkLabel(frame, text='Birthdate: (dd/mm/yyyy) ')#, fg_color='#73C2FB'
        lbl_birthdate.grid(row=3, column=0, padx=10, pady=5, sticky='w')  # Changed row from 2 to 3
        date_frame = ctk.CTkFrame(frame)#, fg_color='#73C2FB'
        date_frame.grid(row=3, column=1, padx=10, pady=5, sticky='e')  # Changed row from 2 to 3
        ent_date_birthdate = DateEntry(date_frame, width=26, date_pattern='dd/mm/yyyy')
        ent_date_birthdate.pack()

        # Label: NationalCode (shift to row=3)
        lbl_national_code = ctk.CTkLabel(frame, text='NationalCode: ')#, fg_color='#73C2FB'
        lbl_national_code.grid(row=3, column=2, padx=10, pady=5, sticky='w')  # Changed row from 2 to 3
        ent_national_code = ctk.CTkEntry(frame, width=200, placeholder_text="Enter 10-digit code")
        ent_national_code.configure(validate='key', validatecommand=vcmd_national_code)
        ent_national_code.grid(row=3, column=3, padx=10, pady=5, sticky='e')  # Changed row from 2 to 3

        # Label: Gender (shift to row=4)
        lbl_gender = ctk.CTkLabel(frame, text='Gender: ' )## fg_color='#73C2FB'v, text_color="black"
        lbl_gender.grid(row=4, column=0, padx=10, pady=5, sticky='w')  # Changed row from 3 to 4
        txt_gender = ctk.StringVar()
        rb_gender_male = ctk.CTkRadioButton(frame, text='Male', variable=txt_gender, value='1')# fg_color='#73C2FB'v, text_color="black"
        rb_gender_male.grid(row=4, column=1, padx=10, pady=5, sticky='w')  # Changed row from 3 to 4
        rb_gender_female = ctk.CTkRadioButton(frame, text='Female', variable=txt_gender, value='2')# fg_color='#73C2FB'v, text_color="black"
        rb_gender_female.grid(row=4, column=1, padx=10, pady=5, sticky='e')  # Changed row from 3 to 4

        # Label: Address (shift to row=4)
        lbl_address = ctk.CTkLabel(frame, text='Address: ')#, fg_color='#73C2FB'
        lbl_address.grid(row=4, column=2, padx=10, pady=5, sticky='w')  # Changed row from 3 to 4
        ent_address = ctk.CTkEntry(frame, width=200, placeholder_text="Enter address")
        ent_address.configure(validate='key', validatecommand=vcmd_40)
        ent_address.grid(row=4, column=3, padx=10, pady=5, sticky='e')  # Changed row from 3 to 4

        # Label: Mobile (shift to row=5)
        lbl_mobile = ctk.CTkLabel(frame, text='Mobile: ')#, fg_color='#73C2FB'
        lbl_mobile.grid(row=5, column=0, padx=10, pady=5, sticky='w')  # Changed row from 4 to 5
        ent_mobile = ctk.CTkEntry(frame, width=200, placeholder_text="Enter 11-digit mobile")
        ent_mobile.configure(validate='key', validatecommand=vcmd_mobile)
        ent_mobile.grid(row=5, column=1, padx=10, pady=5, sticky='e')  # Changed row from 4 to 5

        # Label: EducationID (shift to row=5)
        lbl_education_id = ctk.CTkLabel(frame, text='Select EducationID: ')#, fg_color='#73C2FB'
        lbl_education_id.grid(row=5, column=2, padx=10, pady=5, sticky='w')
        comb_education_id = ctk.CTkComboBox(frame, width=200, values=[])
        comb_education_id.grid(row=5, column=3, padx=10, pady=5, sticky='e')
        education_levels = self.fetchEducationLevels()
        comb_education_id.configure(values=[f"{level[0]} - {level[1]}" for level in education_levels])
        comb_education_id.set("Select EducationID")  # Set default text to "Select EducationID?

        # Label: StudentCode (shift to row=6)
        lbl_student_code = ctk.CTkLabel(frame, text='StudentCode')#, fg_color='#73C2FB'
        lbl_student_code.grid(row=6, column=0, padx=10, pady=5, sticky='w')  # Changed row from 5 to 6
        ent_student_code = ctk.CTkEntry(frame, width=200, placeholder_text="Enter student code")
        # ent_student_code.configure(validate='key', validatecommand=vcmd_20)  # Assuming studedentCode
        ent_student_code.grid(row=6, column=1, padx=10, pady=5, sticky='e')  # Changed row from 5 to 6

        # Label: Job (shift to row=6)
        lbl_job = ctk.CTkLabel(frame, text='Job: ')#, fg_color='#73C2FB'
        lbl_job.grid(row=6, column=2, padx=10, pady=5, sticky='w')  # Changed row from 5 to 6
        ent_job = ctk.CTkEntry(frame, width=200, placeholder_text="Enter job")
        ent_job.configure(validate='key', validatecommand=vcmd_20)  # Job field validation
        ent_job.grid(row=6, column=3, padx=10, pady=5, sticky='e')  # Changed row from 5 to 6


        #CTkComboBox

        # Buttons (shift to row=1)
        btn_clear_student = ctk.CTkButton(frame_button, text='Clear', command=clearText, width=150)
        btn_clear_student.grid(row=1, column=0, padx=20, pady=3, sticky='w')  # Changed row from 7 to 1

        btn_select_all = ctk.CTkButton(frame_button, text='Select All', command=selectAllStudents, width=150)
        btn_select_all.grid(row=1, column=1, padx=20, pady=3, sticky='w')  # Changed row from 7 to 1

        btn_insert_student = ctk.CTkButton(frame_button, text='Insert', command=registerStudent, width=150)
        btn_insert_student.grid(row=1, column=2, padx=20, pady=3, sticky='w')  # Changed row from 7 to 1

        btn_update_student = ctk.CTkButton(frame_button, text='Update', command=updateStudent, width=150)
        btn_update_student.grid(row=1, column=3, padx=15, pady=3, sticky='w')  # Changed row from 7 to 1

        btn_delete_student = ctk.CTkButton(frame_button, text='Delete', command=deleteStudent, width=150)
        btn_delete_student.grid(row=3, column=0, padx=20, pady=3, sticky='w')  # Changed row from 7 to 1

        btn_backToMain_student = ctk.CTkButton(frame_button, text='BackToMain', command=destroyForm, width=150)
        btn_backToMain_student.grid(row=3, column=3, padx=15, pady=3, sticky='w')  # Changed row from 7 to 1


        lbl_search_national_code = ctk.CTkLabel(frame_button, text='Search By NationalCode: ')#, fg_color='#95C8D8'
        lbl_search_national_code.grid(row=2, column=0, padx=20, pady=3, sticky='w')  # Changed row from 8 to 2
        ent_search_national_code = ctk.CTkEntry(frame_button, width=150, placeholder_text="Enter code")
        ent_search_national_code.grid(row=2, column=1, padx=20, pady=3, sticky='e')  # Changed row from 8 to 2
        btn_search_student = ctk.CTkButton(frame_button, text='Search', command=searchStudent, width=150)
        btn_search_student.grid(row=2, column=2, padx=20, pady=3, sticky='w')  # Changed row from 8 to 2

        btn_generate_card = ctk.CTkButton(frame_button, text='Generate Student Card', command=generate_student_card,
                                          width=150)
        btn_generate_card.grid(row=2, column=3, padx=15, pady=3, sticky='w')  # Changed row from 8 to 2

        btn_export_excel = ctk.CTkButton(frame_button, text='Export to Excel', command=export_to_excel, width=150)
        btn_export_excel.grid(row=3, column=1, padx=20, pady=3, sticky='w')  # Placed next to btn_delete_student

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
        # frameGrid
        columns = ('person_id', 'first_name', 'last_name', 'birthdate', 'national_code', 'gender', 'address', 'mobile',
                   'photo', 'education_id', 'student_code', 'job')
        tree = ttk.Treeview(frame_grid, columns=columns, show='headings')
        # Set up headings for the Treeview
        tree.heading('person_id', text='PersonID', anchor='w')
        tree.heading('first_name', text='FirstName', anchor='w')
        tree.heading('last_name', text='LastName', anchor='w')
        tree.heading('birthdate', text='BirthDate', anchor='w')
        tree.heading('national_code', text='NationalCode', anchor='w')
        tree.heading('gender', text='Gender', anchor='w')
        tree.heading('address', text='Address', anchor='w')
        tree.heading('mobile', text='Mobile', anchor='w')
        tree.heading('photo', text='Photo', anchor='w')
        tree.heading('education_id', text='EducationID', anchor='w')
        tree.heading('student_code', text='StudentCode', anchor='w')
        tree.heading('job', text='Job', anchor='w')

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
            studentBusinessLogic = StudentBusinessLogic()
            studentBusinessLogic.getStudentList(userparam.IsAdmin)  # PersonID
            self.GetData = studentBusinessLogic.AllDataStudent

            for item in self.GetData:
                photo_thumb = create_thumbnail_15x15(item[8])
                if photo_thumb:
                    self.photo_cache[item[0]] = photo_thumb
                    tree.insert("", "end",
                                values=(item[0], item[1], item[2], item[3], item[4],
                                        item[5], item[6], item[7], "",
                                        item[9], item[10], item[11]),
                                image=photo_thumb)
                else:
                    tree.insert("", "end",
                                values=(item[0], item[1], item[2], item[3], item[4],
                                        item[5], item[6], item[7], "No Photo",
                                        item[9], item[10], item[11]))

        def item_selected(event):
            # Get the selected item from the tree
            selected_item = tree.focus()
            if not selected_item:  # If nothing is selected, exit
                return

            item = tree.item(selected_item)
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
            ent_national_code.delete(0, END)
            ent_national_code.insert(0, record[4])
            # Set the gender radio button
            if record[5] == "Male":  # Check if the gender is "Male"
                txt_gender.set(1)  # Set to 1 for Male
            elif record[5] == "Female":  # Check if the gender is "Female"
                txt_gender.set(2)  # Set to 2 for Female
            else:
                txt_gender.set(0)  # Clear selection if gender is not recognized
            ent_address.delete(0, END)
            ent_address.insert(0, record[6])
            ent_mobile.delete(0, END)
            ent_mobile.insert(0, record[7])
            comb_education_id.set(record[9])  # Set the selected value for the combobox
            ent_student_code.delete(0, END)
            ent_student_code.insert(0, record[10])
            ent_job.delete(0, END)
            ent_job.insert(0, record[11])

            # ========== PHOTO HANDLING SECTION ==========
            # Handle photo display
            photo_data = next((x[8] for x in self.GetData if x[0] == record[0]), None)

            # Clear current photo
            photo_label.configure(image=None)  # Changed from config(image='') to configure(image=None)
            photo_label.image = None

            # Display new photo if exists
            if photo_data:
                try:
                    pil_img = Image.open(io.BytesIO(photo_data))
                    pil_img = pil_img.resize((100, 100), Image.LANCZOS)
                    tk_img = CTkImage(pil_img, size=(100, 100))  # Use CTkImage instead of ImageTk.PhotoImage

                    photo_label.configure(image=tk_img)  # Changed from config to configure
                    photo_label.image = tk_img  # Keep reference
                except Exception as e:
                    print(f"Error displaying photo: {e}")  # This print can be removed if you want to suppress it

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
        treeXScroll = ttk.Scrollbar(frame_grid, orient=HORIZONTAL)  # Use ctk constants if needed
        treeXScroll.configure(command=tree.xview)
        tree.configure(xscrollcommand=treeXScroll.set)
        treeXScroll.grid(column=0, row=2, columnspan=3, sticky='we')
        #
        #
        # Configure grid weights
        student_form.columnconfigure(0, weight=1)
        student_form.rowconfigure(0, weight=1)
        frame_grid.columnconfigure(0, weight=3)
        frame_grid.columnconfigure(1, weight=3)
        frame_grid.columnconfigure(2, weight=3)
        frame_grid.columnconfigure(3, weight=1)
        frame_grid.columnconfigure(4, weight=1)
        frame_grid.rowconfigure(1, weight=1)

        # Access control for non-admin users
        if not userparam.IsAdmin:
            # Disable admin-only buttons
            btn_update_student.configure(state='disabled')
            btn_delete_student.configure(state='disabled')
            btn_select_all.configure(state='disabled')
            btn_search_student.configure(state='disabled')
            btn_export_excel.configure(state='disabled')  # Disable export for non-admins
            # btn_generate_card.configure(state= 'disabled')

            # Hide search-related widgets
            lbl_search_national_code.grid_forget()
            ent_search_national_code.grid_forget()

            # Optionally hide the data grid (treeview) to avoid showing an empty table
            frame_grid.grid_forget()

            # Note: btn_clear_student, btn_insert_student,btn_generate_card and btn_backToMain_student remain enabled

        student_form.mainloop()













