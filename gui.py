import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import datetime
import json
import os
import traceback

from crewai import Agent, Task, Crew, LLM
from main import Config, AgentFactory, TaskManager, SERPER_API_KEY, COUNTRY, SEARCH_RESULTS

from agent_window import AgentWindow
from monitor_window import MonitorWindow

class TerminalWindow:
    """Separate window for terminal output."""

    def __init__(self, root_window):
        self.window = tk.Toplevel(root_window)
        self.window.title("Analysis Terminal Output")

        # Nord theme colors
        self.nord_colors = {
            "bg": "#2E3440",  # Nord darker background
            "fg": "#D8DEE9",  # Nord foreground
            "accent": "#88C0D0",  # Nord blue
            "button_bg": "#3B4252",  # Nord darker blue
            "button_fg": "#ECEFF4",  # Nord lighter text
        }

        # Configure the window
        window_width = int(root_window.winfo_screenwidth() * 0.4)
        window_height = int(root_window.winfo_screenheight() * 0.6)
        x_position = int((root_window.winfo_screenwidth() - window_width) / 2)
        y_position = int((root_window.winfo_screenheight() - window_height) / 2)

        self.window.geometry(
            f"{window_width}x{window_height}+{x_position}+{y_position}"
        )
        self.window.configure(bg=self.nord_colors["bg"])

        # Create the terminal text widget
        self.terminal_area = scrolledtext.ScrolledText(
            self.window,
            wrap=tk.WORD,
            bg=self.nord_colors["bg"],
            fg=self.nord_colors["fg"],
            font=("Cascadia Code", 10),
            insertbackground=self.nord_colors["accent"],
        )
        self.terminal_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Configure text tags for ANSI colors using Nord palette
        self.terminal_area.tag_configure("bold", font=("Cascadia Code", 10, "bold"))
        self.terminal_area.tag_configure("magenta", foreground="#B48EAD")  # Nord purple
        self.terminal_area.tag_configure("green", foreground="#A3BE8C")  # Nord green
        self.terminal_area.tag_configure("red", foreground="#BF616A")  # Nord red
        self.terminal_area.tag_configure("blue", foreground="#81A1C1")  # Nord blue
        self.terminal_area.tag_configure("cyan", foreground="#88C0D0")  # Nord cyan
        self.terminal_area.tag_configure("yellow", foreground="#EBCB8B")  # Nord yellow
        self.terminal_area.tag_configure("white", foreground="#ECEFF4")  # Nord snow

        # Style the close button with Nord theme
        style = ttk.Style()
        style.configure(
            "Nord.TButton",
            background=self.nord_colors["button_bg"],
            foreground=self.nord_colors["button_fg"],
            bordercolor=self.nord_colors["button_bg"],
            darkcolor=self.nord_colors["button_bg"],
            lightcolor=self.nord_colors["button_bg"],
            relief="flat",
        )

        style.configure(
            "NordActive.TButton",
            background=self.nord_colors["button_bg"],
            foreground=self.nord_colors["accent"],
            bordercolor=self.nord_colors["button_bg"],
            darkcolor=self.nord_colors["button_bg"],
            lightcolor=self.nord_colors["button_bg"],
            relief="flat",
        )

        style.map(
            "Nord.TButton",
            background=[
                ("active", "#4C566A"),  # Nord darker blue for hover
                ("disabled", "#2E3440"),
            ],  # Nord darkest for disabled
            foreground=[("disabled", "#4C566A")],
        )  # Nord darker blue for disabled text

        style.map(
            "NordActive.TButton",
            background=[
                ("active", "#4C566A"),  # Nord darker blue for hover
                ("disabled", "#2E3440"),
            ],  # Nord darkest for disabled
            foreground=[("disabled", "#4C566A")],
        )  # Nord darker blue for disabled text

        self.close_button = ttk.Button(
            self.window,
            text="Close Terminal",
            command=self.window.destroy,
            style="Nord.TButton",
            padding=5,
        )
        self.close_button.pack(pady=5)

        # Bind window close event
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)

        # Focus the window
        self.window.focus_set()

    def clear(self):
        """Clear the terminal output."""
        self.terminal_area.delete(1.0, tk.END)

    def write(self, text, tags=None):
        """Write text to the terminal with optional tags."""
        self.terminal_area.insert(tk.END, text, tags)
        self.terminal_area.see(tk.END)
        self.terminal_area.update_idletasks()


class ToolOutputWindow:
    """Separate window for displaying tool outputs."""

    def __init__(self, root_window):
        self.window = tk.Toplevel(root_window)
        self.window.title("Agent Tool Outputs")

        # Nord theme colors
        self.nord_colors = {
            "bg": "#2E3440",  # Nord darker background
            "fg": "#D8DEE9",  # Nord foreground
            "accent": "#88C0D0",  # Nord blue
            "button_bg": "#3B4252",  # Nord darker blue
            "button_fg": "#ECEFF4",  # Nord lighter text
        }

        # Configure the window
        window_width = int(root_window.winfo_screenwidth() * 0.3)
        window_height = int(root_window.winfo_screenheight() * 0.4)
        x_position = int((root_window.winfo_screenwidth() - window_width) / 2)
        y_position = int((root_window.winfo_screenheight() - window_height) / 2)

        self.window.geometry(
            f"{window_width}x{window_height}+{x_position}+{y_position}"
        )
        self.window.configure(bg=self.nord_colors["bg"])

        # Create the output text widget
        self.output_area = scrolledtext.ScrolledText(
            self.window,
            wrap=tk.WORD,
            bg=self.nord_colors["bg"],
            fg=self.nord_colors["fg"],
            font=("Cascadia Code", 10),
            insertbackground=self.nord_colors["accent"],
        )
        self.output_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Configure text tags
        self.output_area.tag_configure("tool_name", 
            font=("Cascadia Code", 10, "bold"),
            foreground="#88C0D0"  # Nord blue
        )
        self.output_area.tag_configure("output", 
            font=("Cascadia Code", 10),
            foreground="#D8DEE9"  # Nord foreground
        )
        self.output_area.tag_configure("separator",
            font=("Cascadia Code", 10),
            foreground="#4C566A"  # Nord muted
        )

        # Close button
        self.close_button = ttk.Button(
            self.window,
            text="Close Tool Output",
            command=self.window.destroy,
            style="Nord.TButton",
            padding=5,
        )
        self.close_button.pack(pady=5)

        # Bind window close event
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)

    def write(self, tool_name, output):
        """Write tool output with formatting."""
        self.output_area.insert(tk.END, f"\n[{tool_name}]\n", "tool_name")
        self.output_area.insert(tk.END, f"{output}\n", "output")
        self.output_area.insert(tk.END, "-" * 50 + "\n", "separator")
        self.output_area.see(tk.END)
        
    def clear(self):
        """Clear the output area."""
        self.output_area.delete(1.0, tk.END)

