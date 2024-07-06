#importing required libraries

from tkinter import *
import tkinter.messagebox as mb
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#function to add an expense

def add_expense():
  global description_entry, category_entry, amount_entry, date_entry
  
  description = description_entry.get()
  category = category_entry.get()
  amount = float(amount_entry.get())
  date = datetime.strptime(date_entry.get(), "%Y-%m-%d").strftime("%d/%m/%Y")

  expenses.append({"description": description, "category": category, "amount": amount, "date": date})

  description_entry.delete(0, END)
  category_entry.delete(0, END)
  amount_entry.delete(0, END)
  date_entry.delete(0, END)

  update_expense_list()
  update_pie_chart()

#function to update the expense list

def update_expense_list():
  listbox.delete(0, END)

  for expense in expenses:
    listbox.insert(END, f"{expense['date']} - {expense['description']} ({expense['category']}) - ${expense['amount']:.2f}")

#function to update pie chart

window = Tk()
window.title("Manya's Expense Tracker Pie-Chart")
fig, ax = plt.subplots()

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack()

def update_pie_chart():
  ax.clear()

  category_totals = {}
  for expense in expenses:
    category = expense["category"]
    amount = expense["amount"]
    category_totals[category] = category_totals.get(category, 0) + amount

  category_labels = list(category_totals.keys())
  category_amounts = list(category_totals.values())

  if category_labels:

    ax.pie(category_amounts, labels=category_labels, autopct="%1.1f%%")
    ax.set_title("Expense Category Distribution")

    canvas.draw()
    window.update()

#function to calculate total expense

def calculate_total_expense():
  total = sum(expense["amount"] for expense in expenses)
  total_label.config(text=f"Total Expense: ${total:.2f}")
    
#function to delete an expense
    
def delete_expense():
  selected_index = listbox.curselection()[0]

  del expenses[selected_index]

  update_expense_list()
  update_pie_chart()

#creating the main window
  
window = Tk()
window.title("Manya's Expense Tracker")
window.geometry('900x900')
window.resizable(0,0)

window["bg"] = "Light Gray" 
frame_font = ("Californian FB", 11) 

#creating and placing components in the window

Label(window, text='EXPENSE TRACKER', font=("Californian FB", 20, "italic"), bg='Black', fg='White').pack(side=TOP, fill=X)

#placing components in the window

Label(window, text='Description',font=("Californian FB", 12, "bold"), bg='Light Gray').place(relx=0.078, rely=0.09)

description_entry = Entry(window, width=18, font=("Californian FB", 12))
description_entry.place(relx=0.03, rely=0.13)

Label(window, text='Category',font=("Californian FB", 12, "bold"), bg='Light Gray').place(relx=0.34, rely=0.09)

category_entry = Entry(window, width=18, font=("Californian FB", 12))
category_entry.place(relx=0.28, rely=0.13)

Label(window, text='Amount', font=("Californian FB", 12, "bold"), bg='Light Gray').place(relx=0.593, rely=0.09)

amount_entry = Entry(window, width=18, font=("Californian FB", 12))
amount_entry.place(relx=0.53, rely=0.13)

Label(window, text='Date(YYYY-MM-DD)',font=("Californian FB", 12, "bold"), bg='Light Gray').place(relx=0.79, rely=0.09)

date_entry = Entry(window, width=18, font=("Californian FB", 12))
date_entry.place(relx=0.78, rely=0.13)

#creating a button to add an expense

Button(window, text='Add Expense', font=frame_font, width=89, command=add_expense).place(relx=0.102 , rely=0.214)

#creating a listbox to display the expenses

listbox = Listbox(window, font=('Californian FB', 12), height=24, width=80)
scroller = Scrollbar(listbox, orient=VERTICAL, command=listbox.yview)
scroller.place(relx=0.976, rely=0, relheight=1)
listbox.config(yscrollcommand=scroller.set)
listbox.place(relx=0.1, rely=0.248)

#creating a button to delete an expense

Button(window, text='Delete Expense', font=frame_font, width=89, command=delete_expense).place(relx=0.102 , rely=0.786)

#creating button to find the total expense

total_label = Label(window, text="", font=("Californian FB", 15, "bold"), bg="Light Gray")
total_label.place(relx=0.4, rely=0.87)

Button(window, text='Total Expense', font=frame_font, width= 30, command=calculate_total_expense).place(relx=0.368, rely=0.92)

#creating a list to store the expenses

expenses = []

#run the main loop

window.mainloop()
