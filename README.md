# MiniOS Ekoms

## Group Members
1. Necesario - Project Leader and CLI Developer
2. Panado - File Management Developer
3. Pagdato - Process and Memory Developer
4. Ciupan - User/System Developer

## Project Description
MiniOS is a command-line operating system simulator written in Python. It simulates a shell, a file system, processes, memory, user login and system information.

## Features
- Command-line interface
- File management (virtual disk saved to minios_disk.json)
- Process simulation (PID table)
- Memory simulation (1024 MB total, 256 MB reserved for the system)
- User login (admin / student, hashed passwords)
- System information
- Error handling

## Requirements
Python 3.x, Windows CMD (no extra packages)

## How to Run
1. Clone the repository.
2. Open CMD and go to the project folder.
3. Run: `python main.py`

Accounts: `admin` / `admin123`, `student` / `student123`

## Available Commands
help, clear, date, time, whoami, systeminfo, version, echo, history, exit,
dir, mkdir, create, read, delete, write, rename, cd, pwd,
process, run, kill, memory, allocate, free, users, logout

## Run the tests
`python -m unittest discover tests`
