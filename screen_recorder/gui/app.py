import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import threading
import time
from .components import (
    HeaderSection,
    ControlButtons,
    FileInfoSection,
    LogSection
)
from ..core.recorder import ScreenRecorder
from ..core.s3_uploader import S3Uploader

class ScreenRecorderGUI:
    """Main GUI application class"""
    
    def __init__(self):
        self.root = self._setup_window()
        self.recorder = ScreenRecorder()
        self.s3_uploader = S3Uploader()
        self._init_state()
        self._create_gui()
        self._create_key_bindings()

        # Ensure cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _setup_window(self):
        """Setup main window with theme"""
        return ttk.Window(
            title="Screen Recorder Pro",
            themename="darkly",
            size=(800, 600),
            resizable=(False, False)
        )

    def _init_state(self):
        """Initialize application state"""
        self.is_recording = False
        self.is_paused = False
        self.current_file_path = None
        self.current_url = None
        self.recording_start_time = None
        self.pause_start_time = None
        self.total_pause_time = 0

    def _create_gui(self):
        """Create main GUI elements"""
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=BOTH, expand=YES)

        self.header = HeaderSection(self.main_frame)
        self.controls = ControlButtons(self.main_frame, self)
        self.file_info = FileInfoSection(self.main_frame)
        self.log_section = LogSection(self.main_frame)

    def _create_key_bindings(self):
        """Setup keyboard shortcuts"""
        self.root.bind("<F9>", lambda e: self.start_recording())
        self.root.bind("<F10>", lambda e: self.toggle_pause())
        self.root.bind("<F11>", lambda e: self.stop_recording())

    def start_recording(self):
        """Start recording"""
        if not self.is_recording:
            try:
                self.is_recording = True
                self.recording_start_time = time.time()
                self.recorder.start_recording()
                
                self.controls.start_button.configure(state=DISABLED)
                self.controls.pause_button.configure(state=NORMAL)
                self.controls.stop_button.configure(state=NORMAL)
                
                self.header.status_label.configure(text="Status: Recording")
                self.log_section.log("Recording started")
                self._update_duration()
                
            except Exception as e:
                self.handle_error(f"Failed to start recording: {str(e)}")

    def stop_recording(self):
        """Stop recording"""
        if self.is_recording:
            try:
                self.is_recording = False
                self.is_paused = False
                
                self.header.status_label.configure(text="Status: Processing...")
                self.log_section.log("Stopping recording...")
                
                def process_recording():
                    try:
                        video_path = self.recorder.stop_recording()
                        if video_path:
                            self.current_file_path = video_path
                            self.root.after(0, lambda: self.file_info.file_path_var.set(f"File: {video_path}"))
                            
                            # Upload to S3
                            self.log_section.log("Uploading to S3...")
                            url = self.s3_uploader.upload_file(video_path)
                            if url:
                                self.current_url = url
                                self.root.after(0, lambda: self.file_info.url_var.set(url))
                                
                        self.root.after(0, self._reset_ui)
                        
                    except Exception as e:
                        # Use a local variable for the error message
                        error_msg = str(e)
                        self.root.after(0, lambda: self.handle_error(error_msg))
                
                threading.Thread(target=process_recording).start()
                
            except Exception as e:
                self.handle_error(f"Failed to stop recording: {str(e)}")

    def toggle_pause(self):
        """Toggle pause/resume recording"""
        if not self.is_recording:
            return
            
        try:
            if self.is_paused:
                self.recorder.resume_recording()
                self.is_paused = False
                if self.pause_start_time:
                    self.total_pause_time += time.time() - self.pause_start_time
                self.pause_start_time = None
                self.controls.pause_button.configure(text="Pause (F10)")
                self.header.status_label.configure(text="Status: Recording")
                self.log_section.log("Recording resumed")
                self._update_duration()
            else:
                self.recorder.pause_recording()
                self.is_paused = True
                self.pause_start_time = time.time()
                self.controls.pause_button.configure(text="Resume (F10)")
                self.header.status_label.configure(text="Status: Paused")
                self.log_section.log("Recording paused")
                
        except Exception as e:
            self.handle_error(f"Failed to toggle pause: {str(e)}")

    def _update_duration(self):
        """Update the duration display"""
        if self.is_recording and self.recording_start_time:
            current_time = time.time()
            elapsed = current_time - self.recording_start_time - self.total_pause_time
            
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            
            self.header.duration_label.configure(
                text=f"Duration: {hours:02d}:{minutes:02d}:{seconds:02d}"
            )
            
            if not self.is_paused:
                self.root.after(1000, self._update_duration)

    def _reset_ui(self):
        """Reset UI elements to initial state"""
        self.controls.start_button.configure(state=NORMAL)
        self.controls.pause_button.configure(state=DISABLED)
        self.controls.stop_button.configure(state=DISABLED)
        self.header.status_label.configure(text="Status: Ready")
        self.header.duration_label.configure(text="Duration: 00:00:00")
        self.log_section.log("Recording completed")

    def handle_error(self, error_message):
        """Handle errors during recording"""
        self.log_section.log(f"Error: {error_message}")
        self.header.status_label.configure(text="Status: Error")
        self._reset_ui()
        Messagebox.show_error(
            title="Error",
            message=f"An error occurred: {error_message}"
        )

    def _on_closing(self):
        """Handle application cleanup on closing"""
        if self.is_recording:
            self.stop_recording()
        self.root.destroy()

    def run(self):
        """Start the GUI application"""
        self.root.mainloop() 