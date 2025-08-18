# Project: Personal To-Do List Application
## Objective:
Develop a Personal To-Do List Application that allows users to create, view, edit, and delete tasks. This project emphasizes user interaction and file handling without the complexity of databases.
## Project Details:
**1. Functionality:**
_o Task Management:_
▪ Users can add tasks with a title and description.
▪ Users can mark tasks as completed or delete them.
_o Categorization:_
▪ Allow users to categorize tasks (e.g., Work, Personal, Urgent).
_o Persistence:_
▪ Store tasks in a local text file (JSON or CSV format) to save user progress between sessions.

**2. User Interface:**
o Use a simple command-line interface or a basic graphical interface using libraries like Tkinter.
o Provide clear prompts and feedback for user actions (adding, editing, deleting tasks).

**3. Deployment:**
o The application can be run locally on the user’s machine without any complex deployment requirements.

**5. Documentation:**
o Provide user-friendly documentation that explains how to use the application and the features available in a ppt(10-15 slides)

## Guidance
**1. Set Up Your Environment:**
• Make sure to have Python installed on your machine.

**2. Project Structure:**
• Organize your project into files, such as:

/todo_app
├── todo.py        # Main application logic
├── tasks.json     # File to store tasks (or tasks.csv)
└── README.md      # Documentation

**3. Implement Core Features:**
• _Task Class:_ Define a class to represent a task:

_**class Task:**_
def __init__(self, title, description, category):
self.title = title
self.description = description
self.category = category
self.completed = False
def mark_completed(self):
self.completed = True

• _File Handling:_ Write functions to save and load tasks from a JSON file:

import json
def save_tasks(tasks):
with open('tasks.json', 'w') as f:
json.dump([task.__dict__ for task in tasks], f)
def load_tasks():
try:
with open('tasks.json', 'r') as f:
return [Task(**data) for data in json.load(f)]
except FileNotFoundError:
return []

**4. User Interaction:**
• Implement a simple command-line interface to interact with the user:

def main():
tasks = load_tasks()
while True:
print("1. Add Task")
print("2. View Tasks")
print("3. Mark Task Completed")
print("4. Delete Task")
print("5. Exit")
choice = input("Choose an option: ")
if choice == '1':
# Code to add a task
elif choice == '2':
# Code to display tasks
elif choice == '3':
# Code to mark a task as completed
elif choice == '4':
# Code to delete a task
elif choice == '5':
save_tasks(tasks)
break

**5. Testing and Documentation:**
• Test the application to ensure all features work correctly and provide clear documentation in the README file.
