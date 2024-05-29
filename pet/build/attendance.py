import tkinter as tk
from tkinter import messagebox, Canvas
import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="student_attendance_system"
)

cursor = db.cursor()

# Initialize the Tkinter root window
root = tk.Tk()
root.title("Student Attendance System")
root.geometry("800x600")

student_vars = []

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=MD5(%s)", (username, password))
    user = cursor.fetchone()
    if user:
        if user[3] == 'teacher':
            show_teacher_dashboard()
        else:
            show_student_dashboard(username)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Function to display the login screen
def show_login():
    clear_screen()
    
    # Add a canvas to draw shapes (rectangle, line)
    canvas = Canvas(root)
    canvas.pack(fill="both", expand=True)
    
    # Create rectangle and line as per Figma design
    canvas.create_rectangle(100, 50, 700, 150, fill="lightblue")
    canvas.create_line(100, 150, 700, 150)
    
    tk.Label(root, text="Login", font=("Arial", 24)).pack(pady=20)
    tk.Label(root, text="Username").pack(pady=5)
    global username_entry
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)
    tk.Label(root, text="Password").pack(pady=5)
    global password_entry
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)
    
    login_button = tk.Button(root, text="Login", command=login)
    login_button.pack(pady=20)
    
    def on_enter(event):
        login_button['background'] = 'yellow'
    def on_leave(event):
        login_button['background'] = 'SystemButtonFace'
    
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)

# Function to display the teacher dashboard
def show_teacher_dashboard():
    clear_screen()
    tk.Label(root, text="Teacher Dashboard", font=("Arial", 24)).pack(pady=20)
    tk.Button(root, text="Add Student", command=show_add_student_form).pack(pady=10)

    cursor.execute("SELECT * FROM students")
    for student in cursor.fetchall():
        frame = tk.Frame(root)
        frame.pack(pady=5)
        tk.Label(frame, text=student[1]).pack(side=tk.LEFT, padx=10)
        present_var = tk.IntVar()
        absent_var = tk.IntVar()
        tk.Checkbutton(frame, text="Present", variable=present_var).pack(side=tk.LEFT)
        tk.Checkbutton(frame, text="Absent", variable=absent_var).pack(side=tk.LEFT)
        tk.Button(frame, text="Edit", command=lambda s=student: show_edit_student_form(s)).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Delete", command=lambda s=student: delete_student(s)).pack(side=tk.LEFT, padx=5)
        student_vars.append({'id': student[0], 'present': present_var, 'absent': absent_var})

    tk.Button(root, text="Submit Attendance", command=submit_attendance).pack(pady=20)

# Function to display the add student form
def show_add_student_form():
    clear_screen()
    tk.Label(root, text="Add Student", font=("Arial", 24)).pack(pady=20)
    tk.Label(root, text="Name").pack(pady=5)
    new_student_name_entry = tk.Entry(root)
    new_student_name_entry.pack(pady=5)
    tk.Button(root, text="Add", command=lambda: add_student(new_student_name_entry.get())).pack(pady=10)
    tk.Button(root, text="Back", command=show_teacher_dashboard).pack(pady=10)

# Function to add a new student
def add_student(name):
    if name:
        cursor.execute("INSERT INTO students (name) VALUES (%s)", (name,))
        db.commit()
        messagebox.showinfo("Success", "Student added successfully")
        show_teacher_dashboard()
    else:
        messagebox.showerror("Error", "Name cannot be empty")

# Function to display the edit student form
def show_edit_student_form(student):
    clear_screen()
    tk.Label(root, text="Edit Student", font=("Arial", 24)).pack(pady=20)
    tk.Label(root, text="Name").pack(pady=5)
    edit_student_name_entry = tk.Entry(root)
    edit_student_name_entry.insert(0, student[1])
    edit_student_name_entry.pack(pady=5)
    tk.Button(root, text="Update", command=lambda: update_student(student[0], edit_student_name_entry.get())).pack(pady=10)
    tk.Button(root, text="Back", command=show_teacher_dashboard).pack(pady=10)

# Function to update a student
def update_student(student_id, new_name):
    if new_name:
        cursor.execute("UPDATE students SET name=%s WHERE id=%s", (new_name, student_id))
        db.commit()
        messagebox.showinfo("Success", "Student updated successfully")
        show_teacher_dashboard()
    else:
        messagebox.showerror("Error", "Name cannot be empty")

# Function to delete a student
def delete_student(student):
    if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
        cursor.execute("DELETE FROM students WHERE id=%s", (student[0],))
        db.commit()
        messagebox.showinfo("Success", "Student deleted successfully")
        show_teacher_dashboard()

# Function to submit attendance
def submit_attendance():
    for student in student_vars:
        student_id = student['id']
        present = student['present'].get()
        absent = student['absent'].get()
        status = 'present' if present else 'absent'
        cursor.execute("INSERT INTO attendance_records (student_id, date, status) VALUES (%s, CURDATE(), %s)", (student_id, status))
        db.commit()

    messagebox.showinfo("Attendance", "Attendance submitted successfully")
    show_teacher_dashboard()

# Function to display the student dashboard
def show_student_dashboard(username):
    clear_screen()
    cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
    student_id = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM attendance_records WHERE student_id=%s", (student_id,))
    attendance = cursor.fetchall()

    tk.Label(root, text=f"{username.capitalize()}'s Attendance", font=("Arial", 24)).pack(pady=20)
    for record in attendance:
        tk.Label(root, text=f"Date: {record[2]}, Status: {record[3]}").pack()
    tk.Button(root, text="Back to Login", command=show_login).pack(pady=20)

# Display the login screen initially
show_login()

# Run the Tkinter event loop
root.mainloop()