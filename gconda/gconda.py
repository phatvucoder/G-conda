#!/usr/bin/env python3
"""
Module: gconda

This module provides helper functions for managing Conda environments and running commands
installed within those environments.

Main functions:
    - check_conda(): Check if Conda is installed.
    - check_python(): Check if Python is installed.
    - install_conda(): Install Conda using condacolab (suitable for Colab/Kaggle environments).
    - setup_env(python_version="3.10", env_name="python_env"):
          Create a new Conda environment with the specified Python version (default 3.10) and update
          symbolic links for python and pip. If Conda is not installed, it will prompt installation.
    - run_library_command(cmd_name, *args):
          Run a command from a pip-installed library (e.g., gdown). If the command is not found in PATH,
          it will attempt to locate it in the bin directory of the current Conda environment.
"""

import os
import shutil
import subprocess
import sys


def check_conda() -> bool:
    """
    Checks if Conda is installed and returns a message with the version if available.

    Returns:
        str: A status message indicating whether Conda is installed and its version.
    """
    conda_path = shutil.which("conda")
    if conda_path:
        try:
            version = subprocess.check_output(["conda", "--version"], text=True).strip()
            print(f"✅ Conda is installed. Version: {version}")
            return True
        except subprocess.CalledProcessError:
            print("⚠️ Conda is installed, but the version could not be retrieved.")
            return True
    else:
        print("❌ Conda is not installed.")
        return False


def check_python() -> bool:
    """
    Checks if Python is installed and returns a message with the version if available.

    Returns:
        str: A status message indicating whether Python is installed and its version.
    """
    python_path = shutil.which("python") or shutil.which("python3")  # Ensure compatibility across systems
    if python_path:
        try:
            version = subprocess.check_output(["python", "--version"], text=True).strip()
            print(f"✅ Python is installed. Version: {version}")
            return True
        except subprocess.CalledProcessError:
            "⚠️ Python is installed, but the version could not be retrieved."
            return True
    else:
        print("❌ Python is not installed.")
        return False