import datetime
import json
    """GUI for the CrewAI Analysis System."""

import os
        """Initialize the GUI and set up the main window."""

import traceback
        master.title("George Was Right - CrewAI Analysis System")
from crewai import Agent, Task, Crew, LLM
        # Nord theme colors
        self.nord_colors = {
            "bg": "#2E3440",  # Nord darker background
            "fg": "#D8DEE9",  # Nord foreground
            "accent": "#88C0D0",  # Nord blue
            "button_bg": "#3B4252",  # Nord darker blue
            "button_fg": "#ECEFF4",  # Nord lighter text
            "frame_bg": "#3B4252",  # Nord darker blue for frames
            "text_bg": "#2E3440",  # Nord background for text areas
            "text_fg": "#E5E9F0",  # Nord light text
            "success": "#A3BE8C",  # Nord green for active state
        }

        # Configure the main window
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        window_width = int(screen_width * 0.425)
        window_height = int(screen_height * 0.68)
        x_position = int((screen_width - window_width) / 2)

        # Set window size and position
        master.geometry(f"{window_width}x{window_height}+{x_position}+0")
        master.configure(bg=self.nord_colors["bg"])

        # Configure ttk styles with Nord theme
        style = ttk.Style()

        # Configure frame styles
        style.configure("Nord.TFrame", background=self.nord_colors["bg"])
        style.configure("Nord.TLabelframe", background=self.nord_colors["frame_bg"])
        style.configure(
            "Nord.TLabelframe.Label",
            background=self.nord_colors["frame_bg"],
            foreground=self.nord_colors["fg"],
        )

        # Configure button styles
        style.configure(
            "Nord.TButton",
            background=self.nord_colors["button_bg"],
            foreground=self.nord_colors["button_fg"],
            bordercolor=self.nord_colors["button_bg"],
            darkcolor=self.nord_colors["button_bg"],
            lightcolor=self.nord_colors["button_bg"],
            relief="flat",
        )

        style.configure(
            "NordActive.TButton",
            background=self.nord_colors["button_bg"],
            foreground=self.nord_colors["success"],
            bordercolor=self.nord_colors["button_bg"],
            darkcolor=self.nord_colors["button_bg"],
            lightcolor=self.nord_colors["button_bg"],
            relief="flat",
        )

        # Configure button states
        style.map(
            "Nord.TButton",
            background=[
                ("active", "#4C566A"),  # Nord darker blue for hover
                ("disabled", "#2E3440"),
            ],  # Nord darkest for disabled
            foreground=[("disabled", "#4C566A")],
        )  # Nord darker blue for disabled text

        style.map(
            "NordActive.TButton",
            background=[
                ("active", "#4C566A"),  # Nord darker blue for hover
                ("disabled", "#2E3440"),
            ],  # Nord darkest for disabled
            foreground=[("disabled", "#4C566A")],
        )  # Nord darker blue for disabled text

        # Initialize configuration
        self.config = Config()

        # Create main frames
        self.create_menu()

        # Control Panel - Moved up
        control_panel = ttk.Frame(self.master, style="Nord.TFrame")
        control_panel.pack(fill=tk.X, padx=5, pady=2)

        self.start_button = ttk.Button(
            control_panel,
            text="Start Analysis",
            command=self.start_execution,
            style="Nord.TButton",
            padding=5,
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
            "bg": "#2E3440",  # Nord darker background
        self.pause_button = ttk.Button(
            control_panel,
            text="Pause",
            command=self.pause_execution,
            state=tk.DISABLED,
            style="Nord.TButton",
            padding=5,
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)

        # Status Bar - Moved up
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(
            self.master,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            background=self.nord_colors["frame_bg"],
            foreground=self.nord_colors["fg"],
        )
        self.status_bar.pack(fill=tk.X, padx=5, pady=2)

        self.create_main_layout()

        # Initialize state variables
        self.is_running = False
        self.execution_active = False
        self.initialize_crew()

        # Initialize tool output window reference
        self.tool_window = None

    def create_menu(self):
        """Initialize the GUI and set up the main window."""

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

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_main_layout(self):
        """Create the main layout of the GUI including panels and frames."""

        # Create main container with single panel
        main_container = ttk.Frame(self.master, style="Nord.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        # Preview Report Area
        report_frame = ttk.LabelFrame(
            main_container, text="Preview Report", style="Nord.TLabelframe"
        )
        report_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=2)

        # Preview Report Text Area
        self.output_area = scrolledtext.ScrolledText(
            report_frame,
            wrap=tk.WORD,
            height=20,
            font=("Cascadia Code", 10),
            bg=self.nord_colors["text_bg"],
            fg=self.nord_colors["text_fg"],
            insertbackground=self.nord_colors["accent"],
        )
        self.output_area.pack(fill=tk.BOTH, expand=True)

        # Configure text tags for report formatting with Nord colors
        self.output_area.tag_configure(
            "heading1",
            font=("Cascadia Code", 12, "bold"),
            foreground=self.nord_colors["accent"],
        )
        self.output_area.tag_configure(
            "heading2",
            font=("Cascadia Code", 11, "bold"),
            foreground="#81A1C1"  # Nord frost
        )
        self.output_area.tag_configure(
            "normal", font=("Cascadia Code", 10), foreground=self.nord_colors["text_fg"]
        )
        self.output_area.tag_configure(
            "quote",
            font=("Cascadia Code", 10, "italic"),
            foreground="#B48EAD",  # Nord purple
            lmargin1=20,
            lmargin2=20,
        )
        self.output_area.tag_configure(
            "url",
            font=("Cascadia Code", 10),
            foreground="#88C0D0",  # Nord blue
            underline=1,
        )

        # Progress Bar Frame at the bottom
        self.progress_frame = ttk.Frame(self.master, style="Nord.TFrame")
        self.progress_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=2)
        
        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            mode='determinate',
            style="Nord.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X, padx=5, pady=2)

    def initialize_crew(self):
        """Initialize the CrewAI system with agents and tasks."""
        # Initialize the LLM
        llm = LLM(model=self.config.llm_model)
        
        # Initialize the search tool
        search_tool = SerperDevTool(
            n_results=SEARCH_RESULTS,
            country=COUNTRY,
            api_key=SERPER_API_KEY
        )
        
        # Create monitor windows
        screen_width = self.master.winfo_screenwidth()
        window_width = int(screen_width * 0.25)
        
        self.agent_monitor = MonitorWindow(self.master, "Agent Monitor", "agent")
        self.task_monitor = MonitorWindow(self.master, "Task Monitor", "task")
        self.tool_monitor = MonitorWindow(self.master, "Tool Monitor", "tool")

        # Position monitor windows on the right side of the screen
        self.agent_monitor.window.geometry(f"+{screen_width - window_width - 10}+0")
        self.task_monitor.window.geometry(f"+{screen_width - window_width - 10}+{int(self.master.winfo_screenheight() * 0.33)}")
        self.tool_monitor.window.geometry(f"+{screen_width - window_width - 10}+{int(self.master.winfo_screenheight() * 0.66)}")
        
        # Create agent factory with tool callback
        self.agent_factory = AgentFactory(llm, self.tool_callback)
        self.agent_factory.set_search_tool(search_tool)  # Set the search tool
        
        # Create the agents
        self.agents = {
            "researcher": self.agent_factory.create_researcher_agent(),
            "writer": self.agent_factory.create_writer_agent(),
            "illustrator": self.agent_factory.create_illustrator_agent(),
        }

        # Create windows for each agent
        self.agent_windows = {}
        window_positions = {
            "researcher": (0, 0),
            "writer": (1, 0),
            "illustrator": (2, 0)
        }

        for agent_name, agent in self.agents.items():
            window = AgentWindow(self.master, agent_name, agent.role)
            x_pos = window_positions[agent_name][0] * (window_width + 10)
            y_pos = window_positions[agent_name][1] * 100
            window.window.geometry(f"+{x_pos}+{y_pos}")
            self.agent_windows[agent_name] = window
            self.agent_monitor.write(f"✨ Created agent: {agent.role}", "start")
        
        # Create task manager and tasks
        self.task_manager = TaskManager(self.agents)
        self.tasks = self.task_manager.create_tasks()

        # Log tasks
        for task in self.tasks:
            self.task_monitor.write(f"📋 Created task: {task.description[:100]}...", "start")
        
        # Initialize the crew
        self.crew = Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            verbose=True
        )

    def tool_callback(self, tool_name, output):
        """Callback function for tool outputs from agents.
        
        Args:
            tool_name (str): Name of the tool being used
            output (str): Output from the tool
        """
        # Get the current agent's name from the tool's context
        agent_name = getattr(self.current_agent, 'name', '').lower() if hasattr(self, 'current_agent') else None
        
        # Format the output in markdown
        formatted_output = f"""### Tool Usage: {tool_name}
**Agent:** {agent_name}
```
{output}
```
---"""
        
        # Display in tool monitor
        if hasattr(self, 'tool_monitor'):
            self.tool_monitor.write(formatted_output + "\n", "output")
        
        # Display in agent's window if we know which agent is using the tool
        if agent_name and agent_name in self.agent_windows:
            self.agent_windows[agent_name].write(formatted_output + "\n", "tool")

    def process_output_line(self, line, stream='stdout'):
        """Process a line of output from CrewAI and update appropriate monitors."""
        line = line.strip()
        if not line:
            return

        # Extract agent name if present (assuming format like "[researcher]" or "researcher:")
        agent_name = None
        original_line = line
        if line.startswith('[') and ']' in line:
            agent_name = line[1:line.index(']')].lower()
            line = line[line.index(']')+1:].strip()
        elif ':' in line:
            possible_name = line.split(':')[0].lower()
            if possible_name in self.agent_windows:
                agent_name = possible_name
                line = ':'.join(line.split(':')[1:]).strip()

        # Store current agent for tool callback context
        if agent_name:
            self.current_agent = type('Agent', (), {'name': agent_name})()

        # Format the output based on the type
        if "Thought:" in original_line:
            formatted_output = f"""### 💭 Thought
**Agent:** {agent_name}
{line.replace('Thought:', '').strip()}
---"""
            if agent_name and agent_name in self.agent_windows:
                self.agent_windows[agent_name].write(formatted_output + "\n", "thought")
            self.agent_monitor.write(formatted_output + "\n", "thought")
        
        elif "Action:" in original_line:
            formatted_output = f"""### ⚡ Action
**Agent:** {agent_name}
{line.replace('Action:', '').strip()}
---"""
            if agent_name and agent_name in self.agent_windows:
                self.agent_windows[agent_name].write(formatted_output + "\n", "action")
            self.agent_monitor.write(formatted_output + "\n", "action")
        
        elif "Task output:" in original_line or "Final Answer:" in original_line:
            header = "Task Output" if "Task output:" in original_line else "Final Answer"
            content = line.replace('Task output:', '').replace('Final Answer:', '').strip()
            formatted_output = f"""### 📝 {header}
**Agent:** {agent_name}
```
{content}
```
---"""
            if agent_name and agent_name in self.agent_windows:
                self.agent_windows[agent_name].write(formatted_output + "\n", "output")
            self.task_monitor.write(formatted_output + "\n", "output")
        
        else:
            # General output
            formatted_output = f"""### Info
**Agent:** {agent_name}
{line}
---"""
            if agent_name and agent_name in self.agent_windows:
                self.agent_windows[agent_name].write(formatted_output + "\n", "info")
            self.agent_monitor.write(formatted_output + "\n", "info")

    def format_log_entry(self, entry):
        """Format log entry with markdown and proper line breaks."""
        if isinstance(entry, dict):
            if "agent" in entry:
                formatted_agent = entry['agent'].strip().replace('#', '').strip()
                return f"\n# Agent: {formatted_agent}\n## Task: {entry.get('message', '').strip()}\n"
            elif "task" in entry:
                return f"\n### Task: {entry['task'].strip()}\n"
            elif "result" in entry:
                return f"\n#### Result:\n{entry['result'].strip()}\n"
            else:
                return str(entry)
        return f"{str(entry)}\n"

    def setup_text_tags(self):
        """Setup text tags for markdown-like formatting."""
        # Headers with Nord theme colors
        self.output_area.tag_configure(
            "h1",
            font=("Cascadia Code", 14, "bold"),
            foreground="#88C0D0"  # Nord blue
        )
        self.output_area.tag_configure(
            "h2",
            font=("Cascadia Code", 12, "bold"),
            foreground="#81A1C1"  # Nord frost
        )
        self.output_area.tag_configure(
            "h3",
            font=("Cascadia Code", 11, "bold"),
            foreground="#5E81AC"  # Nord darker blue
        )
        self.output_area.tag_configure(
            "h4",
            font=("Cascadia Code", 10, "bold"),
            foreground="#A3BE8C"  # Nord green
        )
        self.output_area.tag_configure(
            "normal",
            font=("Cascadia Code", 10),
            foreground=self.nord_colors["text_fg"]
        )

    def insert_formatted_text(self, text):
        """Insert text with markdown-like formatting into the output area."""
        lines = text.split("\n")
        for line in lines:
            line = line.rstrip()
            if not line:  # Empty line
                self.output_area.insert(tk.END, "\n")
                continue
                
            if line.startswith("# "):
                self.output_area.insert(tk.END, line[2:] + "\n", "h1")
            elif line.startswith("## "):
                self.output_area.insert(tk.END, line[3:] + "\n", "h2")
            elif line.startswith("### "):
                self.output_area.insert(tk.END, line[4:] + "\n", "h3")
            elif line.startswith("#### "):
                self.output_area.insert(tk.END, line[5:] + "\n", "h4")
            else:
                self.output_area.insert(tk.END, line + "\n", "normal")
        
        self.output_area.see(tk.END)
        )
        self.window.configure(bg=self.nord_colors["bg"])
        """Start the analysis execution."""
        self.execution_active = True
        self.start_button.configure(
            style="NordActive.TButton", state="disabled", text="Analysis Running..."
        )
        self.pause_button.configure(style="NordActive.TButton", state="normal")

        # Create and show terminal window
        if (
            not hasattr(self, "terminal_window")
            or not self.terminal_window.window.winfo_exists()
        ):
            self.terminal_window = TerminalWindow(self.master)
            # Position the window to the right of the main window
            main_x = self.master.winfo_x()
            main_y = self.master.winfo_y()
            main_width = self.master.winfo_width()
            self.terminal_window.window.geometry(f"+{main_x + main_width + 10}+{main_y}")
            self.terminal_window.window.lift()  # Bring window to front
            self.terminal_window.window.focus_force()  # Force focus

        self.crew_thread = threading.Thread(target=self.run_crew_analysis)
        self.crew_thread.daemon = True
        self.crew_thread.start()

            wrap=tk.WORD,
        """Pause the analysis execution."""
        self.execution_active = False
        self.start_button.configure(
            style="Nord.TButton", state="normal", text="Start Analysis"
        )
        self.pause_button.configure(style="Nord.TButton", state="disabled")

            font=("Cascadia Code", 10),
        """Save the analysis report to a file."""

        if not self.output_area.get(1.0, tk.END).strip():
            messagebox.showwarning("Warning", "No report to save")
            return

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[
                ("Markdown files", "*.md"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
            initialfile=f"surveillance_analysis_{timestamp}.md",
        )

        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self.output_area.get(1.0, tk.END))
                self.status_var.set(f"Report saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save report: {str(e)}")

    def save_report_as_markdown(self):
        """Save the current report as a markdown file."""
        try:
            # Get the report content
            report_content = self.output_area.get("1.0", tk.END)
            
            # Create filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            model_name = self.config.llm_model.replace('/', '-').replace(':', '-')
            filename = f"report-{model_name}-{timestamp}.md"
            
            # Save the file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            messagebox.showinfo("Report Saved", f"Report has been saved as {filename}")
            return filename
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")
            return None

    def show_settings(self):
        """Show the settings window for configuring the analysis."""

        settings_window = tk.Toplevel(self.master)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.master)

        # Create settings form
        settings_frame = ttk.LabelFrame(settings_window, text="Analysis Configuration")
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # LLM Model
        ttk.Label(settings_frame, text="LLM Model:").grid(
            row=0, column=0, padx=5, pady=5
        )
        llm_entry = ttk.Entry(settings_frame)
        llm_entry.insert(0, self.config.llm_model)
        llm_entry.grid(row=0, column=1, padx=5, pady=5)

        # Country
        ttk.Label(settings_frame, text="Country:").grid(row=1, column=0, padx=5, pady=5)
        country_entry = ttk.Entry(settings_frame)
        country_entry.insert(0, self.config.country)
        country_entry.grid(row=1, column=1, padx=5, pady=5)

        # Search Results
        ttk.Label(settings_frame, text="Search Results:").grid(
            row=2, column=0, padx=5, pady=5
        )
        results_entry = ttk.Entry(settings_frame)
        results_entry.insert(0, str(self.config.search_results))
        results_entry.grid(row=2, column=1, padx=5, pady=5)

    def show_about(self):
        """Show the About dialog with information about the application."""

        about_text = """
        George-Was-Right - CrewAI Analysis System
        
        Version: 2.0
        
        An AI-powered analysis system examining modern events through the lens
        of George Orwell's "1984".
        
        2024 TheRealFredP3D"""

        messagebox.showinfo("About", about_text)

    def run_crew_analysis(self):
        """Execute the analysis in a separate thread."""
        if not self.execution_active:
            return

        try:
            # Update agent windows status
            for window in self.agent_windows.values():
                window.update_status("Starting...")
                window.clear()

            # Create output handlers to capture and process CrewAI output
            import sys
            import io
            import traceback

            class OutputHandler(io.StringIO):
                def __init__(self, gui, original_stream, stream_name='stdout'):
                    super().__init__()
                    self.gui = gui
                    self.original_stream = original_stream
                    self.stream_name = stream_name
                    self.buffer = ""

                def write(self, text):
                    # Write to original stream
                    self.original_stream.write(text)
                    
                    # Add to buffer and process complete lines
                    self.buffer += text
                    while "\n" in self.buffer:
                        line, self.buffer = self.buffer.split("\n", 1)
                        if line.strip():  # Skip empty lines
                            self.gui.process_output_line(line, self.stream_name)

                def flush(self):
                    self.original_stream.flush()

            # Store original stdout and stderr
            original_stdout = sys.stdout
            original_stderr = sys.stderr

            # Create and set custom output handlers
            stdout_handler = OutputHandler(self, original_stdout, 'stdout')
            stderr_handler = OutputHandler(self, original_stderr, 'stderr')
            sys.stdout = stdout_handler
            sys.stderr = stderr_handler

            try:
                # Run the crew's tasks
                result = self.crew.kickoff()

                # Process any remaining buffered output
                if stdout_handler.buffer:
                    self.process_output_line(stdout_handler.buffer, 'stdout')
                if stderr_handler.buffer:
                    self.process_output_line(stderr_handler.buffer, 'stderr')

                # Update status
                self.status_var.set("Analysis completed successfully")
                
                # Update agent windows status
                for window in self.agent_windows.values():
                    window.update_status("Completed")

                # Add monitor logs to the report
                self.output_area.insert(tk.END, "\n\n## Execution Logs\n", "heading1")
                self.add_monitor_logs_to_report()

            finally:
                # Restore original stdout and stderr
                sys.stdout = original_stdout
                sys.stderr = original_stderr

        except Exception as e:
            error_msg = f"Error during execution: {str(e)}\n{traceback.format_exc()}"
            self.terminal_window.write(error_msg, ("red",))
            self.status_var.set("Analysis failed")
            
            # Update agent windows status on error
            for window in self.agent_windows.values():
                window.update_status("Error")

        finally:
            # Reset GUI state
            self.is_running = False
            self.start_button.configure(
                style="Nord.TButton", state="normal", text="Start Analysis"
            )
            self.pause_button.configure(style="Nord.TButton", state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    gui = CrewAI_GUI(root)
    root.mainloop()
        self.terminal_area.tag_configure("bold", font=("Cascadia Code", 10, "bold"))
        self.terminal_area.tag_configure("magenta", foreground="#B48EAD")  # Nord purple
        self.terminal_area.tag_configure("green", foreground="#A3BE8C")  # Nord green
        self.terminal_area.tag_configure("red", foreground="#BF616A")  # Nord red
        self.terminal_area.tag_configure("blue", foreground="#81A1C1")  # Nord blue
        self.terminal_area.tag_configure("cyan", foreground="#88C0D0")  # Nord cyan
        self.terminal_area.tag_configure("yellow", foreground="#EBCB8B")  # Nord yellow
        self.terminal_area.tag_configure("white", foreground="#ECEFF4")  # Nord snow

        # Style the close button with Nord theme
        style = ttk.Style()
        style.configure(
            "Nord.TButton",
            background=self.nord_colors["button_bg"],
            foreground=self.nord_colors["button_fg"],
            bordercolor=self.nord_colors["button_bg"],
            darkcolor=self.nord_colors["button_bg"],
            lightcolor=self.nord_colors["button_bg"],
            relief="flat",
        )

        style.configure(
            "NordActive.TButton",
            background=self.nord_colors["button_bg"],
            foreground=self.nord_colors["accent"],
            bordercolor=self.nord_colors["button_bg"],
            darkcolor=self.nord_colors["button_bg"],
            lightcolor=self.nord_colors["button_bg"],
            relief="flat",
        )

        style.map(
            "Nord.TButton",
            background=[
                ("active", "#4C566A"),  # Nord darker blue for hover
                ("disabled", "#2E3440"),
            ],  # Nord darkest for disabled
            foreground=[("disabled", "#4C566A")],
        )  # Nord darker blue for disabled text

        style.map(
            "NordActive.TButton",
            background=[
                ("active", "#4C566A"),  # Nord darker blue for hover
                ("disabled", "#2E3440"),
            ],  # Nord darkest for disabled
            foreground=[("disabled", "#4C566A")],
        )  # Nord darker blue for disabled text

        self.close_button = ttk.Button(
            self.window,
            text="Close Terminal",
            command=self.window.destroy,
            style="Nord.TButton",
            padding=5,
        )
        self.close_button.pack(pady=5)

        # Bind window close event
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)

        # Focus the window
        self.window.focus_set()

    def clear(self):
        """Clear the terminal output."""
        self.terminal_area.delete(1.0, tk.END)

    def write(self, text, tags=None):
        """Write text to the terminal with optional tags."""
        self.terminal_area.insert(tk.END, text, tags)
        self.terminal_area.see(tk.END)
        self.terminal_area.update_idletasks()


