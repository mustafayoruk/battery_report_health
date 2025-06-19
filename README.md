# Windows Battery Health Analyzer

This Python project analyzes your **battery health on Windows**, stores the results in a CSV log, and archives the original HTML reports.

---

## Features

- Generates battery reports using `powercfg /batteryreport`
- Extracts the following from the report:
  - Design Capacity
  - Full Charge Capacity
  - Battery Health Percentage
- Saves results to a CSV file (`battery_history.csv`)
- Archives original HTML reports with timestamp
- Provides a health rating (Excellent / Normal / Warning / Critical)

---

## Requirements

- **Operating System:** Windows 10 or newer
- **Python Version:** 3.8+
- **Dependencies:** No third-party libraries required  
  (only built-in Python modules are used)

---

## Usage

1. Clone the repository or download `battery_analyzer.py`:

```bash
git clone https://github.com/your-username/project-name.git
cd project-name


---

### Note
- mustafayoruk battery_report_health
