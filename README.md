# Task Manager

A modern, user-friendly desktop task management application built with Python and Tkinter. This application helps you organize, track, and manage your tasks with an intuitive graphical interface.

## Features

- **Task Management**
  - Create, edit, and delete tasks
  - Set task priorities (High, Medium, Low)
  - Mark tasks as complete
  - Favorite important tasks
  - Automatic task sorting by priority and status

- **User Interface**
  - Clean, modern design with a professional color scheme
  - Intuitive task list view
  - Alternating row colors for better readability
  - Priority-based color coding
  - Responsive layout that adapts to window size

- **Data Persistence**
  - Automatic saving of tasks to JSON file
  - Task data persists between sessions
  - Reliable data storage and retrieval

## Requirements

- Python 3.x
- Tkinter (usually comes with Python installation)

## Installation

1. Clone this repository or download the source code
2. Ensure you have Python 3.x installed on your system
3. Run the application using:
   ```bash
   python taskmanager.py
   ```

## Usage

1. **Adding Tasks**
   - Click the "Add Task" button
   - Fill in the task details (title, description, priority)
   - Click "Save" to create the task

2. **Managing Tasks**
   - Select a task from the list to view its details
   - Use the buttons below the task list to:
     - Mark tasks as complete
     - Edit task details
     - Delete tasks
     - Toggle favorite status

3. **Task Organization**
   - Tasks are automatically sorted by priority and completion status
   - Use the priority system to organize tasks (High, Medium, Low)
   - Favorite important tasks for quick access

## File Structure

- `taskmanager.py`: Main application file containing the TaskManager class and UI implementation
- `tasks.json`: JSON file storing task data

## Preview

![image](https://github.com/user-attachments/assets/df50c218-d914-4478-be6e-1cd0f264c381)


## License

This project is open source and available under the MIT License. 
