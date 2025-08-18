# Tkinter GUI Version

## Step 1 — Same persistence (reuse schema)
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

def load_tasks() -> list[Task]:
    if not DATA_FILE.exists():
        return []
    try:
        return [Task(**obj) for obj in json.loads(DATA_FILE.read_text(encoding="utf-8"))]
    except Exception:
        return []

def save_tasks(tasks: list[Task]) -> None:
    DATA_FILE.write_text(
        json.dumps([asdict(t) for t in tasks], indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

def next_id(tasks: list[Task]) -> int:
    return (max((t.id for t in tasks), default=0) + 1)

# Step 2 — GUI skeleton (window, widgets, layout)
import tkinter as tk
from tkinter import ttk, messagebox

VALID_CATEGORIES = ["Work", "Personal", "Urgent", "Other"]

class TodoGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Personal To-Do List")
        self.tasks: list[Task] = load_tasks()
        self.filtered_tasks_idx: list[int] = []  # map listbox index -> tasks index
        self._build_ui()
        self.refresh_list()

    def _build_ui(self):
        # Left: listbox + filter
        left = ttk.Frame(self.root, padding=8)
        left.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        filter_row = ttk.Frame(left)
        filter_row.pack(fill="x", pady=(0,6))
        ttk.Label(filter_row, text="Filter by category:").pack(side="left")
        self.filter_var = tk.StringVar(value="All")
        self.filter_combo = ttk.Combobox(filter_row, textvariable=self.filter_var,
                                         values=["All"] + VALID_CATEGORIES, state="readonly", width=12)
        self.filter_combo.pack(side="left", padx=6)
        self.filter_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_list())

        self.listbox = tk.Listbox(left, height=18)
        self.listbox.pack(fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # Right: form
        right = ttk.Frame(self.root, padding=8)
        right.grid(row=0, column=1, sticky="nsew")
        self.root.columnconfigure(1, weight=1)

        ttk.Label(right, text="Title").pack(anchor="w")
        self.title_var = tk.StringVar()
        ttk.Entry(right, textvariable=self.title_var).pack(fill="x", pady=(0,6))

        ttk.Label(right, text="Description").pack(anchor="w")
        self.desc_text = tk.Text(right, height=6)
        self.desc_text.pack(fill="both", expand=True)

        ttk.Label(right, text="Category").pack(anchor="w", pady=(6,0))
        self.cat_var = tk.StringVar(value=VALID_CATEGORIES[-1])
        self.cat_combo = ttk.Combobox(right, textvariable=self.cat_var, values=VALID_CATEGORIES)
        self.cat_combo.pack(fill="x", pady=(0,6))

        btns = ttk.Frame(right)
        btns.pack(fill="x", pady=6)
        ttk.Button(btns, text="Add / Update", command=self.add_or_update).pack(side="left")
        ttk.Button(btns, text="Mark Completed", command=self.mark_completed).pack(side="left", padx=6)
        ttk.Button(btns, text="Delete", command=self.delete_task).pack(side="left")
        ttk.Button(btns, text="Clear Form", command=self.clear_form).pack(side="right")

# Step 3 — Wire up actions (list management + persistence)
    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        self.filtered_tasks_idx = []
        filt = self.filter_var.get()
        for idx, t in enumerate(self.tasks):
            if filt != "All" and t.category != filt:
                continue
            mark = "✓" if t.completed else " "
            self.listbox.insert(tk.END, f"[{mark}] {t.title}  ({t.category})")
            self.filtered_tasks_idx.append(idx)

    def get_selected_task_index(self) -> int | None:
        sel = self.listbox.curselection()
        if not sel:
            return None
        # map listbox row -> tasks index
        return self.filtered_tasks_idx[sel[0]]

    def on_select(self, _event=None):
        idx = self.get_selected_task_index()
        if idx is None: 
            return
        t = self.tasks[idx]
        self.title_var.set(t.title)
        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert(tk.END, t.description)
        self.cat_var.set(t.category)

    def add_or_update(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showerror("Error", "Title cannot be empty.")
            return
        desc = self.desc_text.get("1.0", tk.END).strip()
        cat = (self.cat_var.get().strip() or "Other")

        idx = self.get_selected_task_index()
        if idx is None:
            # add new
            t = Task(id=next_id(self.tasks), title=title, description=desc, category=cat, completed=False)
            self.tasks.append(t)
            messagebox.showinfo("Added", "Task added.")
        else:
            # update existing
            t = self.tasks[idx]
            t.title, t.description, t.category = title, desc, cat
            messagebox.showinfo("Updated", "Task updated.")

        save_tasks(self.tasks)
        self.refresh_list()

    def mark_completed(self):
        idx = self.get_selected_task_index()
        if idx is None:
            messagebox.showinfo("Info", "Select a task first.")
            return
        self.tasks[idx].completed = True
        save_tasks(self.tasks)
        self.refresh_list()

    def delete_task(self):
        idx = self.get_selected_task_index()
        if idx is None:
            messagebox.showinfo("Info", "Select a task to delete.")
            return
        t = self.tasks[idx]
        if messagebox.askyesno("Confirm", f"Delete '{t.title}'?"):
            self.tasks.pop(idx)
            save_tasks(self.tasks)
            self.refresh_list()
            self.clear_form()

    def clear_form(self):
        self.title_var.set("")
        self.desc_text.delete("1.0", tk.END)
        self.cat_var.set(VALID_CATEGORIES[-1])
        self.listbox.selection_clear(0, tk.END)

# Step 4 — Run the app
def main():
    root = tk.Tk()
    # Slightly nicer default spacing
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except:
        pass
    root.geometry("820x420")
    app = TodoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