class ToolOutputWindow:
    """Separate window for displaying tool outputs."""

    def __init__(self, root_window):
        self.window = tk.Toplevel(root_window)
        self.window.title("Agent Tool Outputs")

        # Nord theme colors
        self.nord_colors = {
            "bg": "#2E3440",  # Nord darker background
            "fg": "#D8DEE9",  # Nord foreground
            "accent": "#88C0D0",  # Nord blue
            "button_bg": "#3B4252",  # Nord darker blue
            "button_fg": "#ECEFF4",  # Nord lighter text
        }

        # Configure the window
        window_width = int(root_window.winfo_screenwidth() * 0.3)
        window_height = int(root_window.winfo_screenheight() * 0.4)
        x_position = int((root_window.winfo_screenwidth() - window_width) / 2)
        y_position = int((root_window.winfo_screenheight() - window_height) / 2)

        self.window.geometry(
            f"{window_width}x{window_height}+{x_position}+{y_position}"
        )
        self.window.configure(bg=self.nord_colors["bg"])

        # Create the output text widget
        self.output_area = scrolledtext.ScrolledText(
            self.window,
            wrap=tk.WORD,
            bg=self.nord_colors["bg"],
            fg=self.nord_colors["fg"],
            font=("Cascadia Code", 10),
            insertbackground=self.nord_colors["accent"],
        )
        self.output_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Configure text tags
        self.output_area.tag_configure("tool_name", 
            font=("Cascadia Code", 10, "bold"),
            foreground="#88C0D0"  # Nord blue
        )
        self.output_area.tag_configure("output", 
            font=("Cascadia Code", 10),
            foreground="#D8DEE9"  # Nord foreground
        )
        self.output_area.tag_configure("separator",
            font=("Cascadia Code", 10),
            foreground="#4C566A"  # Nord muted
        )

        # Close button
        self.close_button = ttk.Button(
            self.window,
            text="Close Tool Output",
            command=self.window.destroy,
            style="Nord.TButton",
            padding=5,
        )
        self.close_button.pack(pady=5)

        # Bind window close event
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)

    def write(self, tool_name, output):
        """Write tool output with formatting."""
        self.output_area.insert(tk.END, f"\n[{tool_name}]\n", "tool_name")
        self.output_area.insert(tk.END, f"{output}\n", "output")
        self.output_area.insert(tk.END, "-" * 50 + "\n", "separator")
        self.output_area.see(tk.END)
        
    def clear(self):
        """Clear the output area."""
        self.output_area.delete(1.0, tk.END)

