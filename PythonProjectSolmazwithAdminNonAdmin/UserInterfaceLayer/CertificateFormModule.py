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

from BusinessLogicLayer.CertificateBusinessLogic import CertificateBusinessLogic
from Model.UserModule import UserModel
from Model.CertificateModel import Certificate,CertificateIdDelete


#
class CertificateFormClass:
    # Initialize the JobFormClass with user and main form references
    def __init__(self,userparam : UserModel, main_form, switch_indication_func=None, home_indicator=None):
        self.User = userparam
        self.main_form = main_form  # Store the reference to main_form
        self.switch_indication = switch_indication_func  # Store the function
        self.home_btn_indicator = home_indicator  # Store the indicator
        self.GetData = []
        self.DeleteID = 0
        self.UpdateID = 0
        self.SearchID = 0


    # Load the certificate form
    def certificate_form_load(self,userparam : UserModel):
        ctk.set_appearance_mode("Dark")  # Set appearance mode (optional, for modern look)
        ctk.set_default_color_theme("green")  # Set default color theme (optional)
        certificate_form = ctk.CTkToplevel(self.main_form)
        # certificate_form = ctk.CTk()
        certificate_form.title('CertificateForm...')
        certificate_form.resizable(0, 0) # Disable resizing of the window
        certificate_form.geometry('850x360')   # Set the window size
        x = int(certificate_form.winfo_screenwidth() / 2 - 850 / 2)
        y = int(certificate_form.winfo_screenheight() / 2 - 360 / 2)
        certificate_form.geometry('+{}+{}'.format(x, y))
        certificate_form.iconbitmap('images/ImagesCertificateForm/Certificate.ico')  # Set the window icon

        # Function to close the job form and show the main form
        def destroyForm():
            certificate_form.withdraw()  # Close the certificate form
            self.main_form.deiconify()  # Show the main form FIRST
            self.main_form.update()  # Force a UI refresh to ensure changes are visible
            if self.switch_indication and self.home_btn_indicator:  # Check if home indicator is available (fixed condition)
                self.switch_indication(
                    indicator_lb=self.home_btn_indicator)  # Activate home indicator AFTER showing the form
                self.main_form.update()  # Force another UI refresh to ensure the indicator change is visible

        # Function to clear all input fields
        def clearText():
            ent_certificate_title.delete(0, END)
            ent_vendor.delete(0, END)

        # Validation functions for input fields
        def validate100(value):
            return len(value) <= 100
        def validate50(value):
            return len(value) <= 50

        # Function to register a new job
        def registerCertificate():

            # Gather data from the input fields
            certificateTitle = ent_certificate_title.get()
            vendor_value = ent_vendor.get()


            # CertificateTitle validation
            if not certificateTitle :
                showinfo('Error', 'Please enter the certificate\'s title')
                certificate_form.focus_force()
                return False

            # vendor_value validation
            if not vendor_value :
                showinfo('Error', 'Please enter the certificate\'s vendor')
                certificate_form.focus_force()
                return False

            # Create a new Certificate object
            new_certificate = Certificate(certificate_title=certificateTitle, vendor = vendor_value)
            # Insert the certificate into the database
            certificate_business_logic = CertificateBusinessLogic(new_certificate)
            certificate_id = certificate_business_logic.insertCertificate()  # Get the new certificate ID
            if certificate_id:  # Check if the certificate was inserted successfully
                showinfo('Success', 'Certificate registered successfully')
                certificate_form.focus_force()
                # Clear the tree view
                for item in tree.get_children():
                    tree.delete(item)
                # Insert the new certificate into the tree view
                tree.insert("", 'end', values=(certificate_id, certificateTitle,vendor_value))  # Insert the new certificate directly into the tree
                clearText()  # Clear the input fields
            else:
                showerror('Error', 'Failed to register certificate. Please try again.')

        def updateCertificate():
            certificateTitle = ent_certificate_title.get()
            vendor_value = ent_vendor.get()

            # CertificateTitle validation
            if not certificateTitle :
                showinfo('Error', 'Please enter the certificate\'s title')
                certificate_form.focus_force()
                return False
            # vendor_value validation
            if not vendor_value :
                showinfo('Error', 'Please enter the certificate\'s vendor')
                certificate_form.focus_force()
                return False

            # Create a Certificate object with the updated title
            certificateObject = Certificate(certificate_id=self.UpdateID,
                                            certificate_title=certificateTitle,
                                            vendor = vendor_value)
            certificateBusinessLogic = CertificateBusinessLogic(certificateObject)
            # Update the certificate in the database
            certificateBusinessLogic.updateCertificate(self.UpdateID)
            showinfo('Success', 'Certificate updated successfully.')
            certificate_form.focus_force()

            # Clear the tree view
            for item in tree.get_children():
                tree.delete(item)
            # Insert the updated certificate directly into the tree view
            tree.insert("", 'end', values=(self.UpdateID, certificateTitle, vendor_value))  # Insert the updated certificate
            clearText()  # Clear the input fields

        # Function to delete a selected certificate
        def deleteCertificate():
            certificateObject = CertificateIdDelete(certificate_id=self.DeleteID)
            certificateBusinessLogic = CertificateBusinessLogic(certificateObject)
            certificateBusinessLogic.deleteCertificate(self.DeleteID)
            showinfo('Success', 'Certificate deleted successfully.')
            certificate_form.focus_force()
            for i in tree.get_children():
                tree.delete(i)
            certificateBusinessLogic = CertificateBusinessLogic()
            certificateBusinessLogic.getCertificateList()
            self.GetData = certificateBusinessLogic.AllDataCertificate

            for item in self.GetData:
                tree.insert("", 'end', values=item)
            clearText()

        # Function to select all Certificates and populate the tree view
        def selectAllCertificates():
            # Clear existing tree data
            for item in tree.get_children():
                tree.delete(item)

            # Fetch all certificates from database
            certificateBL = CertificateBusinessLogic()
            certificateBL.getAllCertificates()  # Fetch all certificates
            self.GetData = certificateBL.AllDataCertificate

            # Insert all records into treeview
            for item in self.GetData:
                tree.insert("", "end",values=(item[0], item[1],item[2]))



        # endregion
        frame = ctk.CTkFrame(certificate_form, width=750, height=150)
        frame_button = ctk.CTkFrame(certificate_form, width=750, height=80)
        frame_grid = ctk.CTkFrame(certificate_form, width=750, height=90)

        frame.grid(row=0, column=0, padx=10,sticky='nsew')
        frame_button.grid(row=1, column=0, padx=10,sticky='nsew')
        frame_grid.grid(row=2, column=0, padx=10,sticky='nsew')

        vcmd_50 = (certificate_form.register(validate50), '%P')
        vcmd_100 = (certificate_form.register(validate100), '%P')

        # Label : CertificateTitle
        lbl_certificate_title = ctk.CTkLabel(frame, text='Certificate Title: ')
        lbl_certificate_title.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        ent_certificate_title = ctk.CTkEntry(frame, width=300)
        ent_certificate_title.configure(validate="key",
                                        validatecommand=vcmd_100)
        ent_certificate_title.grid(row=0, column=1, padx=10, pady=10, sticky='e')
        # Label : Vendor
        lbl_vendor = ctk.CTkLabel(frame, text='Vendor: ')
        lbl_vendor.grid(row=0, column=2, padx=10, pady=10, sticky='w')
        ent_vendor = ctk.CTkEntry(frame, width=300)
        ent_vendor.configure(validate="key", validatecommand=vcmd_50)
        ent_vendor.grid(row=0, column=3, padx=10, pady=10, sticky='e')

        # frameButton : clearCertificate
        btn_clear_certificate = ctk.CTkButton(frame_button, text='Clear', command=clearText, width=120)
        btn_clear_certificate.grid(row=7, column=0, padx=10, pady=10, sticky='w')
        #
        btn_select_all = ctk.CTkButton(frame_button, text='Select All', command=selectAllCertificates, width=120)
        btn_select_all.grid(row=7, column=1, padx=10, pady=10, sticky='w')
        # frameButton : insertCertificate
        btn_insert_certificate = ctk.CTkButton(frame_button, text='Insert', command=registerCertificate, width=120)
        btn_insert_certificate.grid(row=7, column=2, padx=10, pady=10, sticky='e')
        #
        # frameButton : updateCertificate
        btn_update_certificate = ctk.CTkButton(frame_button, text='Update', command=updateCertificate, width=120)
        btn_update_certificate.grid(row=7, column=3, padx=10, pady=10, sticky='w')
        # certificate
        # frameButton : deleteCertificate
        btn_delete_certificate = ctk.CTkButton(frame_button, text='Delete', command=deleteCertificate, width=120)
        btn_delete_certificate.grid(row=7, column=4, padx=10, pady=10, sticky='w')
        #
        # frameButton : closeCertificate
        btn_backToMain_certificate = ctk.CTkButton(frame_button, text='BackToMain', command=destroyForm, width=120)
        btn_backToMain_certificate.grid(row=7, column=5, padx=10, pady=10, sticky='w')
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

        columns = ("certificate_id","certificate_title","vendor")
        tree = ttk.Treeview(frame_grid, columns=columns, show='headings')

        tree.heading("certificate_id", text="CertificateID", anchor=W)
        tree.heading("certificate_title", text="CertificateTitle", anchor=W)
        tree.heading("vendor", text="Vendor", anchor=W)

        # Set column widths
        tree.column("certificate_id", width=120, minwidth=120, stretch=NO)
        tree.column("certificate_title", width=500, minwidth=500, stretch=NO)
        tree.column("vendor", width=150, minwidth=150, stretch=NO)


        for item in self.GetData:
            tree.insert("", 'end', values=item)

        def item_selected(event):
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                record = item['values']

                ent_certificate_title.delete(0, END)
                ent_certificate_title.insert(0, record[1])  ## Set the certificate title in the entry field

                ent_vendor.delete(0, END)
                ent_vendor.insert(0,record[2])


                self.DeleteID = record[0]  ## Store the Certificate ID for deletion
                self.UpdateID = record[0]  ## Store the Certificate ID for updating

        tree.bind('<<TreeviewSelect>>', item_selected)

        tree.grid(row=0, column=0, sticky='nsew')
        treeYScroll = ttk.Scrollbar(frame_grid, orient=VERTICAL)
        treeXScroll = ttk.Scrollbar(frame_grid, orient=HORIZONTAL)
        treeXScroll.configure(command=tree.xview)



        frame_grid.grid(column=0, row=3, sticky=(N, S, E, W))
        tree.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
        treeXScroll.grid(column=0, row=2, columnspan=3, sticky=W + E)

        certificate_form.columnconfigure(0, weight=1)
        certificate_form.rowconfigure(0, weight=1)
        frame_grid.columnconfigure(0, weight=3)
        frame_grid.columnconfigure(1, weight=3)
        frame_grid.columnconfigure(2, weight=3)
        frame_grid.columnconfigure(3, weight=1)
        frame_grid.columnconfigure(4, weight=1)
        frame_grid.rowconfigure(1, weight=1)

        certificate_form.mainloop()