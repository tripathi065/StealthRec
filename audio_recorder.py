import pyaudio
import wave
import threading
import os
from datetime import datetime
import time  # Added for simulation mode

class AudioRecorder:
    def __init__(self):
        self.is_simulation_mode = False
        try:
            self.audio = pyaudio.PyAudio()
            # Get default input device info
            device_count = self.audio.get_host_api_info_by_index(0).get('deviceCount')
            if device_count == 0:
                print("\nNo audio input devices found. Entering simulation mode.")
                self._setup_simulation_mode()
            else:
                # Try to use the default input device
                try:
                    default_input = self.audio.get_default_input_device_info()
                    print(f"\nUsing audio input device: {default_input.get('name')}")
                except Exception:
                    print("\nCould not access audio device. Entering simulation mode.")
                    self._setup_simulation_mode()
        except Exception as e:
            print(f"\nWarning: Error initializing audio system: {str(e)}")
            print("Entering simulation mode.")
            self._setup_simulation_mode()

        self.stream = None
        self.frames = []
        self.is_recording = False
        self.sample_rate = 44100
        self.chunk_size = 1024
        self.channels = 1
        self.format = pyaudio.paInt16
        self._recording_thread = None
        self.simulation_start_time = None

    def _setup_simulation_mode(self):
        """Set up simulation mode for testing"""
        self.is_simulation_mode = True
        self.audio = pyaudio.PyAudio()
        self.sample_rate = 44100
        self.channels = 1
        self.format = pyaudio.paInt16
        print("Recording simulation mode active - no actual audio will be captured.")

    def start_recording(self):
        """Start audio recording or simulation"""
        if self.is_recording:
            print("\nAlready recording...")
            return False

        self.is_recording = True
        self.frames = []

        if self.is_simulation_mode:
            self.simulation_start_time = time.time()
            print("\nSimulated recording started...")
            return True

        try:
            # Configure and open audio stream
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )

            # Start recording thread
            self._recording_thread = threading.Thread(target=self._record)
            self._recording_thread.start()
            print("\nRecording started...")
            return True
        except Exception as e:
            print(f"\nError starting recording: {str(e)}")
            self.is_recording = False
            return False

    def _record(self):
        """Internal method to record audio or simulate recording"""
        if self.is_simulation_mode:
            while self.is_recording:
                # Simulate recording by generating silent frames
                self.frames.append(b'\x00' * self.chunk_size * 2)  # 2 bytes per sample
                time.sleep(self.chunk_size / self.sample_rate)  # Simulate real-time recording
        else:
            while self.is_recording and self.stream:
                try:
                    data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                    self.frames.append(data)
                except Exception as e:
                    print(f"\nError during recording: {str(e)}")
                    self.stop_recording()
                    break

    def stop_recording(self):
        """Stop the audio recording/simulation and save to file"""
        if not self.is_recording:
            print("\nNo active recording to stop.")
            return None

        try:
            self.is_recording = False

            if self.is_simulation_mode and self.simulation_start_time is not None:
                # Calculate simulated recording duration
                duration = time.time() - self.simulation_start_time
                print(f"\nSimulated recording stopped after {duration:.1f} seconds")
            else:
                # Wait for recording thread to finish
                if self._recording_thread and self._recording_thread.is_alive():
                    self._recording_thread.join(timeout=2.0)

                if self.stream:
                    self.stream.stop_stream()
                    self.stream.close()
                    self.stream = None

            if not self.frames:
                print("\nNo audio data recorded.")
                return None

            # Generate filename with timestamp in recordings directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join("recordings", f"recording_{timestamp}.wav")

            # Save the recording
            self._save_recording(filename)
            print(f"\nRecording saved as: {filename}")
            return filename
        except Exception as e:
            print(f"\nError stopping recording: {str(e)}")
            return None

    def _save_recording(self, filename):
        """Save the recorded audio to a WAV file"""
        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(self.frames))
        except Exception as e:
            print(f"\nError saving recording: {str(e)}")

    def __del__(self):
        """Cleanup when object is destroyed"""
        if self.is_recording:
            self.stop_recording()
        if self.stream:
            self.stream.close()
        self.audio.terminate()