=======
    def __init__(self, master):
        """Initialize the GUI and set up the main window."""

        self.master = master
        master.title("George Was Right - CrewAI Analysis System")

        # Nord theme colors
        self.nord_colors = {
            "bg": "#2E3440",  # Nord darker background
            "fg": "#D8DEE9",  # Nord foreground
            "accent": "#88C0D0",  # Nord blue
            "button_bg": "#3B4252",  # Nord darker blue
            "button_fg": "#ECEFF4",  # Nord lighter text
            "frame_bg": "#3B4252",  # Nord darker blue for frames
            "text_bg": "#2E3440",  # Nord background for text areas
            "text_fg": "#E5E9F0",  # Nord light text
            "success": "#A3BE8C",  # Nord green for active state
        }

        # Configure the main window
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        window_width = int(screen_width * 0.425)
        window_height = int(screen_height * 0.68)
        x_position = int((screen_width - window_width) / 2)

        # Set window size and position
        master.geometry(f"{window_width}x{window_height}+{x_position}+0")
        master.configure(bg=self.nord_colors["bg"])

        # Configure ttk styles with Nord theme
        style = ttk.Style()

        # Configure frame styles
        style.configure("Nord.TFrame", background=self.nord_colors["bg"])
        style.configure("Nord.TLabelframe", background=self.nord_colors["frame_bg"])
        style.configure(
            "Nord.TLabelframe.Label",
            background=self.nord_colors["frame_bg"],
            foreground=self.nord_colors["fg"],
        )

        # Configure button styles
        style.configure(
            "Nord.TButton",
            background=self.nord_colors["button_bg"],
            foreground=self.nord_colors["button_fg"],
            bordercolor=self.nord_colors["button_bg"],
            darkcolor=self.nord_colors["button_bg"],
            lightcolor=self.nord_colors["button_bg"],
            relief="flat",
        )

        style.configure(
            "NordActive.TButton",
            background=self.nord_colors["button_bg"],
            foreground=self.nord_colors["success"],
            bordercolor=self.nord_colors["button_bg"],
            darkcolor=self.nord_colors["button_bg"],
            lightcolor=self.nord_colors["button_bg"],
            relief="flat",
        )

        # Configure button states
        style.map(
            "Nord.TButton",
            background=[
                ("active", "#4C566A"),  # Nord darker blue for hover
                ("disabled", "#2E3440"),
            ],  # Nord darkest for disabled
            foreground=[("disabled", "#4C566A")],
        )  # Nord darker blue for disabled text

        style.map(
            "NordActive.TButton",
            background=[
                ("active", "#4C566A"),  # Nord darker blue for hover
                ("disabled", "#2E3440"),
            ],  # Nord darkest for disabled
            foreground=[("disabled", "#4C566A")],
        )  # Nord darker blue for disabled text

        # Initialize configuration
        self.config = Config()

        # Create main frames
        self.create_menu()

        # Control Panel - Moved up
        control_panel = ttk.Frame(self.master, style="Nord.TFrame")
        control_panel.pack(fill=tk.X, padx=5, pady=2)

        self.start_button = ttk.Button(
            control_panel,
            text="Start Analysis",
            command=self.start_execution,
            style="Nord.TButton",
            padding=5,
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = ttk.Button(
            control_panel,
            text="Pause",
            command=self.pause_execution,
            state=tk.DISABLED,
            style="Nord.TButton",
            padding=5,
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)

        # Status Bar - Moved up
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(
            self.master,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            background=self.nord_colors["frame_bg"],
            foreground=self.nord_colors["fg"],
        )
        self.status_bar.pack(fill=tk.X, padx=5, pady=2)

        self.create_main_layout()

        # Initialize state variables
        self.is_running = False
        self.execution_active = False
        self.initialize_crew()

        # Initialize tool output window reference
        self.tool_window = None

    def create_menu(self):
        """Initialize the GUI and set up the main window."""

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
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_main_layout(self):
        """Create the main layout of the GUI including panels and frames."""

        # Create main container with single panel
        main_container = ttk.Frame(self.master, style="Nord.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        # Preview Report Area
        report_frame = ttk.LabelFrame(
            main_container, text="Preview Report", style="Nord.TLabelframe"
        )
        report_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=2)

        # Preview Report Text Area
        self.output_area = scrolledtext.ScrolledText(
            report_frame,
            wrap=tk.WORD,
            height=20,
            font=("Cascadia Code", 10),
            bg=self.nord_colors["text_bg"],
            fg=self.nord_colors["text_fg"],
            insertbackground=self.nord_colors["accent"],
        )
        self.output_area.pack(fill=tk.BOTH, expand=True)

        # Configure text tags for report formatting with Nord colors
        self.output_area.tag_configure(
            "heading1",
            font=("Cascadia Code", 12, "bold"),
            foreground=self.nord_colors["accent"],
        )
        self.output_area.tag_configure(
            "heading2",
            font=("Cascadia Code", 11, "bold"),
            foreground="#81A1C1"  # Nord frost
        )
        self.output_area.tag_configure(
            "normal", font=("Cascadia Code", 10), foreground=self.nord_colors["text_fg"]
        )
        self.output_area.tag_configure(
            "quote",
            font=("Cascadia Code", 10, "italic"),
            foreground="#B48EAD",  # Nord purple
            lmargin1=20,
            lmargin2=20,
        )
        self.output_area.tag_configure(
            "url",
            font=("Cascadia Code", 10),
            foreground="#88C0D0",  # Nord blue
            underline=1,
        )

        # Progress Bar Frame at the bottom
        self.progress_frame = ttk.Frame(self.master, style="Nord.TFrame")
        self.progress_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=2)
        
        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            mode='determinate',
            style="Nord.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X, padx=5, pady=2)

    def initialize_crew(self):
        """Initialize the CrewAI system with agents and tasks."""
        # Initialize the LLM
        llm = LLM(model=self.config.llm_model)
        
        # Initialize the search tool
        search_tool = SerperDevTool(
            n_results=SEARCH_RESULTS,
            country=COUNTRY,
            api_key=SERPER_API_KEY
        )
        
        # Create monitor windows
        screen_width = self.master.winfo_screenwidth()
        window_width = int(screen_width * 0.25)
        
        self.agent_monitor = MonitorWindow(self.master, "Agent Monitor", "agent")
        self.task_monitor = MonitorWindow(self.master, "Task Monitor", "task")
        self.tool_monitor = MonitorWindow(self.master, "Tool Monitor", "tool")

        # Position monitor windows on the right side of the screen
        self.agent_monitor.window.geometry(f"+{screen_width - window_width - 10}+0")
        self.task_monitor.window.geometry(f"+{screen_width - window_width - 10}+{int(self.master.winfo_screenheight() * 0.33)}")
        self.tool_monitor.window.geometry(f"+{screen_width - window_width - 10}+{int(self.master.winfo_screenheight() * 0.66)}")
        
        # Create agent factory with tool callback
        self.agent_factory = AgentFactory(llm, self.tool_callback)
        self.agent_factory.set_search_tool(search_tool)  # Set the search tool
        
        # Create the agents
        self.agents = {
            "researcher": self.agent_factory.create_researcher_agent(),
            "writer": self.agent_factory.create_writer_agent(),
            "illustrator": self.agent_factory.create_illustrator_agent(),
        }

        # Create windows for each agent
        self.agent_windows = {}
        window_positions = {
            "researcher": (0, 0),
            "writer": (1, 0),
            "illustrator": (2, 0)
        }

        for agent_name, agent in self.agents.items():
            window = AgentWindow(self.master, agent_name, agent.role)
            x_pos = window_positions[agent_name][0] * (window_width + 10)
            y_pos = window_positions[agent_name][1] * 100
            window.window.geometry(f"+{x_pos}+{y_pos}")
            self.agent_windows[agent_name] = window
            self.agent_monitor.write(f"✨ Created agent: {agent.role}", "start")
        
        # Create task manager and tasks
        self.task_manager = TaskManager(self.agents)
        self.tasks = self.task_manager.create_tasks()

        # Log tasks
        for task in self.tasks:
            self.task_monitor.write(f"📋 Created task: {task.description[:100]}...", "start")
        
        # Initialize the crew
        self.crew = Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            verbose=True
        )

    def tool_callback(self, tool_name, output):
        """Callback function for tool outputs from agents.
        
        Args:
            tool_name (str): Name of the tool being used
            output (str): Output from the tool
        """
        # Get the current agent's name from the tool's context
        agent_name = getattr(self.current_agent, 'name', '').lower() if hasattr(self, 'current_agent') else None
        
        # Format the output in markdown
        formatted_output = f"""### Tool Usage: {tool_name}
**Agent:** {agent_name}
```
{output}
```
---"""
        
        # Display in tool monitor
        if hasattr(self, 'tool_monitor'):
            self.tool_monitor.write(formatted_output + "\n", "output")
        
        # Display in agent's window if we know which agent is using the tool
        if agent_name and agent_name in self.agent_windows:
            self.agent_windows[agent_name].write(formatted_output + "\n", "tool")

    def process_output_line(self, line, stream='stdout'):
        """Process a line of output from CrewAI and update appropriate monitors."""
        line = line.strip()
        if not line:
            return

        # Extract agent name if present (assuming format like "[researcher]" or "researcher:")
        agent_name = None
        original_line = line
        if line.startswith('[') and ']' in line:
            agent_name = line[1:line.index(']')].lower()
            line = line[line.index(']')+1:].strip()
        elif ':' in line:
            possible_name = line.split(':')[0].lower()
            if possible_name in self.agent_windows:
                agent_name = possible_name
                line = ':'.join(line.split(':')[1:]).strip()

        # Store current agent for tool callback context
        if agent_name:
            self.current_agent = type('Agent', (), {'name': agent_name})()

        # Format the output based on the type
        if "Thought:" in original_line:
            formatted_output = f"""### 💭 Thought
**Agent:** {agent_name}
{line.replace('Thought:', '').strip()}
---"""
            if agent_name and agent_name in self.agent_windows:
                self.agent_windows[agent_name].write(formatted_output + "\n", "thought")
            self.agent_monitor.write(formatted_output + "\n", "thought")
        
        elif "Action:" in original_line:
            formatted_output = f"""### ⚡ Action
**Agent:** {agent_name}
{line.replace('Action:', '').strip()}
---"""
            if agent_name and agent_name in self.agent_windows:
                self.agent_windows[agent_name].write(formatted_output + "\n", "action")
            self.agent_monitor.write(formatted_output + "\n", "action")
        
        elif "Task output:" in original_line or "Final Answer:" in original_line:
            header = "Task Output" if "Task output:" in original_line else "Final Answer"
            content = line.replace('Task output:', '').replace('Final Answer:', '').strip()
            formatted_output = f"""### 📝 {header}
**Agent:** {agent_name}
```
{content}
```
---"""
            if agent_name and agent_name in self.agent_windows:
                self.agent_windows[agent_name].write(formatted_output + "\n", "output")
            self.task_monitor.write(formatted_output + "\n", "output")
        
        else:
            # General output
            formatted_output = f"""### Info
**Agent:** {agent_name}
{line}
---"""
            if agent_name and agent_name in self.agent_windows:
                self.agent_windows[agent_name].write(formatted_output + "\n", "info")
            self.agent_monitor.write(formatted_output + "\n", "info")

    def format_log_entry(self, entry):
        """Format log entry with markdown and proper line breaks."""
        if isinstance(entry, dict):
            if "agent" in entry:
                formatted_agent = entry['agent'].strip().replace('#', '').strip()
                return f"\n# Agent: {formatted_agent}\n## Task: {entry.get('message', '').strip()}\n"
            elif "task" in entry:
                return f"\n### Task: {entry['task'].strip()}\n"
            elif "result" in entry:
                return f"\n#### Result:\n{entry['result'].strip()}\n"
            else:
                return str(entry)
        return f"{str(entry)}\n"

    def setup_text_tags(self):
        """Setup text tags for markdown-like formatting."""
        # Headers with Nord theme colors
        self.output_area.tag_configure(
            "h1",
            font=("Cascadia Code", 14, "bold"),
            foreground="#88C0D0"  # Nord blue
        )
        self.output_area.tag_configure(
            "h2",
            font=("Cascadia Code", 12, "bold"),
            foreground="#81A1C1"  # Nord frost
        )
        self.output_area.tag_configure(
            "h3",
            font=("Cascadia Code", 11, "bold"),
            foreground="#5E81AC"  # Nord darker blue
        )
        self.output_area.tag_configure(
            "h4",
            font=("Cascadia Code", 10, "bold"),
            foreground="#A3BE8C"  # Nord green
        )
        self.output_area.tag_configure(
            "normal",
            font=("Cascadia Code", 10),
            foreground=self.nord_colors["text_fg"]
        )

    def insert_formatted_text(self, text):
        """Insert text with markdown-like formatting into the output area."""
        lines = text.split("\n")
        for line in lines:
            line = line.rstrip()
            if not line:  # Empty line
                self.output_area.insert(tk.END, "\n")
                continue
                
            if line.startswith("# "):
                self.output_area.insert(tk.END, line[2:] + "\n", "h1")
            elif line.startswith("## "):
                self.output_area.insert(tk.END, line[3:] + "\n", "h2")
            elif line.startswith("### "):
                self.output_area.insert(tk.END, line[4:] + "\n", "h3")
            elif line.startswith("#### "):
                self.output_area.insert(tk.END, line[5:] + "\n", "h4")
            else:
                self.output_area.insert(tk.END, line + "\n", "normal")
        
        self.output_area.see(tk.END)

    def start_execution(self):
        """Start the analysis execution."""
        self.execution_active = True
        self.start_button.configure(
            style="NordActive.TButton", state="disabled", text="Analysis Running..."
        )
        self.pause_button.configure(style="NordActive.TButton", state="normal")

        # Create and show terminal window
        if (
            not hasattr(self, "terminal_window")
            or not self.terminal_window.window.winfo_exists()
        ):
            self.terminal_window = TerminalWindow(self.master)
            # Position the window to the right of the main window
            main_x = self.master.winfo_x()
            main_y = self.master.winfo_y()
            main_width = self.master.winfo_width()
            self.terminal_window.window.geometry(f"+{main_x + main_width + 10}+{main_y}")
            self.terminal_window.window.lift()  # Bring window to front
            self.terminal_window.window.focus_force()  # Force focus

        self.crew_thread = threading.Thread(target=self.run_crew_analysis)
        self.crew_thread.daemon = True
        self.crew_thread.start()

    def pause_execution(self):
        """Pause the analysis execution."""
        self.execution_active = False
        self.start_button.configure(
            style="Nord.TButton", state="normal", text="Start Analysis"
        )
        self.pause_button.configure(style="Nord.TButton", state="disabled")

    def save_report(self):
        """Save the analysis report to a file."""

        if not self.output_area.get(1.0, tk.END).strip():
            messagebox.showwarning("Warning", "No report to save")
            return

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[
                ("Markdown files", "*.md"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
            initialfile=f"surveillance_analysis_{timestamp}.md",
        )

        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self.output_area.get(1.0, tk.END))
                self.status_var.set(f"Report saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save report: {str(e)}")

    def save_report_as_markdown(self):
        """Save the current report as a markdown file."""
        try:
            # Get the report content
            report_content = self.output_area.get("1.0", tk.END)
            
            # Create filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            model_name = self.config.llm_model.replace('/', '-').replace(':', '-')
            filename = f"report-{model_name}-{timestamp}.md"
            
            # Save the file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            messagebox.showinfo("Report Saved", f"Report has been saved as {filename}")
            return filename
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")
            return None

    def show_settings(self):
        """Show the settings window for configuring the analysis."""

        settings_window = tk.Toplevel(self.master)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.master)

        # Create settings form
        settings_frame = ttk.LabelFrame(settings_window, text="Analysis Configuration")
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # LLM Model
        ttk.Label(settings_frame, text="LLM Model:").grid(
            row=0, column=0, padx=5, pady=5
        )
        llm_entry = ttk.Entry(settings_frame)
        llm_entry.insert(0, self.config.llm_model)
        llm_entry.grid(row=0, column=1, padx=5, pady=5)

        # Country
        ttk.Label(settings_frame, text="Country:").grid(row=1, column=0, padx=5, pady=5)
        country_entry = ttk.Entry(settings_frame)
        country_entry.insert(0, self.config.country)
        country_entry.grid(row=1, column=1, padx=5, pady=5)

        # Search Results
        ttk.Label(settings_frame, text="Search Results:").grid(
            row=2, column=0, padx=5, pady=5
        )
        results_entry = ttk.Entry(settings_frame)
        results_entry.insert(0, str(self.config.search_results))
        results_entry.grid(row=2, column=1, padx=5, pady=5)

    def show_about(self):
        """Show the About dialog with information about the application."""

        about_text = """
        George-Was-Right - CrewAI Analysis System
        
        Version: 2.0
        
        An AI-powered analysis system examining modern events through the lens
        of George Orwell's "1984".
        
        2024 TheRealFredP3D"""

        messagebox.showinfo("About", about_text)

    def run_crew_analysis(self):
        """Execute the analysis in a separate thread."""
        if not self.execution_active:
            return

        try:
            # Update agent windows status
            for window in self.agent_windows.values():
                window.update_status("Starting...")
                window.clear()

            # Create output handlers to capture and process CrewAI output
            import sys
            import io
            import traceback

            class OutputHandler(io.StringIO):
                def __init__(self, gui, original_stream, stream_name='stdout'):
                    super().__init__()
                    self.gui = gui
                    self.original_stream = original_stream
                    self.stream_name = stream_name
                    self.buffer = ""

                def write(self, text):
                    # Write to original stream
                    self.original_stream.write(text)
                    
                    # Add to buffer and process complete lines
                    self.buffer += text
                    while "\n" in self.buffer:
                        line, self.buffer = self.buffer.split("\n", 1)
                        if line.strip():  # Skip empty lines
                            self.gui.process_output_line(line, self.stream_name)

                def flush(self):
                    self.original_stream.flush()

            # Store original stdout and stderr
            original_stdout = sys.stdout
            original_stderr = sys.stderr

            # Create and set custom output handlers
            stdout_handler = OutputHandler(self, original_stdout, 'stdout')
            stderr_handler = OutputHandler(self, original_stderr, 'stderr')
            sys.stdout = stdout_handler
            sys.stderr = stderr_handler

            try:
                # Run the crew's tasks
                result = self.crew.kickoff()

                # Process any remaining buffered output
                if stdout_handler.buffer:
                    self.process_output_line(stdout_handler.buffer, 'stdout')
                if stderr_handler.buffer:
                    self.process_output_line(stderr_handler.buffer, 'stderr')

                # Update status
                self.status_var.set("Analysis completed successfully")
                
                # Update agent windows status
                for window in self.agent_windows.values():
                    window.update_status("Completed")

                # Add monitor logs to the report
                self.output_area.insert(tk.END, "\n\n## Execution Logs\n", "heading1")
                self.add_monitor_logs_to_report()

            finally:
                # Restore original stdout and stderr
                sys.stdout = original_stdout
                sys.stderr = original_stderr

        except Exception as e:
            error_msg = f"Error during execution: {str(e)}\n{traceback.format_exc()}"
            self.terminal_window.write(error_msg, ("red",))
            self.status_var.set("Analysis failed")
            
            # Update agent windows status on error
            for window in self.agent_windows.values():
                window.update_status("Error")

        finally:
            # Reset GUI state
            self.is_running = False
            self.start_button.configure(
                style="Nord.TButton", state="normal", text="Start Analysis"
            )
            self.pause_button.configure(style="Nord.TButton", state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    gui = CrewAI_GUI(root)
    root.mainloop()
