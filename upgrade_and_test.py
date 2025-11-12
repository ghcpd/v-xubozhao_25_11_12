"""
Main script to run the complete upgrade and testing process.
Tracks start and end times for the entire process.
"""
import subprocess
import sys
import os
from datetime import datetime
import time


def run_command(command, description):
    """Run a shell command and return success status."""
    print(f"\n{'='*60}")
    print(f"Step: {description}")
    print(f"{'='*60}")
    print(f"Command: {command}")
    print()
    
    try:
        if sys.platform == "win32":
            result = subprocess.run(command, shell=True, check=True, 
                                  capture_output=False, text=True)
        else:
            result = subprocess.run(command, shell=True, check=True, 
                                  capture_output=False, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False


def main():
    """Main execution function."""
    start_time = datetime.now()
    start_timestamp = start_time.strftime("%Y-%m-%d %H:%M:%S")
    
    print("\n" + "="*60)
    print("DEPENDENCY UPGRADE AND VALIDATION PROCESS")
    print("="*60)
    print(f"Process started at: {start_timestamp}")
    print("="*60)
    
    # Determine shell script execution method
    if sys.platform == "win32":
        setup_cmd = "bash setup.sh" if os.path.exists("bash.exe") else "setup.sh"
        test_cmd = "bash run_tests.sh" if os.path.exists("bash.exe") else "run_tests.sh"
    else:
        setup_cmd = "bash setup.sh"
        test_cmd = "bash run_tests.sh"
    
    steps = [
        (setup_cmd, "Setting up environment and installing dependencies"),
        (test_cmd, "Running tests with coverage"),
    ]
    
    success = True
    for cmd, desc in steps:
        if not run_command(cmd, desc):
            print(f"\n❌ Failed at step: {desc}")
            success = False
            break
        print(f"\n✅ Completed: {desc}")
    
    end_time = datetime.now()
    end_timestamp = end_time.strftime("%Y-%m-%d %H:%M:%S")
    duration = end_time - start_time
    
    print("\n" + "="*60)
    print("PROCESS SUMMARY")
    print("="*60)
    print(f"Start time: {start_timestamp}")
    print(f"End time: {end_timestamp}")
    print(f"Total duration: {duration}")
    print("="*60)
    
    if success:
        print("\n✅ All steps completed successfully!")
        return 0
    else:
        print("\n❌ Process completed with errors.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

