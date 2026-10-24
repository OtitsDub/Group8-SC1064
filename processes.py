"""processes.py - Simulated process management.
Each process is a small Process Control Block (PCB) stored in a table."""
from datetime import datetime

class ProcessError(Exception):
    pass

class Process:
    def __init__(self, pid, name):
        self.pid = pid
        self.name = name
        self.status = "RUNNING"
        self.started = datetime.now().strftime("%H:%M:%S")

class ProcessManager:
    MAX_PROCESSES = 20

    def __init__(self):
        self.table = {}        # pid -> Process
        self.next_pid = 1

    def run(self, name):
        if len(self.table) >= self.MAX_PROCESSES:
            raise ProcessError("Process table is full.")
        proc = Process(self.next_pid, name)
        self.table[proc.pid] = proc
        self.next_pid += 1
        return proc

    def kill(self, pid_text):
        try:
            pid = int(pid_text)
        except ValueError:
            raise ProcessError("PID must be a number.")
        if pid not in self.table:
            raise ProcessError("Process does not exist.")
        del self.table[pid]
        return pid

    def list(self):
        return list(self.table.values())
