"""Dependency injection functions for PyGUIzer"""

from pyguizer.api.services.pyguizer_app import PyGUIzerApp
from pyguizer.api.services.task_manager import TaskManager


def get_pyguizer_app():
    """Get the PyGUIzerApp instance"""
    # Create a default instance
    return PyGUIzerApp()


def get_task_manager():
    """Get the TaskManager instance"""
    return TaskManager()
