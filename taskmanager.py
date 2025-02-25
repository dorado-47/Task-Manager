import sys
import json

tasks = []
undo_stack = []  # Stack to store last actions for undo

def save_tasks_to_file():
    with open("tasks.json", "w") as f:
        json.dump(tasks, f)

def load_tasks_from_file():
    global tasks
    try:
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

def add_task(task, due_date=None, priority="Medium"):
    task_data = {"task": task, "completed": False, "due_date": due_date, "priority": priority}
    tasks.append(task_data)
    undo_stack.append(("add", task_data))
    save_tasks_to_file()
    print(f'Added task: {task} | Due Date: {due_date or "None"} | Priority: {priority}')

def delete_task(task_index):
    try:
        removed_task = tasks.pop(task_index)
        undo_stack.append(("delete", removed_task, task_index))
        save_tasks_to_file()
        print(f'Deleted task: {removed_task["task"]}')
    except IndexError:
        print("Invalid task number")

def edit_task(task_index, new_task):
    try:
        old_task = tasks[task_index]["task"]
        tasks[task_index]["task"] = new_task
        undo_stack.append(("edit", task_index, old_task))
        save_tasks_to_file()
        print(f'Edited task: {old_task} -> {new_task}')
    except IndexError:
        print("Invalid task number")

def view_tasks():
    if not tasks:
        print("No tasks available")
    else:
        for i, task in enumerate(tasks):
            status = "Completed" if task["completed"] else "Pending"
            print(f'{i + 1}. {task["task"]} [{status}] | Due: {task["due_date"] or "None"} | Priority: {task["priority"]}')

def mark_task_completed(task_index):
    try:
        tasks[task_index]["completed"] = True
        undo_stack.append(("complete", task_index))
        save_tasks_to_file()
        print(f'Marked task as completed: {tasks[task_index]["task"]}')
    except IndexError:
        print("Invalid task number")

def clear_tasks():
    global tasks
    undo_stack.append(("clear", tasks.copy()))
    tasks = []
    save_tasks_to_file()
    print("All tasks cleared.")

def undo_last_action():
    if not undo_stack:
        print("No actions to undo.")
        return
    
    last_action = undo_stack.pop()
    
    if last_action[0] == "add":
        tasks.remove(last_action[1])
    elif last_action[0] == "delete":
        tasks.insert(last_action[2], last_action[1])
    elif last_action[0] == "edit":
        tasks[last_action[1]]["task"] = last_action[2]
    elif last_action[0] == "complete":
        tasks[last_action[1]]["completed"] = False
    elif last_action[0] == "clear":
        tasks = last_action[1]
    
    save_tasks_to_file()
    print("Undo successful.")

def show_help():
    print("""
    Available commands:
    - add <task> <due_date> <priority>: Add a new task with an optional due date and priority
    - delete <task_number>: Delete a task by its number
    - edit <task_number> <new_task>: Edit an existing task
    - view: View all tasks
    - complete <task_number>: Mark a task as completed
    - clear: Remove all tasks
    - undo: Undo last action
    - help: Show this help message
    - exit: Exit the application
    """)

def main():
    print("Task Manager Application")
    load_tasks_from_file()
    show_help()
    
    while True:
        command = input("Enter command: ").strip().split()
        if not command:
            continue

        if command[0] == "add":
            task = " ".join(command[1:-2]) if len(command) > 3 else " ".join(command[1:])
            due_date = command[-2] if len(command) > 3 else None
            priority = command[-1] if len(command) > 3 else "Medium"
            add_task(task, due_date, priority)

        elif command[0] == "delete":
            if len(command) > 1 and command[1].isdigit():
                delete_task(int(command[1]) - 1)
            else:
                print("Invalid command")

        elif command[0] == "edit":
            if len(command) > 2 and command[1].isdigit():
                edit_task(int(command[1]) - 1, " ".join(command[2:]))
            else:
                print("Invalid command")

        elif command[0] == "view":
            view_tasks()

        elif command[0] == "complete":
            if len(command) > 1 and command[1].isdigit():
                mark_task_completed(int(command[1]) - 1)
            else:
                print("Invalid command")

        elif command[0] == "clear":
            clear_tasks()

        elif command[0] == "undo":
            undo_last_action()

        elif command[0] == "help":
            show_help()

        elif command[0] == "exit":
            print("Exiting the application. Goodbye!")
            sys.exit()

        else:
            print("Unknown command. Type 'help' to see available commands.")

if __name__ == "__main__":
    main()