def install_conda():
    """
    Install Conda using condacolab (designed for Colab/Kaggle environments).

    Note:
        - Calling condacolab.install() may reset the environment, so subsequent commands might not execute.
        - If Conda is already installed, the function will notify and do nothing.
    """
    if check_conda():
        print("✅ Conda is already installed.")
        return

    print("ℹ️  Conda not found. Installing condacolab to install Conda...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "condacolab"], check=True)
    except subprocess.CalledProcessError as e:
        print("❌ Error installing condacolab:", e)
        raise

    try:
        import condacolab  # Import after installation
        condacolab.install()
        print("✅ Conda installation complete!")
    except Exception as e:
        print("❌ Error during condacolab.install():", e)
        raise


def fix_conda():
    """
    Automatically fix the error "ModuleNotFoundError: No module named 'conda'" by:
      - Checking the Conda path.
      - Removing the problematic Conda installation.
      - Reinstalling Conda.
    """
    conda_path = shutil.which("conda")
    if not conda_path:
        print("❌ Conda not found! Installing Conda...")
        install_conda()
        return

    print(f"ℹ️  Conda found at: {conda_path}")
    
    # Check if Conda is functioning correctly
    try:
        subprocess.run(["conda", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Conda is working properly!")
        return
    except subprocess.CalledProcessError:
        print("⚠️  Error: Conda is not functioning properly. Attempting to fix...")

    # Remove the problematic Conda installation
    print("🔧 Removing the problematic Conda...")
    subprocess.run(["sudo", "rm", "-f", conda_path], check=True)

    # Reinstall Conda
    print("🔄 Reinstalling Conda...")
    install_conda()

    # Verify Conda after repair
    try:
        subprocess.run(["conda", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Conda has been repaired successfully!")
    except subprocess.CalledProcessError:
        print("❌ Error: Conda is still not functioning! Please review the installation process.")


def setup_env(python_version: str = "3.10", env_name: str = "gconda"):
    """
    Create a new Conda environment with the specified Python version (default is 3.10) and update symbolic links
    for python and pip to switch the default environment.

    Steps:
      1. Check if Conda is installed. If not, prompt the user to install Conda.
      2. Create a new Conda environment with the given env_name.
      3. Determine the Conda base directory (via 'conda info --base').
      4. Identify the current python executable path and its directory.
      5. Remove existing symbolic links for python and pip (requires sudo privileges).
      6. Create new symbolic links pointing to the python and pip in the newly created environment.
      7. Verify the python and pip versions to confirm the environment switch.

    Raises:
        RuntimeError: If creating the Conda environment or updating symbolic links fails.
        EnvironmentError: If the python executable is not found in PATH.
    """
    if not check_conda():
        print("❌ Conda is not installed. Please run install_conda() and try again.")
        print("ℹ️  Automatically calling install_conda() to install Conda...")
        print("ℹ️  Note: This process may restart the kernel. If the environment is not set up, please run setup_env again.")
        install_conda()

    print(f"🚀 Creating new Conda environment '{env_name}' with Python {python_version}...")
    create_cmd = ["conda", "create", "-n", env_name, f"python={python_version}", "ipython", "-y"]
    result = subprocess.run(create_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("❌ Error creating Conda environment:")
        print(result.stderr)
        raise RuntimeError("Failed to create Conda environment.")
    else:
        print(f"✅ Environment '{env_name}' created successfully!")

    # Determine the Conda base directory
    try:
        base_dir = subprocess.check_output(["conda", "info", "--base"], text=True).strip()
    except subprocess.CalledProcessError as e:
        print("❌ Unable to determine Conda base directory:", e)
        raise

    # Get current python path and its directory
    python_path = shutil.which("python")
    if python_path is None:
        raise EnvironmentError("❌ Python executable not found in PATH.")
    python_dir = os.path.dirname(python_path)

    # Paths to python and pip in the new environment
    new_python = os.path.join(base_dir, "envs", env_name, "bin", "python3")
    new_pip = os.path.join(base_dir, "envs", env_name, "bin", "pip")

    print("🔧 Updating symbolic links for python and pip (requires sudo privileges)...")
    commands = [
        ["sudo", "rm", "-f", python_path],
        ["sudo", "rm", "-f", os.path.join(python_dir, "python3")],
        ["sudo", "rm", "-f", os.path.join(python_dir, "pip")],
        ["sudo", "ln", "-sf", new_python, python_path],
        ["sudo", "ln", "-sf", new_python, os.path.join(python_dir, "python3")],
        ["sudo", "ln", "-sf", new_pip, os.path.join(python_dir, "pip")],
    ]

    for cmd in commands:
        print("➡️  Executing command:", " ".join(cmd))
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print("❌ Error executing command:", " ".join(cmd))
            print("stderr:", res.stderr)
            raise RuntimeError(f"Command {' '.join(cmd)} failed.")

    print("✅ Symbolic links updated successfully!")
    print("ℹ️  Verifying updated python and pip versions:")
    subprocess.run(["python", "--version"])
    subprocess.run(["pip", "--version"])
    print(f"🎉 Python environment switched to '{env_name}' successfully!")


def run_library_command(cmd_name: str, *args):
    """
    Run a command from a pip-installed library that may not be recognized directly in the terminal.

    Workflow:
      - Attempt to run the command directly; if it is found in PATH, execute it.
      - If not found, determine the Conda base directory and current environment name from the CONDA_DEFAULT_ENV variable.
      - Build the full path to the command in the environment's bin directory and execute it.

    Example:
        run_library_command("gdown", "--version")
    
    Raises:
        EnvironmentError: If the current Conda environment cannot be determined.
        FileNotFoundError: If the command is not found in the current environment.
    """
    full_cmd = [cmd_name] + list(args)
    print("🚀 Attempting to run command:", " ".join(full_cmd))
    if shutil.which(cmd_name):
        subprocess.run(full_cmd)
        return

    # If command is not in PATH, attempt to find it in the current Conda environment
    try:
        base_dir = subprocess.check_output(["conda", "info", "--base"], text=True).strip()
    except subprocess.CalledProcessError as e:
        print("❌ Unable to determine Conda base directory:", e)
        raise

    current_env = os.environ.get("CONDA_DEFAULT_ENV")
    if not current_env:
        err_msg = (
            "❌ Current Conda environment could not be determined (CONDA_DEFAULT_ENV is not set). "
            "Please activate the desired environment."
        )
        print(err_msg)
        raise EnvironmentError(err_msg)

    env_bin = os.path.join(base_dir, "envs", current_env, "bin")
    cmd_path = os.path.join(env_bin, cmd_name)
    if os.path.exists(cmd_path):
        print(f"🚀 Running command from {cmd_path}")
        subprocess.run([cmd_path] + list(args))
    else:
        err_msg = f"❌ Command {cmd_name} not found in environment {current_env} at {env_bin}."
        print(err_msg)
        raise FileNotFoundError(err_msg)


# if __name__ == "__main__":
#     # Example usage: Check if Conda and Python are installed.
#     print("Checking Conda:", "Installed" if check_conda() else "Not installed")
#     print("Checking Python:", "Installed" if check_python() else "Not installed")
    
    # Uncomment the following lines to test specific functions:
    # install_conda()
    # setup_env(python_version="3.7", env_name="python310_env")
    # run_library_command("gdown", "--version")
