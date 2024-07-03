#first, we import necessary libraries

from tkinter import *
import tkinter.messagebox as mb
import sqlite3

#here, we create a connection with the database

connector = sqlite3.connect('contacts.db')
cursor = connector.cursor()

#create database table in sqlite3

cursor.execute(
"CREATE TABLE IF NOT EXISTS CONTACT_BOOK (S_NO INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, EMAIL TEXT, PHONE_NUMBER TEXT, ADDRESS TEXT)"
)

#function to store the information in the record

def submit_record():
    global name_strvar, email_strvar, phone_strvar, address_entry
    global cursor
    name, email, phone, address = name_strvar.get(), email_strvar.get(), phone_strvar.get(), address_entry.get(1.0, END)

    if name=="" or email=="" or phone=="" or address=="": #empty entry in any of the fields
        mb.showerror('Error!', "Please fill all the required fields!")
    else:
        cursor.execute(
        "INSERT INTO CONTACT_BOOK (NAME, EMAIL, PHONE_NUMBER, ADDRESS) VALUES (?,?,?,?)", (name, email, phone, address))
        connector.commit()
        mb.showinfo('Contact Successfully Stored!', "The contact has been successfully stored.")
        listbox.delete(0, END)
        list_contacts()
        clear_fields()

#show all the contacts

def list_contacts():
    curr = connector.execute('SELECT NAME FROM CONTACT_BOOK')
    fetch = curr.fetchall()

    for data in fetch:
        listbox.insert(END, data)

#delete a existing record

def delete_record():
    global listbox, connector, cursor

    if not listbox.get(ACTIVE):
        mb.showerror('No item selected!', "You have not selected any item! Please do the needed.")

    cursor.execute('DELETE FROM CONTACT_BOOK WHERE NAME = ?', (listbox.get(ACTIVE)))
    connector.commit()

    mb.showinfo('Contact deleted!', "The desired contact has been deleted.")
    listbox.delete(0, END)
    list_contacts()

#delete all records

def delete_all_records():
    cursor.execute('DELETE FROM CONTACT_BOOK')
    connector.commit()

    mb.showinfo('All records deleted!', "All the records in your contact book have been deleted.")

    listbox.delete(0, END)
    list_contacts()

#view existing records

def view_record():
    global name_strvar, phone_strvar, email_strvar, address_entry, listbox

    curr = cursor.execute('SELECT * FROM CONTACT_BOOK WHERE NAME=?', listbox.get(ACTIVE))
    values = curr.fetchall()[0]

    name_strvar.set(values[1]); phone_strvar.set(values[3]); email_strvar.set(values[2])

    address_entry.delete(1.0, END)
    address_entry.insert(END, values[4])


def clear_fields():
    global name_strvar, phone_strvar, email_strvar, address_entry, listbox

    listbox.selection_clear(0, END)

    name_strvar.set('')
    phone_strvar.set('')
    email_strvar.set('')
    address_entry.delete(1.0, END)


def search():
    query = str(search_strvar.get())

    if query != '':
        listbox.delete(0, END)

        curr = connector.execute('SELECT * FROM CONTACT_BOOK WHERE NAME LIKE ?', ('%'+query+'%', ))
        check = curr.fetchall()

        for data in check:
            listbox.insert(END, data[1])

#initializing the GUI window

root = Tk()
root.title("Manya's Contact Book")
root.geometry('900x600')
root.resizable(0, 0)

#creating the color and font variables

lf_bg = '#7689de'  
cf_bg = '#a9dce3'
rf_bg = '#7689de' 
frame_font = ("Californian FB", 20)

#creating the StringVar variables

name_strvar = StringVar()
phone_strvar = StringVar()
email_strvar = StringVar()
search_strvar = StringVar()

#creating and placing the components in the window

Label(root, text='CONTACT BOOK', font=("Californian FB", 20, "italic"), bg='Black', fg='White').pack(side=TOP, fill=X)

left_frame = Frame(root, bg=lf_bg)
left_frame.place(relx=0, relheight=1, y=30, relwidth=0.5)

center_frame = Frame(root, bg=cf_bg)
center_frame.place(relx=0.33, relheight=1, y=30, relwidth=0.5)

right_frame = Frame(root, bg=rf_bg)
right_frame.place(relx=0.66, relheight=1, y=30,  relwidth=0.5)

#placing components in the left frame

Label(left_frame, text='Name', bg=lf_bg, font=frame_font).place(relx=0.1, rely=0.04)

name_entry = Entry(left_frame, width=20, font=("Californian FB", 11), textvariable=name_strvar)
name_entry.place(relx=0.1, rely=0.1)

Label(left_frame, text='Phone Number', bg=lf_bg, font=frame_font).place(relx=0.1, rely=0.19)

phone_entry = Entry(left_frame, width=20, font=("Californian FB", 11), textvariable=phone_strvar)
phone_entry.place(relx=0.1, rely=0.25)

Label(left_frame, text='Email', bg=lf_bg, font=frame_font).place(relx=0.1, rely=0.34)

email_entry = Entry(left_frame, width=20, font=("Californian FB", 11), textvariable=email_strvar)
email_entry.place(relx=0.1, rely=0.4)

Label(left_frame, text='Address', bg=lf_bg, font=frame_font).place(relx=0.1, rely=0.49)

address_entry = Text(left_frame, width=20, font=("Californian FB", 11), height=5)
address_entry.place(relx=0.1, rely=0.55)

#placing components in the middle frame

search_entry = Entry(center_frame, width=20, font=("Californian FB", 18), textvariable=search_strvar).place(relx=0.039, rely=0.09)

Button(center_frame, text='Search', font=frame_font, width=16, command=search).place(relx=0.055, rely=0.19)
Button(center_frame, text='Add Record', font=frame_font, width=16, command=submit_record).place(relx=0.055, rely=0.29)
Button(center_frame, text='View Record', font=frame_font, width=16, command=view_record).place(relx=0.055, rely=0.39)
Button(center_frame, text='Clear Fields', font=frame_font, width=16, command=clear_fields).place(relx=0.055, rely=0.49)
Button(center_frame, text='Delete Record', font=frame_font, width=16, command=delete_record).place(relx=0.055, rely=0.59)
Button(center_frame, text='Delete All Records', font=frame_font, width=16, command=delete_all_records).place(relx=0.055, rely=0.69)

#placing components in the right frame

Label(right_frame, text='Saved Contacts', font=("Californian FB", 20), bg=rf_bg).place(relx=0.15, rely=0.04)

listbox = Listbox(right_frame, selectbackground='SkyBlue', bg='Gainsboro', font=('Californian FB', 13), height=20, width=25)
scroller = Scrollbar(listbox, orient=VERTICAL, command=listbox.yview)
scroller.place(relx=0.93, rely=0, relheight=1)
listbox.config(yscrollcommand=scroller.set)
listbox.place(relx=0.1, rely=0.1)

list_contacts()

#finalizing the window
root.update()
root.mainloop()
