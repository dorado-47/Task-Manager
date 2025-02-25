import sys
import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Task List
tasks = []

# Load and Save Tasks
def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            global tasks
            tasks = json.load(file)
    except FileNotFoundError:
        pass

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

# Task Functions
def add_task():
    task = task_entry.get()
    due_date = due_date_entry.get()
    priority = priority_var.get()
    category = category_entry.get()
    if task:
        tasks.append({"task": task, "completed": False, "due_date": due_date, "priority": priority, "category": category})
        update_task_list()
        save_tasks()
        task_entry.delete(0, tk.END)
        due_date_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task cannot be empty")

def delete_task():
    selected_task = task_list.curselection()
    if selected_task:
        tasks.pop(selected_task[0])
        update_task_list()
        save_tasks()
    else:
        messagebox.showwarning("Warning", "No task selected")

def mark_task_completed():
    selected_task = task_list.curselection()
    if selected_task:
        tasks[selected_task[0]]["completed"] = True
        update_task_list()
        save_tasks()
    else:
        messagebox.showwarning("Warning", "No task selected")

def update_task_list():
    task_list.delete(0, tk.END)
    for task in tasks:
        status = "✓" if task["completed"] else "✗"
        task_list.insert(tk.END, f'{task["task"]} [{status}] - Due: {task.get("due_date", "No due date")} - Priority: {task.get("priority", "No priority")}')

# GUI Setup
root = tk.Tk()
root.title("Task Manager")
root.geometry("600x400")
root.configure(bg="#f0f0f0")

# UI Elements
tk.Label(root, text="Task:", bg="#f0f0f0").pack()
task_entry = tk.Entry(root, width=50)
task_entry.pack()

tk.Label(root, text="Due Date (YYYY-MM-DD):", bg="#f0f0f0").pack()
due_date_entry = tk.Entry(root, width=50)
due_date_entry.pack()

tk.Label(root, text="Priority:", bg="#f0f0f0").pack()
priority_var = tk.StringVar(value="Medium")
priority_menu = tk.OptionMenu(root, priority_var, "High", "Medium", "Low")
priority_menu.pack()

tk.Label(root, text="Category:", bg="#f0f0f0").pack()
category_entry = tk.Entry(root, width=50)
category_entry.pack()

tk.Button(root, text="Add Task", command=add_task, bg="#4CAF50", fg="white").pack(pady=5)
tk.Button(root, text="Delete Task", command=delete_task, bg="#f44336", fg="white").pack(pady=5)
tk.Button(root, text="Mark Completed", command=mark_task_completed, bg="#008CBA", fg="white").pack(pady=5)

task_list = tk.Listbox(root, width=80, height=10)
task_list.pack(pady=10)

update_task_list()
root.mainloop()