import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from crewai import Crew, Agent, Task, LLM
import threading
import datetime
import json
import os
from main import Config, AgentFactory, TaskManager, search_tool

class CrewAI_GUI:
    def __init__(self, master):
        self.master = master
        master.title("George Was Right - CrewAI Analysis System")
        
        # Configure the main window
        master.geometry("1200x800")
        master.configure(bg='#f0f0f0')
        
        # Initialize configuration
        self.config = Config()
        
        # Create main frames
        self.create_menu()
        self.create_main_layout()
        
        # Initialize state variables
        self.is_running = False
        self.initialize_crew()
        
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
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def create_main_layout(self):
        # Create main container
        main_container = ttk.PanedWindow(self.master, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel for agents and tasks
        left_panel = ttk.Frame(main_container)
        main_container.add(left_panel, weight=1)
        
        # Agents Frame
        agents_frame = ttk.LabelFrame(left_panel, text="Agents")
        agents_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.agent_list = ttk.Treeview(agents_frame, columns=("Status",), show="headings")
        self.agent_list.heading("Status", text="Status")
        self.agent_list.pack(fill=tk.BOTH, expand=True)
        
        # Tasks Frame
        tasks_frame = ttk.LabelFrame(left_panel, text="Tasks")
        tasks_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.task_list = ttk.Treeview(tasks_frame, columns=("Status", "Agent"), show="headings")
        self.task_list.heading("Status", text="Status")
        self.task_list.heading("Agent", text="Assigned Agent")
        self.task_list.pack(fill=tk.BOTH, expand=True)
        
        # Right panel for output and report
        right_panel = ttk.Frame(main_container)
        main_container.add(right_panel, weight=2)
        
        # Output Area
        output_frame = ttk.LabelFrame(right_panel, text="Execution Log")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_area = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD)
        self.output_area.pack(fill=tk.BOTH, expand=True)
        
        # Report Area
        report_frame = ttk.LabelFrame(right_panel, text="Analysis Report")
        report_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.report_area = scrolledtext.ScrolledText(report_frame, wrap=tk.WORD)
        self.report_area.pack(fill=tk.BOTH, expand=True)
        
        # Control Panel
        control_panel = ttk.Frame(self.master)
        control_panel.pack(fill=tk.X, padx=5, pady=5)
        
        self.start_button = ttk.Button(control_panel, text="Start Analysis", command=self.start_execution)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = ttk.Button(control_panel, text="Pause", command=self.pause_execution, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.save_button = ttk.Button(control_panel, text="Save Report", command=self.save_report)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.master, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, padx=5, pady=2)
        
    def initialize_crew(self):
        # Initialize LLM
        llm = LLM(model=self.config.llm_model)
        
        # Create agent factory
        agent_factory = AgentFactory(llm)
        
        # Create agents using factory methods from main.py
        agents = {
            'researcher': agent_factory.create_researcher_agent(),
            'writer': agent_factory.create_writer_agent(),
            'illustrator': agent_factory.create_illustrator_agent()
        }
        
        # Create task manager and get tasks
        task_manager = TaskManager(agents)
        tasks = task_manager.create_tasks()
        
        # Initialize crew
        self.crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            verbose=True
        )
        
        # Update agent list in GUI
        for agent in agents.values():
            self.agent_list.insert("", "end", text=agent.role, values=("Ready",))
        
        # Update task list in GUI
        for task in tasks:
            self.task_list.insert("", "end", text=task.description, values=("Pending", task.agent.role))
        
    def start_execution(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.configure(state=tk.DISABLED)
            self.pause_button.configure(state=tk.NORMAL)
            self.status_var.set("Analysis in progress...")
            
            # Start execution in a separate thread
            self.execution_thread = threading.Thread(target=self.run_analysis)
            self.execution_thread.start()
    
    def run_analysis(self):
        try:
            result = self.crew.kickoff()
            self.report_area.delete(1.0, tk.END)
            self.report_area.insert(tk.END, result)
            self.status_var.set("Analysis completed successfully")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred during analysis: {str(e)}")
        finally:
            self.is_running = False
            self.start_button.configure(state=tk.NORMAL)
            self.pause_button.configure(state=tk.DISABLED)
    
    def pause_execution(self):
        if self.is_running:
            # Implement pause functionality
            self.status_var.set("Analysis paused")
            self.pause_button.configure(text="Resume")
        else:
            # Implement resume functionality
            self.status_var.set("Analysis resumed")
            self.pause_button.configure(text="Pause")
    
    def save_report(self):
        if not self.report_area.get(1.0, tk.END).strip():
            messagebox.showwarning("Warning", "No report to save")
            return
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"surveillance_analysis_{timestamp}.md"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.report_area.get(1.0, tk.END))
                self.status_var.set(f"Report saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save report: {str(e)}")
    
    def show_settings(self):
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.master)
        
        # Create settings form
        settings_frame = ttk.LabelFrame(settings_window, text="Analysis Configuration")
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # LLM Model
        ttk.Label(settings_frame, text="LLM Model:").grid(row=0, column=0, padx=5, pady=5)
        llm_entry = ttk.Entry(settings_frame)
        llm_entry.insert(0, self.config.llm_model)
        llm_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Country
        ttk.Label(settings_frame, text="Country:").grid(row=1, column=0, padx=5, pady=5)
        country_entry = ttk.Entry(settings_frame)
        country_entry.insert(0, self.config.country)
        country_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Search Results
        ttk.Label(settings_frame, text="Search Results:").grid(row=2, column=0, padx=5, pady=5)
        results_entry = ttk.Entry(settings_frame)
        results_entry.insert(0, str(self.config.search_results))
        results_entry.grid(row=2, column=1, padx=5, pady=5)
    
    def show_about(self):
        about_text = """George Was Right - CrewAI Analysis System
        
Version: 2.0
        
An AI-powered analysis system examining modern surveillance through the lens of George Orwell's "1984".
        
        2024 TheRealFredP3D"""
        
        messagebox.showinfo("About", about_text)

if __name__ == "__main__":
    root = tk.Tk()
    gui = CrewAI_GUI(root)
    root.mainloop()
