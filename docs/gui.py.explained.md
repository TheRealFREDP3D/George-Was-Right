The `gui.py` file is responsible for the graphical user interface (GUI) implementation of the "George Was Right - CrewAI Analysis System." Here's a high-level overview of its components:

### Initialization and Setup

- **Class Definition**: The `CrewAI_GUI` class is defined to encapsulate the GUI logic.
- **Window Configuration**: The main window is set up with a title and dimensions, configuring it to take up a portion of the screen.
- **Configuration**: An instance of the `Config` class is initialized to manage configuration settings.

<!-- file: f:\BACKUP\FRED\PROJECTS\_GITHUB-TheRealFredP3D\George-Was-Right\_PUBLIC-REPO\gui.py -->
```python
class CrewAI_GUI:
    def __init__(self, master):
        self.master = master
        master.title("George Was Right - CrewAI Analysis System")

        # Configure the main window
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        window_width = int(screen_width * 0.5)  # 50% of screen width
        window_height = screen_height * 0.8  # 80% of screen height
        x_position = int((screen_width - window_width) / 2)  # Center horizontally

        # Set window size and position
        master.geometry(f"{window_width}x{window_height}+{x_position}+0")
        master.configure(bg="#f0f0f0")

        # Initialize configuration
        self.config = Config()
```

### GUI Components

- **Menu**: A menu bar is created with options for File and Settings, including functionalities like saving reports or exiting the application.
- **Status Bar**: Displays the current status of operations (e.g., "Ready", "Analysis in Progress").

```python
def create_menu(self):
    menubar = tk.Menu(self.master)
    self.master.config(menu=menubar)

    # File Menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Save Report", command=self.save_report)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=self.master.quit)

    # Settings Menu
    settings_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Settings", menu=settings_menu)
    settings_menu.add_command(label="Configure", command=self.show_settings)
```

### Core Functionality

- **Crew Initialization**: Sets up the language model (LLM), an `AgentFactory`, and agents for tasks.
- **Task Manager**: Uses agents to create and manage tasks.

```python
def initialize_crew(self):
    # Initialize LLM
    llm = LLM(model=self.config.llm_model)

    # Create agent factory
    agent_factory = AgentFactory(llm)

    # Create agents using factory methods from main.py
    agents = {
        "researcher": agent_factory.create_researcher_agent(),
        "writer": agent_factory.create_writer_agent(),
        "illustrator": agent_factory.create_illustrator_agent(),
    }

    # Create task manager and list tasks
    task_manager = TaskManager(agents)
    tasks = task_manager.create_tasks()
```

### Execution and Logging

- **Buttons**: Start and pause buttons to control the analysis process.
- **Output and Logs**: Logs and results from the analysis are formatted and displayed in the GUI.

```python
def start_execution(self):
    if not self.is_running:
        self.is_running = True
        self.start_button.configure(state=tk.DISABLED)
        self.pause_button.configure(state=tk.NORMAL)
        self.status_var.set("Analysis in progress...")

        # Start execution in a separate thread
        self.execution_thread = threading.Thread(target=self.run_analysis)
        self.execution_thread.start()

def format_log_entry(self, entry):
    """Format log entry with markdown and proper line breaks."""
    if isinstance(entry, dict):
        if 'agent' in entry:
            return f"\n## 🤖 {entry['agent']}\n{entry.get('message', '')}\n"
        elif 'task' in entry:
            return f"\n### 📋 Task: {entry['task']}\n"
        elif 'result' in entry:
            return f"\n#### ✅ Result:\n{entry['result']}\n"
        else:
            return str(entry)
    return f"{str(entry)}\n"
```

The file integrates a task-oriented architecture for analyzing surveillance and privacy issues, utilizing agents to complete specific roles and functionalities with a user-friendly GUI.

---

The `gui.py` file is responsible for the graphical user interface (GUI) implementation of the "George Was Right - CrewAI Analysis System." Here's a high-level overview of its components:

### Initialization and Setup

- **Class Definition**: The `CrewAI_GUI` class is defined to encapsulate the GUI logic.
- **Window Configuration**: The main window is set up with a title and dimensions, configuring it to take up a portion of the screen.
- **Configuration**: An instance of the `Config` class is initialized to manage configuration settings.

<!-- file: f:\BACKUP\FRED\PROJECTS\_GITHUB-TheRealFredP3D\George-Was-Right\_PUBLIC-REPO\gui.py -->
```python
class CrewAI_GUI:
    def __init__(self, master):
        self.master = master
        master.title("George Was Right - CrewAI Analysis System")

        # Configure the main window
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        window_width = int(screen_width * 0.5)  # 50% of screen width
        window_height = screen_height * 0.8  # 80% of screen height
        x_position = int((screen_width - window_width) / 2)  # Center horizontally

        # Set window size and position
        master.geometry(f"{window_width}x{window_height}+{x_position}+0")
        master.configure(bg="#f0f0f0")

        # Initialize configuration
        self.config = Config()
```

### GUI Components

- **Menu**: A menu bar is created with options for File and Settings, including functionalities like saving reports or exiting the application.
- **Status Bar**: Displays the current status of operations (e.g., "Ready", "Analysis in Progress").

```python
def create_menu(self):
    menubar = tk.Menu(self.master)
    self.master.config(menu=menubar)

    # File Menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Save Report", command=self.save_report)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=self.master.quit)

    # Settings Menu
    settings_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Settings", menu=settings_menu)
    settings_menu.add_command(label="Configure", command=self.show_settings)
```

### Core Functionality

- **Crew Initialization**: Sets up the language model (LLM), an `AgentFactory`, and agents for tasks.
- **Task Manager**: Uses agents to create and manage tasks.

```python
def initialize_crew(self):
    # Initialize LLM
    llm = LLM(model=self.config.llm_model)

    # Create agent factory
    agent_factory = AgentFactory(llm)

    # Create agents using factory methods from main.py
    agents = {
        "researcher": agent_factory.create_researcher_agent(),
        "writer": agent_factory.create_writer_agent(),
        "illustrator": agent_factory.create_illustrator_agent(),
    }

    # Create task manager and list tasks
    task_manager = TaskManager(agents)
    tasks = task_manager.create_tasks()
```

### Execution and Logging

- **Buttons**: Start and pause buttons to control the analysis process.
- **Output and Logs**: Logs and results from the analysis are formatted and displayed in the GUI.

```python
def start_execution(self):
    if not self.is_running:
        self.is_running = True
        self.start_button.configure(state=tk.DISABLED)
        self.pause_button.configure(state=tk.NORMAL)
        self.status_var.set("Analysis in progress...")

        # Start execution in a separate thread
        self.execution_thread = threading.Thread(target=self.run_analysis)
        self.execution_thread.start()

def format_log_entry(self, entry):
    """Format log entry with markdown and proper line breaks."""
    if isinstance(entry, dict):
        if 'agent' in entry:
            return f"\n## 🤖 {entry['agent']}\n{entry.get('message', '')}\n"
        elif 'task' in entry:
            return f"\n### 📋 Task: {entry['task']}\n"
        elif 'result' in entry:
            return f"\n#### ✅ Result:\n{entry['result']}\n"
        else:
            return str(entry)
    return f"{str(entry)}\n"
```

The file integrates a task-oriented architecture for analyzing surveillance and privacy issues, utilizing agents to complete specific roles and functionalities with a user-friendly GUI.
