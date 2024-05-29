from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
import subprocess
import mysql.connector
from tkinter import ttk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\xampp\htdocs\pet\build\assets\frame3")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_main():
    window.destroy()
    script_dir = Path(__file__).resolve().parent
    addpet_path = script_dir / "main.py"
    subprocess.run(["python", str(addpet_path)])

def fetch_pet_data():
    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='pet'
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT pname, pgender, age, breed FROM pet")
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

def fetch_adopt_data():
    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='pet'
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT pname, owname, address, contact FROM adopt")
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

def populate_pet_treeview():
    for row in pet_tree.get_children():
        pet_tree.delete(row)
    data = fetch_pet_data()
    for row in data:
        pet_tree.insert('', 'end', values=row)

def populate_adopt_treeview():
    for row in adopt_tree.get_children():
        adopt_tree.delete(row)
    data = fetch_adopt_data()
    for row in data:
        adopt_tree.insert('', 'end', values=row)

def load_selected_pet(event):
    selected_item = pet_tree.selection()
    if not selected_item:
        return
    selected_pet = pet_tree.item(selected_item[0], 'values')
    entry_1.delete(0, 'end')
    entry_1.insert(0, selected_pet[0])
    entry_2.delete(0, 'end')
    entry_2.insert(0, '')
    entry_3.delete(0, 'end')
    entry_3.insert(0, '')
    entry_4.delete(0, 'end')
    entry_4.insert(0, '')

def load_selected_adopt(event):
    selected_item = adopt_tree.selection()
    if not selected_item:
        return
    selected_adopt = adopt_tree.item(selected_item[0], 'values')
    entry_1.delete(0, 'end')
    entry_1.insert(0, selected_adopt[0])
    entry_2.delete(0, 'end')
    entry_2.insert(0, selected_adopt[1])
    entry_3.delete(0, 'end')
    entry_3.insert(0, selected_adopt[2])
    entry_4.delete(0, 'end')
    entry_4.insert(0, selected_adopt[3])

def adopt_pet():
    pname = entry_1.get()
    owname = entry_2.get()
    address = entry_3.get()
    contact = entry_4.get()

    if pname and owname and address and contact:
        try:
            mydb = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='pet'
            )
            mycursor = mydb.cursor()
            
            # Insert into adopt table
            sql_insert = "INSERT INTO adopt (pname, owname, address, contact) VALUES (%s, %s, %s, %s)"
            val_insert = (pname, owname, address, contact)
            mycursor.execute(sql_insert, val_insert)
            
            # Delete from pet table
            sql_delete = "DELETE FROM pet WHERE pname = %s"
            val_delete = (pname,)
            mycursor.execute(sql_delete, val_delete)

            mydb.commit()

            messagebox.showinfo("Success", "Pet adopted successfully")
            populate_pet_treeview()
            populate_adopt_treeview()

            entry_1.delete(0, 'end')
            entry_2.delete(0, 'end')
            entry_3.delete(0, 'end')
            entry_4.delete(0, 'end')
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Failed to adopt pet")
        finally:
            if mycursor:
                mycursor.close()
            if mydb:
                mydb.close()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

def update_pet():
    selected_item = adopt_tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a pet to update")
        return
    
    pname = entry_1.get()
    owname = entry_2.get()
    address = entry_3.get()
    contact = entry_4.get()

    if pname and owname and address and contact:
        try:
            mydb = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='pet'
            )
            mycursor = mydb.cursor()

            # Update adopt details
            sql_update = "UPDATE adopt SET pname = %s, owname = %s, address = %s, contact = %s WHERE pname = %s"
            val_update = (pname, owname, address, contact, pname)
            mycursor.execute(sql_update, val_update)

            mydb.commit()

            messagebox.showinfo("Success", "Pet details updated successfully")
            populate_adopt_treeview()  # Refresh the adopt table only

            entry_1.delete(0, 'end')
            entry_2.delete(0, 'end')
            entry_3.delete(0, 'end')
            entry_4.delete(0, 'end')
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Failed to update pet details")
        finally:
            if mycursor:
                mycursor.close()
            if mydb:
                mydb.close()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")


window = Tk()

window.geometry("996x540")
window.configure(bg = "#FFFFFF")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 800,
    width = 996,
    bd = 0,
    highlightthickness=0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    996.0,
    534.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    996.0,
    70.0,
    fill="#60714F",
    outline="")

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    108.5,
    142.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FDF2F2",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=35.0,
    y=118.0,
    width=147.0,
    height=46.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    108.5,
    228.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FDF2F2",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=35.0,
    y=204.0,
    width=147.0,
    height=46.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    108.5,
    314.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#FDF2F2",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=35.0,
    y=290.0,
    width=147.0,
    height=46.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    108.5,
    395.0,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#FDF2F2",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=35.0,
    y=371.0,
    width=147.0,
    height=46.0
)

canvas.create_text(
    790.0,
    10.0,
    anchor="nw",
    text="Adopt Pet",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 36 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    81.0,
    103.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    91.0,
    194.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    98.0,
    361.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    98.0,
    280.0,
    image=image_image_4
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=adopt_pet,
    relief="flat"
)
button_1.place(
    x=14.0,
    y=432.0,
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
    x=14.0,
    y=481.0,
    width=183.0,
    height=36.0
)

canvas.create_rectangle(
    240.0,
    80.0,
    981.0,
    517.0,
    fill="#60714F",
    outline="")

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=open_main,
    relief="flat"
)
button_3.place(
    x=9.0,
    y=0.0,
    width=112.0,
    height=70.0
)

pet_columns = ('#1', '#2', '#3', '#4')
pet_tree = ttk.Treeview(window, columns=pet_columns, show='headings')
pet_tree.heading('#1', text='Pet Name')
pet_tree.heading('#2', text='Gender')
pet_tree.heading('#3', text='Age')
pet_tree.heading('#4', text='Breed')

pet_tree.column('#1', width=100, minwidth=100, anchor='center')
pet_tree.column('#2', width=80, minwidth=80, anchor='center')
pet_tree.column('#3', width=50, minwidth=50, anchor='center')
pet_tree.column('#4', width=100, minwidth=100, anchor='center')

pet_tree.place(x=240.0, y=82.0, width=740.0, height=210.0)
pet_tree.bind('<<TreeviewSelect>>', load_selected_pet)

adopt_columns = ('#1', '#2', '#3', '#4')
adopt_tree = ttk.Treeview(window, columns=adopt_columns, show='headings')
adopt_tree.heading('#1', text='Pet Name')
adopt_tree.heading('#2', text='Owner Name')
adopt_tree.heading('#3', text='Address')
adopt_tree.heading('#4', text='Contact')

adopt_tree.column('#1', width=100, minwidth=100, anchor='center')
adopt_tree.column('#2', width=100, minwidth=100, anchor='center')
adopt_tree.column('#3', width=150, minwidth=150, anchor='center')
adopt_tree.column('#4', width=100, minwidth=100, anchor='center')

adopt_tree.place(x=240.0, y=300.0, width=740.0, height=210.0)
adopt_tree.bind('<<TreeviewSelect>>', load_selected_adopt)

populate_pet_treeview()
populate_adopt_treeview()

window.resizable(False, False)
window.mainloop()
