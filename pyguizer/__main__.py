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
        print("Usage: python -m pyguizer <command> [<args>]")
        print("\nAvailable commands:")
        print("  run      Run a PyGUIzer application")
        print("  init     Initialize a new PyGUIzer project")
        print("  package  Package a PyGUIzer application into a standalone executable")
        sys.exit(1)
    
    command = sys.argv[1]
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
