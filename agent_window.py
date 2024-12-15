import tkinter as tk
from tkinter import ttk
from tkhtmlview import HTMLScrolledText
import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

class AgentWindow:
    def __init__(self, root_window, agent_name, agent_role):
        """Initialize an agent window.
        
        Args:
            root_window: The main window
            agent_name: Name of the agent (e.g., "researcher")
            agent_role: Role of the agent (e.g., "Research Specialist")
        """
        self.window = tk.Toplevel(root_window)
        self.window.title(f"Agent: {agent_role}")

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
        self.window.geometry(f"{window_width}x{window_height}")
        self.window.configure(bg=self.nord_colors["bg"])

        # Create header
        header_frame = ttk.Frame(self.window)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        header_label = ttk.Label(
            header_frame,
            text=f"{agent_role}",
            font=("Cascadia Code", 12, "bold"),
            background=self.nord_colors["bg"],
            foreground=self.nord_colors["accent"]
        )
        header_label.pack(side=tk.LEFT)

        # Create the status label
        self.status_label = ttk.Label(
            header_frame,
            text="Status: Idle",
            background=self.nord_colors["bg"],
            foreground=self.nord_colors["fg"]
        )
        self.status_label.pack(side=tk.RIGHT)

        # Create HTML viewer for markdown rendering
        self.html_viewer = HTMLScrolledText(
            self.window,
            html=self.get_initial_html(),
            background=self.nord_colors["bg"],
            foreground=self.nord_colors["fg"],
            font=("Cascadia Code", 10)
        )
        self.html_viewer.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Store markdown content
        self.markdown_content = []
        
        # Configure CSS for markdown rendering
        self.css = """
        <style>
            body {
                background-color: #2E3440;
                color: #D8DEE9;
                font-family: 'Cascadia Code', monospace;
                padding: 10px;
            }
            h3 {
                color: #88C0D0;
                margin-top: 20px;
                margin-bottom: 10px;
            }
            strong {
                color: #A3BE8C;
            }
            code {
                background-color: #3B4252;
                padding: 10px;
                display: block;
                border-radius: 5px;
                margin: 10px 0;
                white-space: pre-wrap;
            }
            hr {
                border: 1px solid #4C566A;
                margin: 20px 0;
            }
        </style>
        """

    def get_initial_html(self):
        """Get initial HTML content with styling."""
        return f"""
        <html>
        <head>
            <style>
                body {{
                    background-color: #2E3440;
                    color: #D8DEE9;
                    font-family: 'Cascadia Code', monospace;
                    padding: 10px;
                }}
            </style>
        </head>
        <body>
        </body>
        </html>
        """

    def write(self, text, tag=None):
        """Write text to the window with markdown rendering.
        
        Args:
            text: The markdown text to write
            tag: The type of content (for styling)
        """
        # Add the new markdown content
        self.markdown_content.append(text)
        
        # Convert markdown to HTML
        md_text = "\n".join(self.markdown_content)
        html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])
        
        # Add CSS and update the viewer
        full_html = f"<html><head>{self.css}</head><body>{html}</body></html>"
        self.html_viewer.set_html(full_html)
        
        # Scroll to bottom
        self.html_viewer.yview_moveto(1.0)

    def update_status(self, status):
        """Update the agent's status label."""
        self.status_label.config(text=f"Status: {status}")

    def clear(self):
        """Clear the output area."""
        self.markdown_content = []
        self.html_viewer.set_html(self.get_initial_html())
