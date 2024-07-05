import tkinter as tk
from tkinter import messagebox
import json
import os

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")

        # Set background image
        try:
            self.background_image = tk.PhotoImage(file="background.jpg")
            self.background_label = tk.Label(root, image=self.background_image)
        except tk.TclError:
            self.background_label = tk.Label(root, bg="white")
        
        self.background_label.place(relwidth=1, relheight=1)

        # Initialize tasks list
        self.tasks = []

        # Create main frame with orange background
        self.main_frame = tk.Frame(root, bg="#FFA500", bd=5)
        self.main_frame.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.8, anchor="center")

        # Create entry widget to add/update tasks
        self.entry_label = tk.Label(self.main_frame, text="Task:", font=("Helvetica", 12), bg="#FFA500", fg="white")
        self.entry_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.entry = tk.Entry(self.main_frame, font=("Helvetica", 12), bg="white", fg="black")
        self.entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Create buttons for adding, updating, and deleting tasks
        self.add_button = tk.Button(self.main_frame, text="Add Task", command=self.add_task, font=("Helvetica", 12), bg="black", fg="white")
        self.add_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.update_button = tk.Button(self.main_frame, text="Update Task", command=self.update_task, font=("Helvetica", 12), bg="black", fg="white")
        self.update_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.delete_button = tk.Button(self.main_frame, text="Delete Task", command=self.delete_task, font=("Helvetica", 12), bg="black", fg="white")
        self.delete_button.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # Create listbox to display tasks
        self.task_listbox = tk.Listbox(self.main_frame, font=("Helvetica", 12), bg="white", fg="black", selectbackground="blue", selectforeground="white")
        self.task_listbox.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Create scrollbar for the listbox
        self.scrollbar = tk.Scrollbar(self.main_frame)
        self.scrollbar.grid(row=2, column=3, sticky="ns")

        # Configure listbox and scrollbar
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        # Load tasks from file
        self.load_tasks()

        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

    def add_task(self):
        """Add a new task to the list."""
        task = self.entry.get()
        if task != "":
            self.tasks.append(task)
            self.update_task_listbox()
            self.entry.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def update_task(self):
       
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            new_task = self.entry.get()
            if new_task != "":
                self.tasks[selected_task_index] = new_task
                self.update_task_listbox()
                self.entry.delete(0, tk.END)
                self.save_tasks()
            else:
                messagebox.showwarning("Warning", "You must enter a task.")
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to update.")

    def delete_task(self):
        """Delete the selected task."""
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_task_index]
            self.update_task_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to delete.")

    def update_task_listbox(self):
        
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

    def load_tasks(self):
        """Load tasks from a JSON file."""
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
                self.update_task_listbox()

    def save_tasks(self):
        """Save tasks to a JSON file."""
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
