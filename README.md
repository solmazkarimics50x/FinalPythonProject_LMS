# 🎓 Learning Management System (LMS) - Final Python Project

[![Python](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green.svg)](https://customtkinter.tomschimansky.com/)
[![SQL Server](https://img.shields.io/badge/Database-SQL%20Server-red.svg)](https://www.microsoft.com/en-us/sql-server/)

> **A Comprehensive Desktop Learning Management System for Educational Institutions**
>

## 📖 Overview

This is a **desktop Learning Management System** for educational institutions to manage students, teachers, employees, courses, departments, and scores. The project follows a **multi-layer architecture** and was developed as the final project of the Python Data Science course under the supervision of **Mr.Vahid Ghorbani**.

---

## ✨ Key Features

- 🔐 **Secure Login** with Admin / NonAdmin roles  
- 📊 **Full CRUD** for Students, Teachers, Employees, Courses, Departments, and Scores  
- 🪪 **ID Card Generator** for students, teachers, and employees (PNG output)  
- 📁 **Photo Upload** and display for all entities  
- 📤 **Excel Export** for student, teacher, and employee data  
- 🔍 **Search** by national code and other fields  
- 🔗 **Relationship Management** (course prerequisites, hierarchical org structures)  
- 🖥️ **Standalone .exe** file for easy distribution  

---

## 🏗️ Architecture

│ Presentation Layer (GUI) │ ← CustomTkinter / Tkinter

│ Business Logic Layer │ ← Business Rules & Validation

│ Data Access Layer │ ← Database Communication

│
▼

│ Database Layer │
│ SQL Server │


---

---

## 💻 Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.13+ |
| GUI | CustomTkinter, Tkinter |
| Database | SQL Server |
| DB Connection | pyodbc |
| Images | Pillow (PIL) |
| Excel Export | openpyxl |
| Packaging | PyInstaller |

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/solmazkarimics50x/FinalProjectPython_LMS.git
cd FinalProjectPython_LMS

# Install dependencies
pip install -r requirements.txt

# Run the application
python LoginModule.py
```
## 🖥️ Executable File

A pre-built .exe file is available at:
```bash
PythonProjectSolmazwithAdminNonAdmin/output/SematecLMS.exe
```
## Requirements to run the EXE:
- Windows 10
- SQL Server 2019 installed
- ODBC Driver for SQL Server

---


## 👥 User Roles

| Role | Access Level | Permissions |
|------|--------------|-------------|
| **Admin** | 🔓 Full Access | • View, add, edit, and delete all records<br>• Manage users<br>• Access to all system functions<br>• Generate reports and exports |
| **NonAdmin** | 🔒 Limited Access | • Add new records (Students, Teachers, Employees)<br>• Generate ID cards<br>• Search and view data |

---
## 📁 Project Structure
```bash
FinalProjectPython_SolmazKarimi/
├── BusinessLogicLayer/          # Business Logic Layer
│   ├── StudentBusinessLogic.py
│   ├── TeacherBusinessLogic.py
│   └── ...
├── DataAccessLayer/              # Data Access Layer
│   ├── StudentDataAccess.py
│   ├── TeacherDataAccess.py
│   └── ...
├── Model/                        # Data Models
│   ├── UserModel.py
│   ├── StudentModel.py
│   └── ...
├── UserInterfaceLayer/           # User Interface Layer
│   ├── LoginModule.py
│   ├── MainFormModule.py
│   ├── StudentFormModule.py
│   └── ...
├── DB/                           # Database
│   └── sematec_db.db
├── images/                       # Application Images
│   ├── output/                   # Output folder
│   │   └── SematecLMS.exe       # ✅ Executable file
│   ├── logo.png
│   └── ...
├── ExcelFiles/                   # Excel Output Files
├── SyllabusFiles/                # Syllabus Files
├── output/                       # Application Outputs
├── requirements.txt              # Project Dependencies
└── README.md                     # Project Documentation
```
## 🎥 Video Tutorial
[![Learning Management System - Desktop App with CustomTkinter & SQL](https://img.youtube.com/vi/Mrce1hDpajo/0.jpg)](https://youtu.be/Mrce1hDpajo)

---
## 👨‍🏫 Acknowledgments
Special thanks to Mr. Vahid Ghorbani for his guidance and support.
---
## 📧 Contact
- Developer: Solmaz Karimi
- GitHub: @solmazkarimics50x


