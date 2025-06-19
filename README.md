# Windows Battery Analysis Tool

![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)
![Operating System](https://img.shields.io/badge/OS-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg) This Python-based tool for Windows automatically analyzes your computer's battery health. It leverages Windows' built-in `powercfg` command to generate a battery report, parses this report, and presents your battery's current health percentage in a user-friendly manner. The temporary HTML report file generated during the analysis is automatically deleted upon completion.

## Features

* **Automatic Report Generation:** Automatically creates an on-demand battery report using the `powercfg /batteryreport` Windows command.
* **Intelligent Battery Capacity Extraction:** Flexibly extracts "Design Capacity" and "Full Charge Capacity" values from the generated HTML report, supporting both English and Turkish report formats.
* **Unit Conversion:** Automatically converts capacity values to milliwatt-hours (mWh) if the report provides them in Watt-hours (Wh), ensuring consistent calculations.
* **Battery Health Calculation:** Calculates the battery's health percentage by comparing the current full charge capacity to the original design capacity.
* **Meaningful Evaluation:** Provides user-friendly feedback categorized by battery health status (Excellent, Normal, Warning, Critical, Abnormal).
* **Automatic Cleanup:** The temporary `battery-report.html` file is automatically deleted after the analysis is complete.
* **Error Handling:** Catches and reports potential errors during report generation or analysis, providing informative messages to the user.

## Requirements

* **Windows Operating System:** This tool relies on the `powercfg` command, making it exclusive to Windows.
* **Python 3:** Python 3.x must be installed on your system for the tool to run.
  * You can download Python from: [python.org/downloads/](https://www.python.org/downloads/)
  * **Crucially, remember to check "Add Python to PATH" during installation.**
* **`beautifulsoup4` Library:** Requires the `beautifulsoup4` library for HTML parsing.

## Installation

1. **Clone or Download the Repository:**
    To get this tool on your machine, you can clone the GitHub repository or download it as a ZIP file.

    ```bash
    git clone https://github.com/mustafayoruk/battery_report_health.git
    cd battery_report_health     
    ```
    *(Skip this step if you are not using Git/GitHub and simply downloaded the code file.)*
  
2. **Create a Virtual Environment (Recommended):**
    It is highly recommended to create a virtual environment to isolate project dependencies.

    ```bash
    python -m venv .venv
    ```

3. **Activate the Virtual Environment:**

* **For Windows (Command Prompt / CMD):**
      ```cmd
        .\.venv\Scripts\activate
        ```
* **For Windows (PowerShell):**
        ```powershell
        .\.venv\Scripts\Activate.ps1
        ```
* **For macOS / Linux (Bash / Zsh):**
        ```bash
        source ./.venv/bin/activate
        ```
    *(Note: Your command line prompt should show `(.venv)` at the beginning once the environment is active.)*

4. **Install Required Libraries:**
    With the virtual environment activated, install the necessary Python library (`beautifulsoup4`):

    ```bash
    pip install beautifulsoup4
    ```

## Usage

Running the tool is straightforward. With your virtual environment activated, or if you have installed the necessary libraries globally (not recommended):

```bash
python battery_report_health.py