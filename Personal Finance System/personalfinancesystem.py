#importing required libraries

import matplotlib.pyplot as plt
import pandas as pd
from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime

#database functions

def connect_db():
  return sqlite3.connect('expenses.db')

def create_table(conn):
  with conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS expenses (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          amount REAL NOT NULL,
          category TEXT NOT NULL,
          date TEXT NOT NULL,
          description TEXT
        );''')

def add_expense(conn, amount, category, date, description):
  with conn:
    conn.execute('''INSERT INTO expenses (amount, category, date, description) 
          VALUES (?, ?, ?, ?)''', (amount, category, date, description))

def update_expense(conn, id, amount, category, date, description):
  with conn:
    conn.execute('''UPDATE expenses SET amount=?, category=?, date=?, description=?
          WHERE id=?''', (amount, category, date, description, id))

def delete_expense(conn, id):
  with conn:
    conn.execute('DELETE FROM expenses WHERE id=?', (id,))

def fetch_expenses(conn):
  with conn:
    return conn.execute('SELECT * FROM expenses').fetchall()

def fetch_expenses_by_date(conn, date):
  with conn:
    return conn.execute('SELECT * FROM expenses WHERE date=?', (date,)).fetchall()

#analysis function

def plot_pie_chart():
  conn = connect_db()
  expenses = fetch_expenses(conn)
  conn.close()

  df = pd.DataFrame(expenses, columns=['ID', 'Amount', 'Category', 'Date', 'Description'])
  category_group = df.groupby('Category')['Amount'].sum()

  category_group.plot(kind='pie', autopct='%1.1f%%', startangle=90, title='Expenses by Category')
  plt.ylabel('')
  plt.show()

#GUI functions

def submit_expense():
  amount = float(amount_entry.get())
  category = category_entry.get()
  date = date_entry.get()
  description = description_entry.get()

  conn = connect_db()
  add_expense(conn, amount, category, date, description)
  conn.close()

  refresh_expense_list()
  clear_entries()
  messagebox.showinfo("Expense Tracker", "Expense Added Successfully")

def delete_selected_expense():
  selected_item = expense_tree.selection()
  if selected_item:
    expense_id = expense_tree.item(selected_item)['values'][0]
    conn = connect_db()
    delete_expense(conn, expense_id)
    conn.close()
    refresh_expense_list()
    messagebox.showinfo("Expense Tracker", "Expense Deleted Successfully")

def update_selected_expense():
  selected_item = expense_tree.selection()
  if selected_item:
    expense_id = expense_tree.item(selected_item)['values'][0]
    amount = float(amount_entry.get())
    category = category_entry.get()
    date = date_entry.get()
    description = description_entry.get()

    conn = connect_db()
    update_expense(conn, expense_id, amount, category, date, description)
    conn.close()
    refresh_expense_list()
    clear_entries()
    messagebox.showinfo("Expense Tracker", "Expense Updated Successfully")

def load_selected_expense(event):
  selected_item = expense_tree.selection()
  if selected_item:
    expense_id, amount, category, date, description = expense_tree.item(selected_item)['values']
    amount_entry.delete(0, tk.END)
    amount_entry.insert(0, amount)
    category_entry.delete(0, tk.END)
    category_entry.insert(0, category)
    date_entry.delete(0, tk.END)
    date_entry.insert(0, date)
    description_entry.delete(0, tk.END)
    description_entry.insert(0, description)

def clear_entries():
  """Clears all the entry fields in the GUI."""
  amount_entry.delete(0, tk.END)
  category_entry.delete(0, tk.END)
  date_entry.delete(0, tk.END)
  description_entry.delete(0, tk.END)

#GUI application initialization
  
root = Tk()  
root.title("Manya's Expense Tracker")

#expense list frame

expense_list_frame = ttk.Frame(root)
expense_list_frame.pack(padx=10, pady=10)

#expense list label

expense_list_label = ttk.Label(expense_list_frame, text="Expenses:")
expense_list_label.pack()

#expense list treeview

expense_tree = ttk.Treeview(expense_list_frame, columns=("ID", "Amount", "Category", "Date", "Description"), show="headings")
expense_tree.heading("#0", text="ID")
expense_tree.heading("ID", text="ID")
expense_tree.heading("Amount", text="Amount")
expense_tree.heading("Category", text="Category")
expense_tree.heading("Date", text="Date")
expense_tree.heading("Description", text="Description")
expense_tree.pack()

#expense entry frame

expense_entry_frame = ttk.Frame(root)
expense_entry_frame.pack(padx=10, pady=10)

#amount label and entry

amount_label = ttk.Label(expense_entry_frame, text="Amount:")
amount_label.pack()
amount_entry = ttk.Entry(expense_entry_frame)
amount_entry.pack()

#category label and entry

category_label = ttk.Label(expense_entry_frame, text="Category:")
category_label.pack()
category_entry = ttk.Entry(expense_entry_frame)
category_entry.pack()

#date label and entry

date_label = ttk.Label(expense_entry_frame, text="Date (YYYY-MM-DD):")
date_label.pack()
date_entry = ttk.Entry(expense_entry_frame)
date_entry.pack()

#description label and entry

description_label = ttk.Label(expense_entry_frame, text="Description:")
description_label.pack()
description_entry = ttk.Entry(expense_entry_frame)
description_entry.pack()

#button frame

button_frame = ttk.Frame(root)
button_frame.pack(padx=10, pady=10)

#submit expense button
submit_button = ttk.Button(button_frame, text="Submit Expense", command=submit_expense)
submit_button.pack(side=tk.LEFT, padx=5)

#clear entries button
clear_button = ttk.Button(button_frame, text="Clear Entries", command=clear_entries)
clear_button.pack(side=tk.LEFT, padx=5)

#view pie chart button
plot_chart_button = ttk.Button(button_frame, text="View Pie Chart", command=plot_pie_chart)
plot_chart_button.pack(side=tk.LEFT, padx=5)

#update selected expense button
update_button = ttk.Button(button_frame, text="Update Expense", command=update_selected_expense)
update_button.pack(side=tk.LEFT, padx=5)

#delete selected expense button
delete_button = ttk.Button(button_frame, text="Delete Expense", command=delete_selected_expense)
delete_button.pack(side=tk.LEFT, padx=5)

#bind selection event for expense list

expense_tree.bind("<<TreeviewSelect>>", load_selected_expense)

#refresh expense list on startup

refresh_expense_list()

#start the main application loop
 
root.mainloop() 

