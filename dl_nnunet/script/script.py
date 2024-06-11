import json
import sys
from pathlib import Path
import subprocess

base_path = Path('./').resolve()

# File path for the configuration file
config_file_path = base_path / 'config.json'

def load_config():
    """Load the configuration file."""
    try:
        with open(config_file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_config(config):
    """Save the configuration file."""
    with open(config_file_path, 'w') as file:
        json.dump(config, file, indent=4)

def create_path_config():
    """Create initial path configuration."""
    config = {'input_path': '', 'output_path': ''}
    save_config(config)
    print("Path config created.")

def edit_path_config():
    """Edit path configurations."""
    config = load_config()
    input_path = input("Enter input path: ")
    output_path = input("Enter output path: ")
    config['input_path'] = input_path
    config['output_path'] = output_path
    save_config(config)
    print("Path config updated.")

def show_path_config():
    """Show current path configurations."""
    config = load_config()
    print(f"Input Path: {config.get('input_path', 'Not set')}")
    print(f"Output Path: {config.get('output_path', 'Not set')}")

def open_file():
    """Placeholder for opening a file."""
    print("Opening a file...")

def show_status():
    """Placeholder for showing status."""
    print("Showing status...")

def show_running_processes():
    # Run the 'qstat' command
    result = subprocess.run(['qstat'], capture_output=True, text=True)
    
    # Check if the command was executed successfully
    if result.returncode == 0:
        # Print the output of the command
        print("Running Job:")
        print(result.stdout)
    else:
        # If there was an error, print the error
        print("Error in running command:")
        print(result.stderr)

def close_program():
    """Close the program with confirmation."""
    confirmation = input("Are you sure you want to close the program? (yes/no): ").lower()
    if confirmation in ['yes', 'y']:
        print("Closing program.")
        sys.exit()
    else:
        print("Program will continue running.")


def main_menu():
    while True:
        print("\nWelcome Software")
        print("a) File")
        print("b) Edit")
        print("c) View")
        print("d) Help")
        print("============================")
        print("e) Show CCUB Running task")
        print("============================")
        print("f) add path config")
        print("g) show path config")
        print("============================")
        print("q) Exit Program")

        choice = input("Enter your choice (a-q): ").lower()

        if choice == 'a':
            open_file()
        elif choice == 'b':
            show_status()
        elif choice == 'c':
            show_running_processes()
        elif choice == 'd':
            close_program()
        elif choice == 'e':
            show_running_processes()
        elif choice == 'f':
            edit_path_config()
        elif choice == 'g':
            show_path_config()
        elif choice == 'q':
            close_program()
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main_menu()
