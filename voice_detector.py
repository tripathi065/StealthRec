import speech_recognition as sr
from messaging import send_alert_message
from utils import get_command_keywords
from datetime import datetime
import sys

class VoiceDetector:
    def __init__(self, start_command="help", stop_command="stop", sen_number="+917300218689"):
        self.recognizer = sr.Recognizer()
        self.start_command = start_command.lower()
        self.stop_command = stop_command.lower()
        self.sen_number  = sen_number.lower()
        self.simulation_mode = False
        try:
            # Try to initialize microphone
            self.microphone = sr.Microphone()
            # Adjust for ambient noise
            with self.microphone as source:
                print("\nCalibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Microphone calibrated.")
        except (OSError, sr.RequestError) as e:
            print("\nError initializing microphone:")
            print("Please ensure you have a working microphone connected.")
            print(f"Technical details: {str(e)}")
            print("\nEntering simulation mode.")
            self.simulation_mode = True

    def _send_recording_alert(self):
        """Send alert message when recording spythontarts"""
        try:
            mode_info = " (Simulation)" if self.simulation_mode else ""
            alert_message = f"recorder activated{mode_info}"
            print(f"\nAttempting to send alert message: {alert_message}")
            if send_alert_message(self.sen_number, alert_message):
                print("\nEmergency contact alert sent successfully!")
            else:
                print("\nWarning: Could not send emergency contact alert.")
        except Exception as e:
            print(f"\nWarning: Failed to send alert message: {str(e)}")

    def listen_for_command(self):
        """Listen for commands and return the detected command"""
        if self.simulation_mode:
            # Check if running in an interactive environment
            if sys.stdin.isatty():
                print(f"\nSimulation Mode: Enter command manually ('{self.start_command}' or '{self.stop_command}'):")
                try:
                    user_input = input().strip().lower()
                    print(f"\nReceived manual input: '{user_input}'")
                except EOFError:
                    print("\nNon-interactive environment detected, using default command...")
                    user_input = self.start_command
                    print(f"\nUsing default start command: '{user_input}'")
            else:
                print("\nNon-interactive environment detected, using default command...")
                user_input = self.start_command
                print(f"\nUsing default start command: '{user_input}'")

            if user_input == self.start_command:
                print("Start command detected! (Simulation)")
                self._send_recording_alert()
                return "start"
            elif user_input == self.stop_command:
                print("Stop command detected! (Simulation)")
                return "stop"
            return None

        try:
            with self.microphone as source:
                print(f"\nListening for commands ('{self.start_command}' to start, '{self.stop_command}' to end)...")
                # Shorter timeout and phrase time limit for more responsive detection
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=2)

                try:
                    # Use Google Speech Recognition
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"Detected: {text}")

                    # Check for specific commands
                    if self.start_command in text:
                        print("Start command detected!")
                        self._send_recording_alert()
                        return "start"
                    elif self.stop_command in text:
                        print("Stop command detected!")
                        return "stop"
                    return None

                except sr.UnknownValueError:
                    print("Could not understand audio")
                    return None
                except sr.RequestError as e:
                    print(f"\nCould not request results from speech recognition service; {e}")
                    return None

        except Exception as e:
            print(f"\nError in voice detection: {str(e)}")
            return None