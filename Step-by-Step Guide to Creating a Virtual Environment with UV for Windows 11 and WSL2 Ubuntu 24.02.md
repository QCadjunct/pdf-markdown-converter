# Step-by-Step Guide to Creating a Virtual Environment with UV for Windows 11 and WSL2 Ubuntu 24.02

## **Windows 11**

1. **Install UV**:
   - Open PowerShell and run the following command to install UV:

     ```powershell
     powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```

   - Alternatively, you can install UV using pip:

     ```bash
     pip install uv
     ```

2. **Verify Installation**:
   - Check if UV is installed correctly by running:

     ```bash
     uv --version
     ```

3. **Initialize the Project**:
   - Navigate to your project directory and initialize UV:

     ```bash
     uv init
     ```

   - This command creates the necessary configuration files, including `pyproject.toml`.

4. **Create a Virtual Environment**:
   - Create a virtual environment:

     ```bash
     uv venv
     ```

   - To specify a Python version, use:

     ```bash
     uv venv --python 3.13
     ```

5. **Activate the Virtual Environment**:
   - Activate the virtual environment using:

     ```bash
     .venv\Scripts\activate
     ```

6. **Install Dependencies**:
   - Once the environment is active, install packages using UV’s pip interface:

     ```bash
     uv pip install requests
     ```

   - To add dependencies to your `pyproject.toml` file:

     ```bash
     uv add requests
     ```

7. **Sync Packages**:
   - To ensure your virtual environment matches the dependencies specified in your `pyproject.toml` and `uv.lock` files, run:

     ```bash
     uv sync
     ```

8. **Upgrade Packages**:
   - To upgrade a specific package to the latest version:

     ```bash
     uv pip install --upgrade package_name
     ```

   - To upgrade all packages to their latest versions:

     ```bash
     uv pip list --outdated
     uv pip install --upgrade package_name
     ```

9. **Force Reinstall Packages**:
   - To force reinstall a specific package:

     ```bash
     uv pip install <package_name> -U --force-reinstall
     ```

10. **Remove Packages**:
    - To remove a package from your environment:

      ```bash
      uv remove package_name
      ```

11. **Freeze Dependencies**:
    - Generate a list of installed dependencies:

      ```bash
      uv pip freeze > requirements.txt
      ```

12. **Deactivate and Remove Environments**:
    - Deactivate the virtual environment:

      ```bash
      uv deactivate
      ```

    - Remove the virtual environment:

      ```bash
      uv remove
      ```

13. **Build a Wheel**:
    - To create a wheel distribution for your project:

      ```bash
      uv build
      ```

## **WSL2 Ubuntu 24.02**

1. **Install UV**:
   - Open your WSL2 terminal and run the following command to install UV:

     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```

   - Alternatively, you can install UV using pip:

     ```bash
     pip install uv
     ```

2. **Verify Installation**:
   - Check if UV is installed correctly by running:

     ```bash
     uv --version
     ```

3. **Initialize the Project**:
   - Navigate to your project directory and initialize UV:

     ```bash
     uv init
     ```

   - This command creates the necessary configuration files, including `pyproject.toml`.

4. **Create a Virtual Environment**:
   - Create a virtual environment:

     ```bash
     uv venv
     ```

   - To specify a Python version, use:

     ```bash
     uv venv --python 3.13
     ```

5. **Activate the Virtual Environment**:
   - Activate the virtual environment using:

     ```bash
     source .venv/bin/activate
     ```

6. **Install Dependencies**:
   - Once the environment is active, install packages using UV’s pip interface:

     ```bash
     uv pip install requests
     ```

   - To add dependencies to your `pyproject.toml` file:

     ```bash
     uv add requests
     ```

7. **Sync Packages**:
   - To ensure your virtual environment matches the dependencies specified in your `pyproject.toml` and `uv.lock` files, run:

     ```bash
     uv sync
     ```

8. **Upgrade Packages**:
   - To upgrade a specific package to the latest version:

     ```bash
     uv pip install --upgrade package_name
     ```

   - To upgrade all packages to their latest versions:

     ```bash
     uv pip list --outdated
     uv pip install --upgrade package_name
     ```

9. **Force Reinstall Packages**:
   - To force reinstall a specific package:

     ```bash
     uv pip install <package_name> -U --force-reinstall
     ```

10. **Remove Packages**:
    - To remove a package from your environment:

      ```bash
      uv remove package_name
      ```

11. **Freeze Dependencies**:
    - Generate a list of installed dependencies:

      ```bash
      uv pip freeze > requirements.txt
      ```

12. **Deactivate and Remove Environments**:
    - Deactivate the virtual environment:dir

      ```bash
      uv deactivate
      ```

    - Remove the virtual environment:

      ```bash
      uv remove
      ```

13. **Build a Wheel**:
    - To create a wheel distribution for your project:

      ```bash
      uv build
      ```

By following these steps, you can efficiently manage Python virtual environments using UV on both Windows 11 and WSL2 Ubuntu 24.02.

### Documentation

1. [UV documentation](https://docs.astral.sh/uv/)
1. [Youtube UV for Python… (Almost) All Batteries Included](https://www.youtube.com/watch?v=qh98qOND6MI)
1. [Youtube How Much FASTER Is Python 3.13 Without the GIL?](https://www.youtube.com/watch?v=zWPe_CUR4yU)