import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import webbrowser

class HeaderSection:
    """Header section of the GUI"""
    
    def __init__(self, parent):
        self.parent = parent
        self._create_widgets()

    def _create_widgets(self):
        # Title with better styling
        self.title_frame = ttk.Frame(self.parent)
        self.title_frame.pack(pady=10, fill=X)
        
        self.title_label = ttk.Label(
            self.title_frame,
            text="Screen Recorder Pro",
            font=("Helvetica", 24, "bold"),
            bootstyle="inverse-primary"
        )
        self.title_label.pack(pady=(0, 10))
        
        # Status with colored indicators
        self.status_frame = ttk.Frame(self.parent)
        self.status_frame.pack(fill=X, pady=5)
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="Status: Ready",
            font=("Helvetica", 12),
            bootstyle="inverse-secondary"
        )
        self.status_label.pack(side=LEFT, padx=5)
        
        self.duration_label = ttk.Label(
            self.status_frame,
            text="Duration: 00:00:00",
            font=("Helvetica", 12),
            bootstyle="inverse-info"
        )
        self.duration_label.pack(side=RIGHT, padx=5)

    def update_status(self, status, style="secondary"):
        """Update status with appropriate color"""
        self.status_label.configure(
            text=f"Status: {status}",
            bootstyle=f"inverse-{style}"
        )

class ControlButtons:
    """Control buttons section"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self._create_widgets()

    def _create_widgets(self):
        self.buttons_frame = ttk.Frame(self.parent)
        self.buttons_frame.pack(pady=20)
        
        # Start button with icon
        self.start_button = ttk.Button(
            self.buttons_frame,
            text="Start Recording (F9)",
            bootstyle="success-outline",
            command=self.app.start_recording,
            width=20
        )
        self.start_button.pack(side=LEFT, padx=5)
        
        # Pause button with toggle state
        self.pause_button = ttk.Button(
            self.buttons_frame,
            text="Pause (F10)",
            bootstyle="warning-outline",
            command=self.app.toggle_pause,
            width=15,
            state=DISABLED
        )
        self.pause_button.pack(side=LEFT, padx=5)
        
        # Stop button with confirmation
        self.stop_button = ttk.Button(
            self.buttons_frame,
            text="Stop (F11)",
            bootstyle="danger-outline",
            command=self._confirm_stop,
            width=15,
            state=DISABLED
        )
        self.stop_button.pack(side=LEFT, padx=5)

    def _confirm_stop(self):
        """Confirm before stopping recording"""
        if Messagebox.yesno(
            title="Confirm Stop",
            message="Are you sure you want to stop recording?"
        ):
            self.app.stop_recording()

class FileInfoSection:
    """File information section"""
    
    def __init__(self, parent):
        self.parent = parent
        self._create_widgets()

    def _create_widgets(self):
        self.file_frame = ttk.LabelFrame(
            self.parent,
            text="Recording Details",
            padding=10
        )
        self.file_frame.pack(fill=X, pady=10)
        
        # File path with ellipsis for long paths
        self.file_path_var = ttk.StringVar(value="No recording saved yet")
        self.file_path_label = ttk.Label(
            self.file_frame,
            textvariable=self.file_path_var,
            font=("Consolas", 10)
        )
        self.file_path_label.pack(fill=X)
        
        # URL section with better layout
        self.url_frame = ttk.LabelFrame(
            self.file_frame,
            text="Share Link (Valid for 2 minutes)",
            padding=10
        )
        self.url_frame.pack(fill=X, pady=(10, 0))
        
        # URL display with copy feedback
        self.url_var = ttk.StringVar(value="No URL generated yet")
        self.url_entry = ttk.Entry(
            self.url_frame,
            textvariable=self.url_var,
            state="readonly",
            font=("Consolas", 10)
        )
        self.url_entry.pack(fill=X, expand=YES, pady=(0, 5))
        
        # Button frame
        self.button_frame = ttk.Frame(self.url_frame)
        self.button_frame.pack(fill=X)
        
        self.copy_button = ttk.Button(
            self.button_frame,
            text="Copy URL",
            command=self._copy_url,
            bootstyle="info-outline",
            width=15
        )
        self.copy_button.pack(side=LEFT, padx=2)
        
        self.open_button = ttk.Button(
            self.button_frame,
            text="Open in Browser",
            command=self._open_url,
            bootstyle="info-outline",
            width=15
        )
        self.open_button.pack(side=LEFT, padx=2)

    def _copy_url(self):
        """Copy URL with feedback"""
        url = self.url_var.get()
        if url != "No URL generated yet":
            self.parent.clipboard_clear()
            self.parent.clipboard_append(url)
            self.copy_button.configure(text="Copied!", bootstyle="success-outline")
            self.parent.after(1500, lambda: self.copy_button.configure(
                text="Copy URL",
                bootstyle="info-outline"
            ))

    def _open_url(self):
        url = self.url_var.get()
        if url != "No URL generated yet":
            webbrowser.open(url)

class LogSection:
    """Logging section"""
    
    def __init__(self, parent):
        self.parent = parent
        self._create_widgets()

    def _create_widgets(self):
        self.log_frame = ttk.LabelFrame(self.parent, text="Log", padding=10)
        self.log_frame.pack(fill=BOTH, expand=YES, pady=10)
        
        self.log_text = ttk.Text(
            self.log_frame,
            height=8,
            width=50,
            wrap=WORD,
            font=("Consolas", 10)
        )
        self.log_text.pack(fill=BOTH, expand=YES)
        
        scrollbar = ttk.Scrollbar(
            self.log_text,
            bootstyle="round",
            command=self.log_text.yview
        )
        scrollbar.pack(side=RIGHT, fill=Y)
        self.log_text.configure(yscrollcommand=scrollbar.set)

    def log(self, message):
        self.log_text.insert(END, f"{message}\n")
        self.log_text.see(END)

# ... (other component classes) 