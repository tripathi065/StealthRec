import os
from datetime import datetime

def create_recordings_directory():
    """Create a directory for storing recordings if it doesn't exist"""
    try:
        os.makedirs("recordings", exist_ok=True)
    except Exception as e:
        print(f"Error creating recordings directory: {str(e)}")

def get_timestamp():
    """Return current timestamp in readable format"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_command_keywords():
    """Get custom command keywords from user input"""
    print("\n=== Voice Command Setup ===")
    print("Please enter your preferred command words.")
    print("Commands should be simple, clear words that are easy to pronounce.")

    while True:
        sen_number = input("\nEnter Emergency Contact Number: ").strip().lower()
        start_command = input("Enter the word to START recording (default 'help'): ").strip().lower()
        stop_command = input("Enter the word to STOP recording (default 'stop'): ").strip().lower()

        # Use defaults if nothing entered
        start_command = start_command if start_command else "help"
        stop_command = stop_command if stop_command else "stop"
        sen_number = sen_number if sen_number else "+917300218689"

        # Validate commands are different
        if start_command == stop_command:
            print("\nError: Start and stop commands must be different words. Please try again.")
            continue

        print(f"\nCommands set:")
        print(f"- Say '{start_command}' to start recording")
        print(f"- Say '{stop_command}' to stop recording")
        print(f"- Send alert message to '{sen_number}' ")
        print("Are these commands correct? (yes/no)")

        if input().strip().lower().startswith('y'):
            return start_command, stop_command, sen_number

def print_instructions(start_command="help", stop_command="stop", sen_number="+917300218689"):
    """Print application instructions"""
    print("\n=== Voice-Activated Audio Recorder ===")
    print(f"Say '{start_command}' to start recording")
    print(f"Say '{stop_command}' to end recording")
    print(f"- Send alert message to '{sen_number}' ")
    print("Press Ctrl+C to exit the program")
    print("===================================")