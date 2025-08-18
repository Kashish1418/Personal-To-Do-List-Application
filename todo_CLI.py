# Step 1 - Task model + storage path
'''
We’ll use a dataclass for tasks and store data in tasks.json (same folder as the script).
'''
from dataclasses import dataclass, asdict
from pathlib import Path
import json

DATA_FILE = Path(__file__).with_name("tasks.json")

@dataclass
class Task:
    id: int
    title: str
    description: str
    category: str
    completed: bool = False

# Step 2 - Load & save helpers
'''
Robust JSON handling with graceful first-run behavior.
'''

def load_tasks() -> list[Task]:
    if not DATA_FILE.exists():
        return []
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return [Task(**item) for item in data]
    except Exception:
        # Corrupt JSON? Start clean (you can also raise if you prefer strictness)
        return []

def save_tasks(tasks: list[Task]) -> None:
    DATA_FILE.write_text(
        json.dumps([asdict(t) for t in tasks], indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

def next_id(tasks: list[Task]) -> int:
    return (max((t.id for t in tasks), default=0) + 1)

# Step 3 — Core operations (add, list, edit, complete, delete)
VALID_CATEGORIES = ["Work", "Personal", "Urgent", "Other"]

def add_task(tasks: list[Task]) -> None:
    title = input("Title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    desc = input("Description: ").strip()
    cat = input(f"Category [{', '.join(VALID_CATEGORIES)} or custom]: ").strip() or "Other"
    t = Task(id=next_id(tasks), title=title, description=desc, category=cat, completed=False)
    tasks.append(t)
    save_tasks(tasks)
    print("✓ Task added.")

def show_tasks(tasks: list[Task]) -> None:
    if not tasks:
        print("No tasks yet.")
        return
    print("\n#  ID  [✓]  Title (Category)")
    print("-- --- ---- ------------------------------")
    for i, t in enumerate(tasks, start=1):
        mark = "✓" if t.completed else " "
        print(f"{i:>2} {t.id:>3}  [{mark}]  {t.title} ({t.category})")
    print()

def pick_index(tasks: list[Task], prompt="Select task # (as shown in list): ") -> int | None:
    if not tasks:
        print("No tasks to choose from.")
        return None
    try:
        idx = int(input(prompt))
        if 1 <= idx <= len(tasks):
            return idx - 1
        print("Invalid selection.")
        return None
    except ValueError:
        print("Enter a number.")
        return None

def edit_task(tasks: list[Task]) -> None:
    show_tasks(tasks)
    i = pick_index(tasks)
    if i is None: return
    t = tasks[i]
    print("Press Enter to keep existing value.")
    new_title = input(f"Title [{t.title}]: ").strip() or t.title
    new_desc  = input(f"Description [{t.description}]: ").strip() or t.description
    new_cat   = input(f"Category [{t.category}]: ").strip() or t.category
    t.title, t.description, t.category = new_title, new_desc, new_cat
    save_tasks(tasks)
    print("✓ Task updated.")

def mark_completed(tasks: list[Task]) -> None:
    show_tasks(tasks)
    i = pick_index(tasks)
    if i is None: return
    tasks[i].completed = True
    save_tasks(tasks)
    print("✓ Task marked completed.")

def delete_task(tasks: list[Task]) -> None:
    show_tasks(tasks)
    i = pick_index(tasks)
    if i is None: return
    removed = tasks.pop(i)
    save_tasks(tasks)
    print(f"✓ Deleted: {removed.title}")

# Step 4 — Menu loop
def main():
    tasks = load_tasks()
    MENU = """
1) Add Task
2) View Tasks
3) Edit Task
4) Mark Task Completed
5) Delete Task
6) Exit
"""
    while True:
        print(MENU)
        choice = input("Choose: ").strip()
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            edit_task(tasks)
        elif choice == "4":
            mark_completed(tasks)
        elif choice == "5":
            delete_task(tasks)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()