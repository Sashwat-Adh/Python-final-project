import json
import os

FILENAME = "tasks.json"


def load_tasks():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(FILENAME, "w") as f:
        json.dump(tasks, f, indent=2)


def show_tasks(tasks):
    if not tasks:
        print("\nYour to-do list is empty!\n")
        return

    print("\nYour To-Do List:")
    for index, task in enumerate(tasks, start=1):
        status = "[x]" if task["done"] else "[ ]"
        print(f"{index}. {status} {task['task']}")
    print()


def add_task(tasks):
    task_text = input("Enter the new task: ").strip()
    if task_text:
        tasks.append({"task": task_text, "done": False})
        print(f'Added: "{task_text}"')
    else:
        print("Task cannot be empty.")


def complete_task(tasks):
    show_tasks(tasks)
    if not tasks:
        return
    choice = input("Enter the number of the task to mark as done: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(tasks):
        tasks[int(choice) - 1]["done"] = True
        print("Task marked as done!")
    else:
        print("Invalid task number.")


def delete_task(tasks):
    show_tasks(tasks)
    if not tasks:
        return
    choice = input("Enter the number of the task to delete: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(tasks):
        removed = tasks.pop(int(choice) - 1)
        print(f'Deleted: "{removed["task"]}"')
    else:
        print("Invalid task number.")


def print_menu():
    print("=== TO-DO LIST MENU ===")
    print("1. View tasks")
    print("2. Add task")
    print("3. Mark task as done")
    print("4. Delete task")
    print("5. Quit")


def main():
    tasks = load_tasks()

    while True:
        print_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            save_tasks(tasks)
            print("Tasks saved. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

        save_tasks(tasks)


if __name__ == "__main__":
    main()
