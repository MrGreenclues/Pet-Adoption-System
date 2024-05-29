from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
import subprocess
import mysql.connector
from tkinter import ttk
from tkinter import messagebox

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\xampp\htdocs\pet\build\assets\frame2")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_main():
    window.destroy()
    script_dir = Path(__file__).resolve().parent
    addpet_path = script_dir / "main.py"
    subprocess.run(["python", str(addpet_path)])

# Function to fetch data from database
def fetch_data():
    try:
        # Establish a connection to the database
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='pet'
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT pname, pgender, age, breed FROM pet")  # Correct table name
        rows = mycursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        rows = []
    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()
    return rows
# --------------------------------------------------------------------------------------------------------------
# Function to populate Treeview
def populate_treeview():
    # Clear existing data in Treeview
    for row in tree.get_children():
        tree.delete(row)
    
    # Fetch data from database
    data = fetch_data()
    
    # Insert fetched data into Treeview
    for row in data:
        tree.insert('', 'end', values=row)
# ADD pet-------------------
# Function to add new pet data to the database
def add_pet():
    pname = entry_1.get()
    pgender = entry_2.get()
    age = entry_3.get()
    breed = entry_4.get()
    
    if pname and pgender and age and breed:
        try:
            # Establish a connection to the database
            mydb = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='pet'
            )
            mycursor = mydb.cursor()
            sql = "INSERT INTO pet (pname, pgender, age, breed) VALUES (%s, %s, %s, %s)"
            val = (pname, pgender, age, breed)
            mycursor.execute(sql, val)
            mydb.commit()
            messagebox.showinfo("Success", "Pet added successfully")
            populate_treeview()  # Refresh the Treeview with new data
            # Clear the entry fields after successful update
            entry_1.delete(0, 'end')
            entry_2.delete(0, 'end')
            entry_3.delete(0, 'end')
            entry_4.delete(0, 'end')
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Failed to add pet")
        finally:
            if mycursor:
                mycursor.close()
            if mydb:
                mydb.close()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Function to load selected pet data into entry fields for editing
def load_selected_pet(event):
    selected_item = tree.selection()
    if not selected_item:
        # messagebox.showwarning("Selection Error", "Please select a pet")
        return

    selected_pet = tree.item(selected_item[0], 'values')
    entry_1.delete(0, 'end')
    entry_1.insert(0, selected_pet[0])
    entry_2.delete(0, 'end')
    entry_2.insert(0, selected_pet[1])
    entry_3.delete(0, 'end')
    entry_3.insert(0, selected_pet[2])
    entry_4.delete(0, 'end')
    entry_4.insert(0, selected_pet[3])

# ADD pet-------------------
# Function to delete pet data from the database
def delete_pet():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a pet to delete")
        return
    
    pet_name = tree.item(selected_item[0], 'values')[0]
    
    try:
        # Establish a connection to the database
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='pet'
        )
        mycursor = mydb.cursor()
        sql = "DELETE FROM pet WHERE pname = %s"
        val = (pet_name,)
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success", "Pet deleted successfully")
        populate_treeview()  # Refresh the Treeview with new data
        # Refresh the Treeview with new data
            # Clear the entry fields after successful update
        entry_1.delete(0, 'end')
        entry_2.delete(0, 'end')
        entry_3.delete(0, 'end')
        entry_4.delete(0, 'end')
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", "Failed to delete pet")
    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()
# Function to load selected pet data into entry fields for editing
def load_selected_pet(event):
    selected_item = tree.selection()
    if not selected_item:
        # messagebox.showwarning("Selection Error", "Please select a pet")
        return

    selected_pet = tree.item(selected_item[0], 'values')
    entry_1.delete(0, 'end')
    entry_1.insert(0, selected_pet[0])
    entry_2.delete(0, 'end')
    entry_2.insert(0, selected_pet[1])
    entry_3.delete(0, 'end')
    entry_3.insert(0, selected_pet[2])
    entry_4.delete(0, 'end')
    entry_4.insert(0, selected_pet[3])

