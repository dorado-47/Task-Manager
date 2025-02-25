import tkinter as tk
from tkinter import messagebox

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        
        self.tasks = []
        
        # UI Components
        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack(pady=10)
        
        self.add_button = tk.Button(root, text="Add Task", command=self.add_task,fg= 'green')
        self.add_button.pack()
        
        self.task_listbox = tk.Listbox(root, width=50, height=10)
        self.task_listbox.pack(pady=10)
        
        self.complete_button = tk.Button(root, text="Mark Completed", command=self.mark_completed,fg= 'blue')
        self.complete_button.pack()
        
        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task,fg= 'red')
        self.delete_button.pack()
        
    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append({"task": task, "completed": False})
            self.task_listbox.insert(tk.END, f"{task} [Pending]")
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")
        
    def mark_completed(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.tasks[selected_index]["completed"] = True
            self.task_listbox.delete(selected_index)
            self.task_listbox.insert(selected_index, f"{self.tasks[selected_index]['task']} [Completed]")
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to mark as completed!")
        
    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.task_listbox.delete(selected_index)
            del self.tasks[selected_index]
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
