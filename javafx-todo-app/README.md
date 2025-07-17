# JavaFX Todo Application

A modern todo list application built with JavaFX, featuring a clean UI and task management capabilities.

## Features

- ✅ Add, edit, and delete tasks
- ✅ Mark tasks as completed
- ✅ Filter tasks by status (All, Active, Completed)
- ✅ Real-time task statistics
- ✅ Clean and modern UI with custom styling
- ✅ Keyboard shortcuts (Enter to add task)
- ✅ Confirmation dialogs for destructive actions

## Requirements

- Java 17 or higher
- Maven 3.6 or higher

## Project Structure

```
javafx-todo-app/
├── src/
│   ├── main/
│   │   ├── java/com/example/todoapp/
│   │   │   ├── TodoApp.java              # Basic todo app
│   │   │   ├── EnhancedTodoApp.java      # Enhanced version with filtering
│   │   │   ├── model/
│   │   │   │   └── Task.java             # Task data model
│   │   │   └── controller/
│   │   │       └── TaskCell.java         # Custom list cell
│   │   └── resources/
│   │       └── styles.css                 # Application styling
├── pom.xml                                # Maven configuration
└── README.md
```

## How to Run

### Method 1: Using the Run Script (No Maven Required)

The easiest way to run the application:

```bash
cd javafx-todo-app
./run.sh
```

The script will automatically:
- Check your Java version
- Download JavaFX if needed
- Compile and run the application

### Method 2: Using Maven

If you have Maven installed:

```bash
cd javafx-todo-app
mvn clean javafx:run
```

### Installing Maven (Optional)

**macOS (using Homebrew):**
```bash
brew install maven
```

**macOS/Linux (manual installation):**
```bash
# Download Maven
curl -O https://dlcdn.apache.org/maven/maven-3/3.9.6/binaries/apache-maven-3.9.6-bin.tar.gz

# Extract
tar -xzvf apache-maven-3.9.6-bin.tar.gz

# Move to /opt
sudo mv apache-maven-3.9.6 /opt/maven

# Add to PATH (add to ~/.zshrc or ~/.bashrc)
export PATH=/opt/maven/bin:$PATH
```

**Verify installation:**
```bash
mvn -version
```

## Usage

1. **Adding Tasks**: Type a task description and press Enter or click "Add Task"
2. **Completing Tasks**: Click the checkbox next to a task
3. **Editing Tasks**: Click the "Edit" button on any task
4. **Deleting Tasks**: Click the "Delete" button on any task
5. **Filtering**: Use the radio buttons to show All, Active, or Completed tasks
6. **Clear Completed**: Remove all completed tasks at once

## Technologies Used

- **JavaFX 21**: Modern Java GUI framework
- **Maven**: Build automation and dependency management
- **Java 17**: Latest LTS version of Java

## Future Enhancements

- [ ] Task persistence (save/load from file)
- [ ] Due dates and reminders
- [ ] Task categories/tags
- [ ] Dark mode support
- [ ] Export tasks to various formats
- [ ] Drag and drop to reorder tasks