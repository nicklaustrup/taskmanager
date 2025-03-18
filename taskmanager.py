import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
from tkinter.constants import *
import tkinter.font as tkfont


class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("800x500")
        self.root.resizable(True, True)
        
        # Configure style
        self.configure_style()
    
        # Data storage
        self.tasks = []
        self.load_tasks()
        
        # Create UI
        self.create_widgets()
    
    def configure_style(self):
        self.style = ttk.Style()
        
        # Define a color palette
        self.colors = {
            "primary": "#3498db",       # Blue
            "secondary": "#2ecc71",     # Green
            "background": "#f9f9f9",    # Light Gray
            "text": "#2c3e50",          # Dark Blue/Gray
            "accent": "#e74c3c"         # Red for high priority
        }

        # Apply colors to style
        self.style.configure("TFrame", background=self.colors["background"])
        self.style.configure("TButton", background=self.colors["primary"], foreground="white")
        self.style.configure("TLabel", background=self.colors["background"], foreground=self.colors["text"])
        
        self.style.configure("evenrow.Treeview", background="#f0f0f0")
        self.style.configure("oddrow.Treeview", background="#e0e0e0")

        # configure the treeview alternating colors
        self.style.configure("Treeview", background="#f0f0f0", fieldbackground="#f0f0f0")
        self.task_tree_even_color = "#f0f0f0"
        self.task_tree_odd_color = "#c7d5ed"
        
        self.default_font = tkfont.nametofont("TkDefaultFont")
        self.default_font.configure(family="Helvetica", size=10)
        self.heading_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.style.configure("Heading.TLabel", font=self.heading_font)
        
        self.style.configure("Action.TButton", background=self.colors["primary"])
        self.style.configure("Delete.TButton", background=self.colors["accent"])
        self.style.configure("Complete.TButton", background=self.colors["secondary"])
        
    def create_widgets(self):
    
        # Main container
        main_frame = ttk.Frame(self.root, relief=SOLID, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Task input area
        input_frame = ttk.Frame(main_frame, padding="5")
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Task:", style="Heading.TLabel").grid(row=0, column=0, padx=5, pady=5)
        self.task_entry = ttk.Entry(input_frame, width=30)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Priority:").grid(row=0, column=2, padx=5, pady=5)
        self.priority_var = tk.StringVar()
        self.priority_combo = ttk.Combobox(input_frame, textvariable=self.priority_var, width=10)
        self.priority_combo['values'] = ('Low', 'Medium', 'High')
        self.priority_combo.current(1)
        self.priority_combo.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Button(input_frame, text="Add Task", command=self.add_task,
                background=self.colors["primary"], 
                width=10, foreground="white").grid(row=0, column=4, padx=5, pady=5)
        
        # Task list area
        self.task_tree = ttk.Treeview(
            main_frame, 
            columns=("favorite", "task", "priority", "date", "status"),
            show="headings",
            selectmode="browse"
        )
        
        # Define columns
        self.task_tree.heading("favorite", text="Favorite")
        self.task_tree.heading("task", text="Task")
        self.task_tree.heading("priority", text="Priority")
        self.task_tree.heading("date", text="Created Date")
        self.task_tree.heading("status", text="Status")
        
        # Configure columns
        self.task_tree.column("favorite", width=50)
        self.task_tree.column("task", width=250)
        self.task_tree.column("priority", width=100)
        self.task_tree.column("date", width=150)
        self.task_tree.column("status", width=100)
        
        self.show_favorites_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(input_frame, text="Show Favorites Only", 
            variable=self.show_favorites_var,
            command=self.refresh_task_list).grid(row=1, column=0, columnspan=2)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscroll=scrollbar.set)
        
        # Place tree and scrollbar
        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame, padding="5")
        button_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(button_frame, text="Complete", command=self.mark_complete, 
                background=self.colors["secondary"],
                width=10, foreground="white").pack(side=tk.BOTTOM, pady=5)
                
        tk.Button(button_frame, text="Delete", command=self.delete_task,
                background=self.colors["accent"], 
                width=10, foreground="white").pack(side=tk.BOTTOM, pady=5)
                
        tk.Button(button_frame, text="Edit", command=self.edit_task,
                background=self.colors["primary"], 
                width=10, foreground="white").pack(side=tk.BOTTOM, pady=5)
        
        self.task_tree.bind("<ButtonRelease-1>", self.handle_click)
        
        # Populate with existing tasks
        self.refresh_task_list()

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Task cannot be empty!")
            return
        
        new_task = {
            "favorite": False,
            "text": task_text,
            "priority": self.priority_var.get(),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "status": "Pending"
        }
        
        self.tasks.append(new_task)
        self.save_tasks()
        self.refresh_task_list()
        self.task_entry.delete(0, tk.END)
    
    def refresh_task_list(self, maintain_selection=False):
        # save task data before clearing
        selected_task_data = self.get_selected_task_data(maintain_selection)
        
        # Clear existing items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Configure tags for status and priority BEFORE inserting items
        self.configure_tags()
        
        # Filter tasks if needed
        tasks_to_display = self.tasks
        if self.show_favorites_var.get():
            tasks_to_display = [task for task in self.tasks if task["favorite"]]
        
        # sort tasks by favorite and name
        self.sorted_tasks = sorted(tasks_to_display, key=lambda x: (not x["favorite"], self.priority_value(x["priority"]), x["text"]))
        # Add tasks to tree with appropriate tags
        self.add_tasks_to_tree()
        
        # At the end of refresh_task_list
        if maintain_selection and selected_task_data:
            self.reconnect_selected_task(selected_task_data)
    
    def priority_value(self, priority):
        priority_order = {"Low": 2, "Medium": 1, "High": 0}
        # Handle case insensitivity and default value
        if isinstance(priority, str):
            return priority_order.get(priority, 1)  # Default to Medium (1) if unknown
        return 1  # Default to Medium if not a string
       
    def get_selected_task_data(self, maintain_selection=False):
        if maintain_selection:
            # Get the currently selected item's ID
            selected_items = self.task_tree.selection()
            if selected_items:  # If something is selected
                selected_id = selected_items[0]
                # Get the index of the selected item
                selected_index = self.task_tree.index(selected_id)
                # Store the corresponding task data
                if 0 <= selected_index < len(self.tasks):
                    return self.tasks[selected_index]
    
    def reconnect_selected_task(self, selected_task_data):
        # Find the task in the newly populated tree
        for i, item_id in enumerate(self.task_tree.get_children()):
            # Get values from the tree item
            values = self.task_tree.item(item_id, 'values')
            # Check if this is our previously selected task
            # We might need to check multiple fields to uniquely identify it
            if (values[1] == selected_task_data["text"] and 
                values[3] == selected_task_data["date"]):
                # Select this item
                self.task_tree.selection_set(item_id)
                # Ensure it's visible
                self.task_tree.see(item_id)
                break

    def configure_tags(self):
        # Configure priority tags
        self.task_tree.tag_configure('high', background='#fadbd8')  # Light red
        self.task_tree.tag_configure('medium', background='#f7f3d0')  # Light yellow
        self.task_tree.tag_configure('low', background='#d5f5e3')  # Light green
        
        # Configure row colors
        self.task_tree.tag_configure('evenrow', background=self.task_tree_even_color)
        self.task_tree.tag_configure('oddrow', background=self.task_tree_odd_color)
        
        # Configure status tags
        self.task_tree.tag_configure('completed', foreground='gray', font=('Helvetica', 9, 'italic'), background='white')
        self.task_tree.tag_configure('pending', foreground=self.colors["text"])
        
        self.task_tree.tag_configure('favorite_star', foreground='gold')
        self.task_tree.tag_configure('unfavorite_star', foreground='gray')
    
    def add_tasks_to_tree(self):
        for i, task in enumerate(self.sorted_tasks):
            # Get row and status tags
            row_tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            
            # Convert status to string if it's not already a string
            if isinstance(task["status"], bool):
                task["status"] = "Pending" if not task["status"] else "Completed"
            
            status_tag = task["status"].lower()
            priority_tag = task["priority"].lower()
            
            # Add favorite button
            favorite = "★" if task["favorite"] else "☆"
            favorite_tag = 'favorite_star' if task["favorite"] else 'unfavorite_star'
            
            # Insert with all tags
            item_id = self.task_tree.insert(
                "", tk.END,
                values=(favorite, task["text"], task["priority"], task["date"], task["status"]),
                tags=(priority_tag, status_tag, row_tag, favorite_tag)
            )
    
    def handle_click(self, event):
        print(f"Clicked at x={event.x}, y={event.y}")
        item_id = self.task_tree.identify_row(event.y)
        
        if not item_id:
            return
        column_id = self.task_tree.identify_column(event.x)
        column_index = int(column_id.replace('#', '')) - 1
        
        # If it's the star column
        if column_index == 0:
            # Get the values from the treeview
            values = self.task_tree.item(item_id, 'values')
            
            # Find the matching task in self.tasks
            for task in self.tasks:
                # Assuming the task text is unique or use multiple fields to match
                if task["text"] == values[1] and task["date"] == values[3]:
                    self.toggle_favorite(task)
                    break
    
    def toggle_favorite(self, task):
        # Toggle the favorite status
        if "favorite" in task and task["favorite"] == True:
            task["favorite"] = False
        else:
            task["favorite"] = True

        self.save_tasks()
        self.refresh_task_list(maintain_selection=True)
    
    def mark_complete(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a task to mark as complete.")
            return
        
        values = self.task_tree.item(selected_item[0], 'values')
        
        # Find the matching task in self.tasks
        for task in self.tasks:
            if task["text"] == values[1] and task["date"] == values[3]:
                # Toggle status
                if task["status"] == "Completed":
                    task["status"] = "Pending"
                else:
                    task["status"] = "Completed"
        
                self.save_tasks()
                self.refresh_task_list()
                break
    
    def delete_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a task to delete.")
            return
        
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this task?")
        if not confirm:
            return
        
        item_id = selected_item[0]
        item_index = self.task_tree.index(item_id)
        
        del self.tasks[item_index]
        self.save_tasks()
        self.refresh_task_list()
    
    def edit_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a task to edit.")
            return
        
        item_id = selected_item[0]
        item_index = self.task_tree.index(item_id)
        
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")
        edit_window.geometry("400x150")
        edit_window.resizable(False, False)
    
        # Create a ttk frame that fills the toplevel window
        content_frame = ttk.Frame(edit_window, style="TFrame", padding="10")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(content_frame, text="Task:").grid(row=0, column=0, padx=10, pady=10)
        
        task_var = tk.StringVar(value=self.tasks[item_index]["text"])
        task_entry = ttk.Entry(content_frame, width=30, textvariable=task_var)
        task_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(content_frame, text="Priority:").grid(row=1, column=0, padx=10, pady=10)
        priority_var = tk.StringVar(value=self.tasks[item_index]["priority"])
        priority_combo = ttk.Combobox(content_frame, textvariable=priority_var, width=10)
        priority_combo['values'] = ('Low', 'Medium', 'High')
        priority_combo.grid(row=1, column=1, padx=10, pady=10)
        
        def save_changes():
            self.tasks[item_index]["text"] = task_var.get()
            self.tasks[item_index]["priority"] = priority_var.get()
            self.save_tasks()
            self.refresh_task_list()
            edit_window.destroy()
        
        ttk.Button(content_frame, text="Save", command=save_changes).grid(row=2, column=0, columnspan=2, pady=10)
    
    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)
    
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

def main():
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()