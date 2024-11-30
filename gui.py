import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from datetime import datetime
import json
import os
from main import Config, AgentFactory, TaskManager, LLM
from crewai import Crew

class CrewAI_GUI:
    def __init__(self, master):
        self.master = master
        master.title("George Was Right - AI Analysis System")
        
        # Configure the main window
        master.geometry("1200x800")
        master.minsize(800, 600)
        
        # Create main frames
        self.create_frames()
        self.create_menu()
        self.create_status_bar()
        
        # Initialize state
        self.config = Config()
        self.is_running = False
        self.current_task = None
        
        # Load initial data
        self.initialize_data()

    def create_frames(self):
        # Create left panel for controls
        left_frame = ttk.Frame(self.master, padding="5")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Agent section
        ttk.Label(left_frame, text="Agents", font=('Helvetica', 12, 'bold')).pack(anchor=tk.W)
        self.agent_list = ttk.Treeview(left_frame, height=5)
        self.agent_list["columns"] = ("Role", "Status")
        self.agent_list.column("#0", width=0, stretch=tk.NO)
        self.agent_list.column("Role", width=100)
        self.agent_list.column("Status", width=100)
        self.agent_list.heading("Role", text="Role")
        self.agent_list.heading("Status", text="Status")
        self.agent_list.pack(fill=tk.X, pady=5)

        # Task section
        ttk.Label(left_frame, text="Tasks", font=('Helvetica', 12, 'bold')).pack(anchor=tk.W)
        self.task_list = ttk.Treeview(left_frame, height=5)
        self.task_list["columns"] = ("Description", "Status")
        self.task_list.column("#0", width=0, stretch=tk.NO)
        self.task_list.column("Description", width=150)
        self.task_list.column("Status", width=50)
        self.task_list.heading("Description", text="Description")
        self.task_list.heading("Status", text="Status")
        self.task_list.pack(fill=tk.X, pady=5)

        # Control buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_execution)
        self.start_button.pack(side=tk.LEFT, padx=2)
        
        self.pause_button = ttk.Button(button_frame, text="Pause", command=self.pause_execution, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=2)
        
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_execution, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=2)

        # Create right panel for output
        right_frame = ttk.Frame(self.master, padding="5")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Output section
        ttk.Label(right_frame, text="Execution Log", font=('Helvetica', 12, 'bold')).pack(anchor=tk.W)
        self.output_area = scrolledtext.ScrolledText(right_frame, height=15)
        self.output_area.pack(fill=tk.BOTH, expand=True, pady=5)

        # Report section
        ttk.Label(right_frame, text="Analysis Report", font=('Helvetica', 12, 'bold')).pack(anchor=tk.W)
        self.report_area = scrolledtext.ScrolledText(right_frame, height=15)
        self.report_area.pack(fill=tk.BOTH, expand=True, pady=5)

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Report", command=self.save_report)
        file_menu.add_command(label="Save Log", command=self.save_log)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Configure", command=self.show_settings)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_status_bar(self):
        self.status_bar = ttk.Label(self.master, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def initialize_data(self):
        # Clear existing items
        for item in self.agent_list.get_children():
            self.agent_list.delete(item)
        for item in self.task_list.get_children():
            self.task_list.delete(item)

        # Add agents
        self.agent_list.insert("", tk.END, values=("Researcher", "Ready"))
        self.agent_list.insert("", tk.END, values=("Writer", "Ready"))
        self.agent_list.insert("", tk.END, values=("Illustrator", "Ready"))

        # Add tasks
        self.task_list.insert("", tk.END, values=("Research Current Events", "Pending"))
        self.task_list.insert("", tk.END, values=("Analyze 1984 Parallels", "Pending"))
        self.task_list.insert("", tk.END, values=("Generate Illustrations", "Pending"))

    def start_execution(self):
        try:
            if not self.is_running:
                self.is_running = True
                self.update_status("Initializing CrewAI system...")
                
                # Initialize CrewAI components
                llm = LLM(model=self.config.llm_model)
                agent_factory = AgentFactory(llm)
                
                # Create agents
                agents = {
                    "researcher": agent_factory.create_researcher_agent(),
                    "writer": agent_factory.create_writer_agent(),
                    "illustrator": agent_factory.create_illustrator_agent(),
                }
                
                # Create tasks
                task_manager = TaskManager(agents)
                tasks = task_manager.create_tasks()
                
                # Create and configure crew
                self.crew = Crew(
                    agents=list(agents.values()),
                    tasks=tasks,
                    verbose=True,
                    llm=self.config.llm_model
                )
                
                # Update UI
                self.start_button.configure(state=tk.DISABLED)
                self.pause_button.configure(state=tk.NORMAL)
                self.stop_button.configure(state=tk.NORMAL)
                
                # Start execution in a separate thread
                self.master.after(100, self.execute_crew)
                
        except Exception as e:
            self.show_error(f"Error starting execution: {str(e)}")
            self.reset_execution()

    def execute_crew(self):
        try:
            # Run the crew
            result = self.crew.kickoff()
            
            # Update report area
            self.report_area.delete(1.0, tk.END)
            self.report_area.insert(tk.END, result)
            
            self.update_status("Analysis completed successfully")
            
        except Exception as e:
            self.show_error(f"Error during execution: {str(e)}")
        finally:
            self.reset_execution()

    def pause_execution(self):
        if self.is_running:
            # Implement pause functionality
            self.update_status("Execution paused")
            self.pause_button.configure(text="Resume")
        else:
            # Implement resume functionality
            self.update_status("Execution resumed")
            self.pause_button.configure(text="Pause")

    def stop_execution(self):
        if self.is_running:
            if messagebox.askyesno("Confirm Stop", "Are you sure you want to stop the execution?"):
                # Implement stop functionality
                self.reset_execution()
                self.update_status("Execution stopped")

    def reset_execution(self):
        self.is_running = False
        self.start_button.configure(state=tk.NORMAL)
        self.pause_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.DISABLED)
        self.initialize_data()

    def save_report(self):
        try:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".md",
                initialfile=filename,
                filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
            )
            if filepath:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(self.report_area.get(1.0, tk.END))
                self.update_status(f"Report saved to {filepath}")
        except Exception as e:
            self.show_error(f"Error saving report: {str(e)}")

    def save_log(self):
        try:
            filename = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                initialfile=filename,
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filepath:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(self.output_area.get(1.0, tk.END))
                self.update_status(f"Log saved to {filepath}")
        except Exception as e:
            self.show_error(f"Error saving log: {str(e)}")

    def show_settings(self):
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.master)
        
        # Add settings controls here
        ttk.Label(settings_window, text="LLM Model:").pack(pady=5)
        ttk.Entry(settings_window).pack(pady=5)
        
        ttk.Label(settings_window, text="Search Results:").pack(pady=5)
        ttk.Entry(settings_window).pack(pady=5)
        
        ttk.Label(settings_window, text="Country:").pack(pady=5)
        ttk.Entry(settings_window).pack(pady=5)
        
        ttk.Button(settings_window, text="Save", command=settings_window.destroy).pack(pady=20)

    def show_about(self):
        messagebox.showinfo(
            "About",
            "George Was Right - AI Analysis System\n\n"
            "A CrewAI-powered system for analyzing modern surveillance "
            "through the lens of Orwell's 1984.\n\n"
            "Version 2.0"
        )

    def show_error(self, message):
        messagebox.showerror("Error", message)
        self.update_status("Error occurred")

    def update_status(self, message):
        self.status_bar.config(text=message)
        self.output_area.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.output_area.see(tk.END)

def main():
    root = tk.Tk()
    app = CrewAI_GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
