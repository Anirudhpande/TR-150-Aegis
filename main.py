#!/usr/bin/env python3
"""
AI-Driven Clinical Trial Matching Engine
Main entry point for the application
"""

import sys
import os
import subprocess
import time
import threading
from pathlib import Path

def start_backend():
    """Start the FastAPI backend server"""
    print("Starting backend server...")
    backend_path = Path(__file__).parent / "backend" / "api" / "main.py"
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "backend.api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ], cwd=Path(__file__).parent)
    except KeyboardInterrupt:
        print("Backend server stopped")

def start_frontend():
    """Start the Streamlit frontend"""
    print("Starting frontend dashboard...")
    time.sleep(3)  # Wait for backend to start
    
    frontend_path = Path(__file__).parent / "frontend" / "app.py"
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(frontend_path),
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("Frontend stopped")

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    requirements_path = Path(__file__).parent / "requirements.txt"
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_path)
        ], check=True)
        print("Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False
    
    # Download spaCy model
    try:
        subprocess.run([
            sys.executable, "-m", "spacy", "download", "en_core_web_sm"
        ], check=True)
        print("spaCy model downloaded successfully")
    except subprocess.CalledProcessError:
        print("spaCy model download failed, but continuing...")
    
    return True

def check_core_dependencies():
    """Check if core dependencies are available"""
    try:
        import fastapi
        import uvicorn
        import streamlit
        import pandas
        import numpy
        return True
    except ImportError:
        return False

def main():
    """Main function to run the application"""
    print("AI-Driven Clinical Trial Matching Engine")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "install":
            install_dependencies()
            return
        elif command == "backend":
            start_backend()
            return
        elif command == "frontend":
            start_frontend()
            return
        elif command == "help":
            print_help()
            return
    
    # Check if core dependencies are available
    if check_core_dependencies():
        print("Core dependencies found. Skipping installation.")
    else:
        print("Installing dependencies...")
        if not install_dependencies():
            return
    
    print("\nStarting both backend and frontend...")
    print("Backend will be available at: http://localhost:8000")
    print("Frontend will be available at: http://localhost:8501")
    print("\nPress Ctrl+C to stop both services")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Start frontend in main thread
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\nShutting down services...")

def print_help():
    """Print help information"""
    print("""
Usage: python main.py [command]

Commands:
    install     Install dependencies only
    backend     Start backend server only
    frontend    Start frontend only
    help        Show this help message
    
    (no command)  Install dependencies and start both services

Examples:
    python main.py              # Start everything
    python main.py install      # Install dependencies
    python main.py backend      # Start backend only
    python main.py frontend     # Start frontend only
    """)

if __name__ == "__main__":
    main()