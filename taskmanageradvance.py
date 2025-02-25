import sys
import json
from datetime import datetime

tasks = []

def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            global tasks
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

def add_task(task, due_date=None, priority=None, category=None):
    task_details = {"task": task, "completed": False, "due_date": due_date, "priority": priority, "category": category}
    tasks.append(task_details)
    print(f'Added task: {task}')

def delete_task(task_index):
    try:
        removed_task = tasks.pop(task_index)
        print(f'Deleted task: {removed_task["task"]}')
    except IndexError:
        print("Invalid task number")

def view_tasks():
    if not tasks:
        print("No tasks available")
    else:
        for i, task in enumerate(tasks):
            status = "Completed" if task["completed"] else "Pending"
            due_date = task["due_date"] if task["due_date"] else "No due date"
            priority = task["priority"] if task["priority"] else "No priority"
            category = task["category"] if task["category"] else "No category"
            print(f'{i + 1}. {task["task"]} [{status}] - Due: {due_date} - Priority: {priority} - Category: {category}')

def mark_task_completed(task_index):
    try:
        tasks[task_index]["completed"] = True
        print(f'Marked task as completed: {tasks[task_index]["task"]}')
    except IndexError:
        print("Invalid task number")

def search_tasks(keyword):
    results = [task for task in tasks if keyword.lower() in task["task"].lower()]
    if not results:
        print("No matching tasks found")
    else:
        for i, task in enumerate(results):
            status = "Completed" if task["completed"] else "Pending"
            due_date = task["due_date"] if task["due_date"] else "No due date"
            priority = task["priority"] if task["priority"] else "No priority"
            category = task["category"] if task["category"] else "No category"
            print(f'{i + 1}. {task["task"]} [{status}] - Due: {due_date} - Priority: {priority} - Category: {category}')

def edit_task(task_index, new_task, new_due_date=None, new_priority=None, new_category=None):
    try:
        tasks[task_index]["task"] = new_task
        if new_due_date:
            tasks[task_index]["due_date"] = new_due_date
        if new_priority:
            tasks[task_index]["priority"] = new_priority
        if new_category:
            tasks[task_index]["category"] = new_category
        print(f'Updated task: {new_task}')
    except IndexError:
        print("Invalid task number")

def sort_tasks(sort_by):
    if sort_by == "due_date":
        tasks.sort(key=lambda x: x["due_date"] if x["due_date"] else "9999-12-31")
    elif sort_by == "priority":
        priority_order = {"High": 1, "Medium": 2, "Low": 3, None: 4}
        tasks.sort(key=lambda x: priority_order[x["priority"]])
    elif sort_by == "completed":
        tasks.sort(key=lambda x: x["completed"])  # Pending tasks first
    print(f'Tasks sorted by {sort_by}')

def show_help():
    print("""
    Available commands:
    - add <task>: Add a new task (you will be prompted for due date, priority, and category)
    - delete <task_number>: Delete a task by its number
    - view: View all tasks
    - complete <task_number>: Mark a task as completed
    - search <keyword>: Search for tasks by keyword
    - edit <task_number> <new_task>: Edit an existing task (you will be prompted for new details)
    - sort <due_date/priority/completed>: Sort tasks by due date, priority, or completion status
    - help: Show this help message
    - exit: Exit the application
    """)

def main():
    print("Task Manager Application")
    load_tasks()
    show_help()
    while True:
        command = input("Enter command: ").strip().split()
        if not command:
            continue
        if command[0] == "add":
            task = " ".join(command[1:])
            due_date = input("Enter due date (YYYY-MM-DD) or press enter to skip: ").strip()
            priority = input("Enter priority (High/Medium/Low) or press enter to skip: ").strip()
            category = input("Enter category or press enter to skip: ").strip()
            add_task(task, due_date if due_date else None, priority if priority else None, category if category else None)
        elif command[0] == "delete":
            if len(command) > 1 and command[1].isdigit():
                delete_task(int(command[1]) - 1)
            else:
                print("Invalid command")
        elif command[0] == "view":
            view_tasks()
        elif command[0] == "complete":
            if len(command) > 1 and command[1].isdigit():
                mark_task_completed(int(command[1]) - 1)
            else:
                print("Invalid command")
        elif command[0] == "search":
            if len(command) > 1:
                search_tasks(" ".join(command[1:]))
            else:
                print("Invalid command")
        elif command[0] == "edit":
            if len(command) > 2 and command[1].isdigit():
                new_task = " ".join(command[2:])
                new_due_date = input("Enter new due date (YYYY-MM-DD) or press enter to skip: ").strip()
                new_priority = input("Enter new priority (High/Medium/Low) or press enter to skip: ").strip()
                new_category = input("Enter new category or press enter to skip: ").strip()
                edit_task(int(command[1]) - 1, new_task, new_due_date, new_priority, new_category)
            else:
                print("Invalid command")
        elif command[0] == "sort":
            if len(command) > 1:
                sort_tasks(command[1])
            else:
                print("Invalid command")
        elif command[0] == "help":
            show_help()
        elif command[0] == "exit":
            save_tasks()
            print("Exiting the application. Goodbye!")
            sys.exit()
        else:
            print("Unknown command. Type 'help' to see available commands.")

if __name__ == "__main__":
    main()