# DELETE pet-----
# UPDATE pet----
# Function to update pet data in the database
# Function to update pet data in the database
def update_pet():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a pet to update")
        return

    pname = entry_1.get()
    pgender = entry_2.get()
    age = entry_3.get()
    breed = entry_4.get()

    old_pet_name = tree.item(selected_item[0], 'values')[0]

    if pname and pgender and age and breed:
        try:
            # Establish a connection to the database
            mydb = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='pet'
            )
            mycursor = mydb.cursor()
            sql = "UPDATE pet SET pname = %s, pgender = %s, age = %s, breed = %s WHERE pname = %s"
            val = (pname, pgender, age, breed, old_pet_name)
            mycursor.execute(sql, val)
            mydb.commit()
            messagebox.showinfo("Success", "Pet updated successfully")
            populate_treeview()  # Refresh the Treeview with new data
            # Clear the entry fields after successful update
            entry_1.delete(0, 'end')
            entry_2.delete(0, 'end')
            entry_3.delete(0, 'end')
            entry_4.delete(0, 'end')
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Failed to update pet")
        finally:
            if mycursor:
                mycursor.close()
            if mydb:
                mydb.close()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Function to load selected pet data into entry fields for editing
def load_selected_pet(event):
    selected_item = tree.selection()
    if not selected_item:
        # messagebox.showwarning("Selection Error", "Please select a pet")
        return

    selected_pet = tree.item(selected_item[0], 'values')
    entry_1.delete(0, 'end')
    entry_1.insert(0, selected_pet[0])
    entry_2.delete(0, 'end')
    entry_2.insert(0, selected_pet[1])
    entry_3.delete(0, 'end')
    entry_3.insert(0, selected_pet[2])
    entry_4.delete(0, 'end')
    entry_4.insert(0, selected_pet[3])


#update pet data----
window = Tk()
window.geometry("996x622")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=622,
    width=996,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(
    0.0,
    0.0,
    996.0,
    622.0,
    fill="#D9D9D9",
    outline=""
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=add_pet,
    relief="flat"
)
button_1.place(
    x=17.0,
    y=455.0,
    width=183.0,
    height=36.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=update_pet,
    relief="flat"
)
button_2.place(
    x=17.0,
    y=506.0,
    width=183.0,
    height=33.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command= delete_pet ,
    relief="flat"
)
button_3.place(
    x=17.0,
    y=553.0,
    width=183.0,
    height=33.0
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    111.5,
    152.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FDF2F2",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=38.0,
    y=128.0,
    width=147.0,
    height=46.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    111.5,
    240.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FDF2F2",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=38.0,
    y=216.0,
    width=147.0,
    height=46.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    111.5,
    328.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#FDF2F2",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=38.0,
    y=304.0,
    width=147.0,
    height=46.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    111.5,
    416.0,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#FDF2F2",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=38.0,
    y=392.0,
    width=147.0,
    height=46.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    84.0,
    108.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    92.0,
    382.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    103.0,
    206.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    92.0,
    293.0,
    image=image_image_4
)

canvas.create_rectangle(
    0.0,
    0.0,
    996.0,
    78.0,
    fill="#60714F",
    outline=""
)

canvas.create_text(
    800.0,
    15.0,
    anchor="nw",
    text="Add Pet",
    fill="#E9DEDE",
    font=("RobotoRoman ExtraBold", 40 * -1)
)

canvas.create_rectangle(
    245.0,
    111.0,
    963.0,
    586.0,
    fill="#60714F",
    outline=""
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=open_main,
    relief="flat"
)
button_4.place(
    x=6.0,
    y=4.0,
    width=112.0,
    height=70.0
)

# Create the Treeview widget
columns = ('#1', '#2', '#3', '#4')
tree = ttk.Treeview(window, columns=columns, show='headings')
tree.heading('#1', text='Pet Name')
tree.heading('#2', text='Gender')
tree.heading('#3', text='Age')
tree.heading('#4', text='Breed')

# Adjust column widths
tree.column('#1', width=100, minwidth=100, anchor='center')
tree.column('#2', width=80, minwidth=80, anchor='center')
tree.column('#3', width=50, minwidth=50, anchor='center')
tree.column('#4', width=100, minwidth=100, anchor='center')

tree.place(x=250.0, y=115.0, width=708.0, height=470.0)
tree.bind('<<TreeviewSelect>>', load_selected_pet)
# Populate Treeview with data
populate_treeview()

window.resizable(False, False)
window.mainloop()
