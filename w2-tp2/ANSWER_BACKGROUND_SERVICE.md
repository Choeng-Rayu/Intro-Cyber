# Running Programs as Background Services: Windows & Ubuntu Implementation Guide

## Introduction

To run code or programs continuously on a computer while avoiding visibility to users, we can execute them as background services. This guide addresses two critical questions: how to convert programming files into executable programs on Windows and Ubuntu, and how to assign our programs to run as background services in the operating system.

## Part A: Converting Programming Files to Executable Programs

### Windows Conversion Process

On Windows, converting Python scripts to executable programs involves using PyInstaller, a powerful tool that packages Python applications into standalone executables. First, PyInstaller must be installed as a one-time setup by running `pip install pyinstaller` in the command prompt with administrator privileges. Once installed, conversion is straightforward by navigating to the folder containing the Python script and executing the command `pyinstaller --onefile --windowed deleteFolderWindown_Dynamic.py`. The `--onefile` flag ensures that PyInstaller creates a single executable file rather than distributing it across multiple files, while the `--windowed` flag runs the application without displaying a console window to the user. Upon successful conversion, the resulting .exe file appears in the `dist/` folder and is ready for deployment. The project provides an automated batch script (`build_exe.bat`) that handles this entire process, including validation checks for Python installation and PyInstaller availability, making the conversion process user-friendly and automated.

### Ubuntu/Linux Conversion Process

Converting Python programs to executables on Ubuntu follows similar principles. PyInstaller can be used identically to the Windows process: `pyinstaller --onefile deleteFolderUbuntu.py`. However, Linux requires an additional step to make the compiled executable actually executable by running `chmod +x dist/deleteFolderUbuntu`, which adds execution permissions to the file. Alternatively, the project includes a pre-compiled SmartCleaner executable that can be used directly without compilation. The modular design allows either approach: users can compile from source for customization or use the pre-compiled binary for immediate deployment.

## Part B: Running Programs as Background Services

### Windows Background Service Execution

Windows provides multiple methods for running programs as background services. The simplest approach uses Windows Task Scheduler, which can be accessed by pressing `Win + R` and typing `taskschd.msc`. In Task Scheduler, users create a new task named appropriately (such as "SmartCleaner"), ensure it is configured to run with highest privileges, and set specific triggers such as "At startup" or "On a schedule" to define when the task should execute. The action specifies the program path to the executable and any required arguments, such as folder paths and execution intervals. This method requires no additional software and provides a graphical interface for configuration. For more advanced scenarios, the project includes support for NSSM (Non-Sucking Service Manager), which provides true Windows service functionality with enhanced control over service lifecycle, logging, and error recovery. The automated batch script (`setup_exe.bat`) simplifies this deployment.

### Ubuntu/Linux Background Service Execution

On Ubuntu and Linux systems, background services are managed through systemd, the modern service management framework. The project includes a comprehensive setup script (`setup_service.sh`) that automates the entire service installation process. When executed with administrative privileges (`sudo bash setup_service.sh`), this script performs three critical steps: it copies the Python script to the system directory `/usr/local/bin/`, creates a systemd service file at `/etc/systemd/system/smart-cleaner.service` with appropriate configuration, and enables the service for automatic startup. The systemd service file contains unit definitions that specify service dependencies, execution type, user context, restart behavior, and working directories. Once installed, the service can be managed using standard systemd commands such as `sudo systemctl start smart-cleaner` to start the service, `sudo systemctl stop smart-cleaner` to stop it, and `sudo systemctl status smart-cleaner` to check its current status. Real-time monitoring is available through the journalctl command: `sudo journalctl -u smart-cleaner -f`, which displays live logs of the service execution. Service removal is equally straightforward using `sudo systemctl disable smart-cleaner` followed by `sudo systemctl stop smart-cleaner` and deletion of the service file.

## Comparison and Implementation Strategy

Both Windows and Ubuntu implementations share a common goal: creating invisible, continuously-running background processes. Windows relies on the Task Scheduler or NSSM for orchestration, while Ubuntu leverages systemd for service management. The key difference lies in the operational philosophy: Windows Task Scheduler offers simplicity for scheduled execution, while systemd provides deeper integration with the operating system's boot process and resource management. The choice between approaches depends on deployment requirements—Task Scheduler suffices for periodic or event-driven execution, while systemd services are ideal for persistent, always-running processes. The project materials provide production-ready implementations for both platforms, including error handling, logging, configuration management, and user-friendly installation procedures that abstract away technical complexity.

## Conclusion

Converting programs to background services requires platform-specific approaches but follows consistent principles: packaging the executable and configuring the operating system to launch and maintain it automatically. Windows developers should leverage Task Scheduler for simplicity or NSSM for advanced features, while Ubuntu administrators should use systemd's powerful service management framework. The provided scripts and templates in this project demonstrate best practices for both platforms and can serve as templates for future service deployments.
