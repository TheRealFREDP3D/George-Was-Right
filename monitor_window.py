import tkinter as tk
from tkinter import ttk, scrolledtext

class MonitorWindow:
    def __init__(self, root_window, title, window_type):
        """Initialize a monitor window.
        
        Args:
            root_window: The main window
            title: Window title
            window_type: Type of monitor ('agent', 'task', or 'tool')
        """
        self.window = tk.Toplevel(root_window)
        self.window.title(title)
        self.window_type = window_type

        # Nord theme colors
        self.nord_colors = {
            "bg": "#2E3440",  # Nord darker background
            "fg": "#D8DEE9",  # Nord foreground
            "accent": "#88C0D0",  # Nord blue
            "button_bg": "#3B4252",  # Nord darker blue
            "button_fg": "#ECEFF4",  # Nord lighter text
        }

        # Configure the window
        window_width = int(root_window.winfo_screenwidth() * 0.25)
        window_height = int(root_window.winfo_screenheight() * 0.4)
        self.window.geometry(f"{window_width}x{window_height}")
        self.window.configure(bg=self.nord_colors["bg"])

        # Create header
        header_frame = ttk.Frame(self.window)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        header_label = ttk.Label(
            header_frame,
            text=title,
            font=("Cascadia Code", 12, "bold"),
            background=self.nord_colors["bg"],
            foreground=self.nord_colors["accent"]
        )
        header_label.pack(side=tk.LEFT)

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
        self.output_area.tag_configure(
            "heading",
            font=("Cascadia Code", 11, "bold"),
            foreground="#81A1C1"  # Nord frost
        )
        self.output_area.tag_configure(
            "start",
            font=("Cascadia Code", 10, "bold"),
            foreground="#A3BE8C"  # Nord green
        )
        self.output_area.tag_configure(
            "process",
            font=("Cascadia Code", 10, "italic"),
            foreground="#B48EAD"  # Nord purple
        )
        self.output_area.tag_configure(
            "action",
            font=("Cascadia Code", 10),
            foreground="#EBCB8B"  # Nord yellow
        )
        self.output_area.tag_configure(
            "output",
            font=("Cascadia Code", 10),
            foreground="#88C0D0"  # Nord blue
        )
        self.output_area.tag_configure(
            "complete",
            font=("Cascadia Code", 10, "bold"),
            foreground="#A3BE8C"  # Nord green
        )
        self.output_area.tag_configure(
            "error",
            font=("Cascadia Code", 10, "bold"),
            foreground="#BF616A"  # Nord red
        )

        # Add to Report button
        self.add_report_button = ttk.Button(
            self.window,
            text="Add to Report",
            command=self.add_to_report,
            style="Nord.TButton",
            padding=5,
        )
        self.add_report_button.pack(pady=5)

        # Store content for report
        self.content = []

    def write(self, text, tags=None):
        """Write text to the monitor window with optional tags."""
        self.output_area.insert(tk.END, f"{text}\n", tags)
        self.output_area.see(tk.END)
        self.content.append((text, tags))

    def clear(self):
        """Clear the output area and content."""
        self.output_area.delete(1.0, tk.END)
        self.content.clear()

    def get_content_for_report(self):
        """Get formatted content for the report."""
        report_text = f"\n## {self.window.title()} Log\n\n"
        for text, tags in self.content:
            report_text += f"{text}\n"
        return report_text

    def add_to_report(self):
        """Add the monitor content to the main report."""
        # This will be connected to the main GUI's add_to_report method
