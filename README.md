# Intro to Cybersecurity Repository

Welcome to my Cybersecurity course repository for **Year 3, Term 1**. This repository contains all assignments and lab work for the Introduction to Cybersecurity course.

## 📁 Repository Structure

```
Intro-Cyber/
├── w1_Assignment/     # Week 1 - Assignment & Lab
├── w2-tp2/            # Week 2 - Assignment & Lab (TP2 = Lab 2)
├── w3-tp3/            # Week 3 - Assignment & Lab (TP3 = Lab 3)
└── README.md          # This file
```

## 📚 Folder Details

### **Week 1: w1_Assignment/**
Contains Week 1 assignment and lab exercises related to CPU and RAM resource management.

**Files:**
- `occupyCPU.py` - Python script to simulate CPU occupation
- `occupyRAM.py` - Python script to simulate RAM occupation
- `occupyCPU.spec` & `occupyRAM.spec` - PyInstaller specification files (for executable building)
- `dist/` - Compiled executable files
- `build/` - Build artifacts
- `README.md` - Week 1 documentation

### **Week 2: w2-tp2/**
Contains Week 2 assignment and lab (TP2) focused on file system operations and folder management.

**Structure:**
- `TP2/` - Main lab folder
  - `ubuntu/` - Ubuntu/Linux specific implementation
  - `windows/` - Windows specific implementation
- `testDelete/` - Test directory for delete operations
- `README.md` - Week 2 documentation

**Key Files:**
- `deleteFolderUbuntu.py` - Python script for folder deletion on Ubuntu
- `deleteFolderWindows.py` - Python script for folder deletion on Windows
- `smart-cleaner.service` - System service file for Ubuntu
- `smart-cleaner.conf` - Configuration file

### **Week 3: w3-tp3/**
Contains Week 3 assignment and lab (TP3).

## 🎯 Quick Navigation

| Week | Folder | Type | Focus Area |
|------|--------|------|-----------|
| 1 | `w1_Assignment/` | Assignment + Lab | Resource Management (CPU/RAM) |
| 2 | `w2-tp2/` | Assignment + Lab | File System Operations |
| 3 | `w3-tp3/` | Assignment + Lab | TBD |

## 📝 File Naming Convention

- `occupyCPU.py` / `occupyRAM.py` - Resource occupation scripts
- `deleteFolderUbuntu.py` / `deleteFolderWindows.py` - OS-specific utilities
- `.spec` files - PyInstaller configuration files
- `.service` - Linux systemd service files
- `.conf` - Configuration files

## 🚀 How to Use This Repository

1. **Navigate to the week you need:** Each week has its own folder (`w1_Assignment/`, `w2-tp2/`, `w3-tp3/`)
2. **Read the README:** Each week folder contains a `README.md` with specific instructions
3. **Find the code:** Look for `.py` files (Python scripts) or documentation files in the respective week folders

## 📖 Course Information

- **Student:** Choeng Rayu, G2, IDTB100252
- **Program:** Year 3, Term 1 (Y3 T1)
- **Course:** Introduction to Cybersecurity (Intro-Cyber)
- **Language:** Python, Bash, System Configuration

## 📌 Notes

- Assignment files and lab files are stored together in each week's folder
- Lab names use the format `w#-tp#` (e.g., `w2-tp2` = Week 2, TP Lab 2)
- Some labs include OS-specific implementations (Ubuntu/Linux and Windows)
- Each week's folder includes a dedicated README with detailed instructions

---

Thank you for visiting! Feel free to explore and review our work. 😊
