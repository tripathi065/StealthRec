import sys
import signal
from audio_recorder import AudioRecorder
from voice_detector import VoiceDetector
from utils import print_instructions, create_recordings_directory, get_command_keywords

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\nExiting program...")
    sys.exit(0)

def main():
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Create recordings directory
    create_recordings_directory()

    try:
        # Get custom command keywords from user
        start_command, stop_command, sen_number = get_command_keywords()

        # Initialize components
        print("\nInitializing voice detector...")
        detector = VoiceDetector(start_command=start_command, stop_command=stop_command, sen_number=sen_number)
        print("Voice detector initialized successfully.")

        print("\nInitializing audio recorder...")
        recorder = AudioRecorder()
        print("Audio recorder initialized successfully.")

        # Print instructions with custom commands
        print_instructions(start_command, stop_command, sen_number)

        # Main application loop
        recording_in_progress = False

        while True:
            try:
                # Listen for commands
                command = detector.listen_for_command()

                if command == "start" and not recording_in_progress:
                    # Start recording
                    if recorder.start_recording():
                        recording_in_progress = True
                        print(f"\nRecording started! Say '{stop_command}' to end recording.")
                elif command == "stop" and recording_in_progress:
                    # Stop recording
                    filename = recorder.stop_recording()
                    if filename:
                        recording_in_progress = False
                        print(f"\nReady for next command... (Say '{start_command}' to start a new recording)")

            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
                if recording_in_progress:
                    recorder.stop_recording()
                    recording_in_progress = False
                print("\nRestarting voice detection...")

    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        print("Please ensure you have a working microphone connected and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()