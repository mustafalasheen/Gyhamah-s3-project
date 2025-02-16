import threading
import time
import os
import numpy as np
from mss import mss
import sounddevice as sd
import soundfile as sf
import subprocess
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from pynput import keyboard

class ScreenRecorder:
    """Core screen recording functionality"""
    
    def __init__(self):
        self.recording = False
        self.paused = False
        self.frames = []
        self.audio_frames = []
        self.fs = 44100
        self.audio_channels = 2
        self.audio_stream = None
        self.listener = None
        self.start_time = None
        self.end_time = None
        
        # Initialize MSS for each thread
        self._setup_directories()
        self._print_audio_devices()

    def _setup_directories(self):
        """Setup necessary directories for recording storage"""
        desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        self.output_folder = os.path.join(desktop_dir, "ScreenRecordings")
        self.temp_dir = os.path.join(self.output_folder, "temp")
        
        # Create directories if they don't exist
        for directory in [self.output_folder, self.temp_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def _print_audio_devices(self):
        """Print available audio devices"""
        print("Available audio devices:")
        print(sd.query_devices())

    def start_recording(self):
        """Start screen and audio recording"""
        if self.recording:
            return
            
        self.recording = True
        self.frames = []
        self.audio_frames = []
        self.start_time = time.time()
        
        # Start screen capture thread
        self.screen_thread = threading.Thread(target=self._capture_screen)
        self.screen_thread.start()
        
        # Start audio capture
        self.audio_stream = sd.InputStream(
            channels=self.audio_channels,
            samplerate=self.fs,
            callback=self._audio_callback
        )
        self.audio_stream.start()

    def _capture_screen(self):
        """Capture screen frames"""
        try:
            # Create new MSS instance in the thread
            with mss() as sct:
                # Get the primary monitor
                monitor = sct.monitors[1]  # Primary monitor
                
                while self.recording and not self.paused:
                    try:
                        screenshot = sct.grab(monitor)
                        frame = np.array(screenshot)
                        self.frames.append(frame)
                        time.sleep(1/30)  # 30 FPS
                    except Exception as e:
                        print(f"Frame capture error: {str(e)}")
                        break
        except Exception as e:
            print(f"Screen capture error: {str(e)}")

    def _audio_callback(self, indata, frames, time_info, status):
        """Callback for audio capture"""
        if self.recording and not self.paused:
            self.audio_frames.append(indata.copy())

    def pause_recording(self):
        """Pause the recording"""
        self.paused = True

    def resume_recording(self):
        """Resume the recording"""
        self.paused = False

    def stop_recording(self):
        """Stop recording and save the file"""
        if not self.recording:
            return None
            
        self.recording = False
        self.end_time = time.time()
        
        if self.audio_stream:
            self.audio_stream.stop()
            self.audio_stream.close()
        
        # Wait for screen capture thread to finish
        if hasattr(self, 'screen_thread'):
            self.screen_thread.join()
        
        # Generate timestamp for filename
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_path = os.path.join(self.output_folder, f"recording_{timestamp}.mp4")
        
        # Create video from frames
        if self.frames:
            clip = ImageSequenceClip(self.frames, fps=30)
            
            # Save audio if captured
            if self.audio_frames:
                audio_data = np.concatenate(self.audio_frames, axis=0)
                audio_path = os.path.join(self.temp_dir, "temp_audio.wav")
                sf.write(audio_path, audio_data, self.fs)
                
                # Combine video and audio
                clip.write_videofile(
                    output_path,
                    codec='libx264',
                    audio=audio_path,
                    fps=30
                )
                
                # Clean up temp audio file
                if os.path.exists(audio_path):
                    os.remove(audio_path)
            else:
                # Save video without audio
                clip.write_videofile(
                    output_path,
                    codec='libx264',
                    fps=30
                )
        
        # Clear recorded data
        self.frames = []
        self.audio_frames = []
        
        return output_path

    # ... (rest of the ScreenRecorder methods) 