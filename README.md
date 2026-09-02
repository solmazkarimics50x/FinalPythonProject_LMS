# 🎓 Learning Management System (LMS)

[![GitHub stars](https://img.shields.io/github/stars/solmazkarimics50x/FinalPythonProject_LMS.svg?style=social&label=Star&maxAge=2592000)](https://github.com/solmazkarimics50x/FinalPythonProject_LMS)


[![Python](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green.svg)](https://customtkinter.tomschimansky.com/)
[![SQL Server](https://img.shields.io/badge/Database-SQL%20Server-red.svg)](https://www.microsoft.com/en-us/sql-server/)
[![Platform](https://img.shields.io/badge/Platform-Windows_10-yellow.svg)](https://www.microsoft.com/windows/)

---
## 🎯 Project Overview
**A Comprehensive Desktop Learning Management System for Educational Institutions**

This desktop application is designed to help educational institutions manage their courses, students, instructors, and grades efficiently. Built with Python and CustomTkinter, it provides a modern and user-friendly interface for administrators, teachers, and students.

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

## 🖥️ Executable File
A pre-built .exe file is available at:
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

> **👆 Click on the image above to watch the complete project demo video.**

---
## 🗄️ Database Setup

The database is managed as a **Visual Studio SQL Server Project**. All scripts are in the `Backup_ScriptsDatabase_Project` folder.

### 📁 Scripts Overview

| Folder/File | Contents |
|-------------|----------|
| **dbo/Tables/** | Table creation scripts (Students, Teachers, Courses, etc.) |
| **dbo/Stored Procedures/** | CRUD operations (Insert, Update, Delete, Select) |
| **DatabaseDiagrams.sql** | Entity-Relationship diagram |
| **DS_1403_09_SK_Project.sqlproj** | Visual Studio project file |

### 🚀 Quick Setup

1. **Open** `DS_1403_09_SK_Project.sqlproj` in Visual Studio
2. **Build** and **Publish** to your SQL Server
3. **Or** run scripts manually in SSMS:
   - First: `dbo/Tables/*.sql`
   - Second: `dbo/Stored Procedures/*.sql`
   - Optional: `DatabaseDiagrams.sql`

### 🔗 Connection Configuration

The database connection is managed in `DataAccessLayer/ConnectionString.py`.  
To connect to your SQL Server, update the following variables:

```python
# ConnectionString.py

Driver = 'SQL Server'  # ODBC driver name
Server = 'YOUR_SERVER_NAME'  # e.g., 'localhost' or 'DESKTOP-XXX'
Database = 'DS_1403_09_SK'   # Database name
Username = 'YOUR_USERNAME'   # e.g., 'sa'
Password = 'YOUR_PASSWORD'   # Your SQL Server password
```

---
## 👨‍🏫 Acknowledgments
Special thanks to Mr. Vahid Ghorbani for his guidance and support.
---
## 📧 Contact
- Developer: Solmaz Karimi
- GitHub: @solmazkarimics50x


