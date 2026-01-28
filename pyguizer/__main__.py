"""
PyGUIzer Main Entry Point

This file handles direct execution of PyGUIzer as a module:
python -m pyguizer package your_app.py
"""

import sys
import subprocess
import os

def main():
    """Main entry point for PyGUIzer module execution."""
    if len(sys.argv) < 2:
        # No command provided, run the default PyGUIzer application
        run_default_app()
        return
    
    # Check if the first argument is a command or a flag
    first_arg = sys.argv[1]
    if first_arg.startswith("-"):
        # First argument is a flag, run default app with arguments
        run_default_app()
        return
    
    command = first_arg
    args = sys.argv[2:]
    
    if command == "package":
        handle_package(args)
    elif command == "run" or command == "init":
        # For other commands, run the CLI directly
        from pyguizer.cli import app
        # Create a new sys.argv with the command as the first argument
        new_argv = [sys.argv[0]] + [command] + args
        sys.argv = new_argv
        sys.exit(app())
    else:
        print(f"Error: Unknown command '{command}'")
        print("\nAvailable commands:")
        print("  run      Run a PyGUIzer application")
        print("  init     Initialize a new PyGUIzer project")
        print("  package  Package a PyGUIzer application into a standalone executable")
        sys.exit(1)


def run_default_app():
    """Run the default PyGUIzer application."""
    # This is used when running `python -m pyguizer` without a command
    # It will run the PyGUIzer CLI with the run command, using the current directory
    from pyguizer.cli import app
    
    # Check for common PyGUIzer app files in the current directory
    app_files = ['app.py', 'main.py']
    found_app_file = None
    
    for app_file in app_files:
        if os.path.exists(app_file):
            found_app_file = app_file
            break
    
    if found_app_file:
        # Create a new sys.argv with the run command and the found app file
        new_argv = [sys.argv[0], "run", found_app_file]
        # Add any additional arguments
        if len(sys.argv) > 1:
            new_argv.extend(sys.argv[1:])
        sys.argv = new_argv
        sys.exit(app())
    else:
        # No app file found, run the CLI to show help
        print("No PyGUIzer application found in the current directory.")
        print("Please create an app.py file with PyGUIzer-decorated functions, or specify a file to run.")
        print("\nUsage: python -m pyguizer run <file_path>")
        print("\nFor example:")
        print("  python -m pyguizer run app.py")
        print("\nTo create a new PyGUIzer project:")
        print("  python -m pyguizer init my_project")
        sys.exit(1)


def handle_package(args):
    """Handle the package command."""
    if len(args) < 1:
        print("Usage: python -m pyguizer package <file_path> [--name NAME] [--output_dir DIR] [--onefile True/False] [--windowed True/False]")
        sys.exit(1)
    
    file_path = args[0]
    
    # Get the path to the deployment script
    deploy_script = os.path.join(os.path.dirname(__file__), "../scripts/deploy.py")
    
    # Run the deployment script with the same arguments
    result = subprocess.run([sys.executable, deploy_script] + args, check=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
