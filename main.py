"""main.py - MiniOS shell (command-line interface and command dispatcher).
Run with:  python main.py"""
import os
from datetime import datetime

from filesystem import FileSystem, FileSystemError
from processes import ProcessManager, ProcessError
from memory import MemoryManager, MemoryError_
from users import UserManager, login_screen
from sysinfo import system_info, OS_NAME, VERSION

class MiniOS:
    def __init__(self):
        self.fs = FileSystem()
        self.procs = ProcessManager()
        self.mem = MemoryManager()
        self.users = UserManager()
        self.history = []
        self.running = True
        self.commands = {
            "help": self.cmd_help, "clear": self.cmd_clear, "date": self.cmd_date,
            "time": self.cmd_time, "whoami": self.cmd_whoami,
            "systeminfo": self.cmd_systeminfo, "exit": self.cmd_exit,
            "shutdown": self.cmd_exit,
            "dir": self.cmd_dir, "mkdir": self.cmd_mkdir, "create": self.cmd_create,
            "read": self.cmd_read, "delete": self.cmd_delete, "write": self.cmd_write,
            "rename": self.cmd_rename, "cd": self.cmd_cd, "pwd": self.cmd_pwd,
            "process": self.cmd_process, "run": self.cmd_run, "kill": self.cmd_kill,
            "memory": self.cmd_memory, "allocate": self.cmd_allocate, "free": self.cmd_free,
            "users": self.cmd_users, "logout": self.cmd_logout,
            "history": self.cmd_history, "echo": self.cmd_echo, "version": self.cmd_version,
        }

    # ---------- shell ----------
    def banner(self):
        print("=" * 40)
        print(f"{OS_NAME.upper() + ' v' + VERSION:^40}")
        print("=" * 40)
        print("\nWelcome to MiniOS!\n")

    def start(self):
        self.banner()
        while self.running:
            if not login_screen(self.users, OS_NAME):
                return
            print("\nType 'help' to see the available commands.\n")
            self.shell_loop()

    def shell_loop(self):
        while self.running and self.users.current_user:
            try:
                line = input("MiniOS> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                self.cmd_exit([])
                return
            if not line:
                continue
            self.history.append(line)
            self.execute(line)

    def execute(self, line):
        parts = line.split()
        name, args = parts[0].lower(), parts[1:]
        handler = self.commands.get(name)
        if handler is None:
            print("Unknown command.\n\nType 'help' to see the available commands.\n")
            return
        try:
            handler(args)
        except (FileSystemError, ProcessError, MemoryError_) as err:
            print(f"Error: {err}\n")
        except Exception as err:                     # last-resort safety net
            print(f"Error: Something went wrong ({err}).\n")

    @staticmethod
    def need(args, n, usage):
        if len(args) < n:
            raise FileSystemError(f"Missing argument. Usage: {usage}")

    # ---------- general ----------
    def cmd_help(self, args):
        print("""
Available Commands:

General:     help, clear, date, time, whoami, systeminfo, version, echo, history, exit
Files:       dir, mkdir <name>, create <file>, read <file>, delete <name>,
             write <file> <text>, rename <old> <new>, cd <folder>, pwd
Processes:   process, run <name>, kill <pid>
Memory:      memory, allocate <MB>, free <MB>
Users:       users, logout
""")

    def cmd_clear(self, args):
        os.system("cls" if os.name == "nt" else "clear")

    def cmd_date(self, args):
        print(datetime.now().strftime("Date: %A, %B %d, %Y\n"))

    def cmd_time(self, args):
        print(datetime.now().strftime("Time: %I:%M:%S %p\n"))

    def cmd_whoami(self, args):
        print(f"Current User: {self.users.current_user}\n")

    def cmd_systeminfo(self, args):
        print(system_info(self.users.current_user, self.mem.total) + "\n")

    def cmd_version(self, args):
        print(f"{OS_NAME} version {VERSION}\n")

    def cmd_echo(self, args):
        print(" ".join(args) + "\n")

    def cmd_history(self, args):
        for i, c in enumerate(self.history, 1):
            print(f"{i:>3}  {c}")
        print()

    def cmd_exit(self, args):
        print("\nShutting down MiniOS...\n\nGoodbye!")
        self.running = False

    # ---------- users ----------
    def cmd_users(self, args):
        print(f"{'USERNAME':<12}ROLE")
        for u, r in self.users.list_users():
            print(f"{u:<12}{r}")
        print()

    def cmd_logout(self, args):
        print(f"\nUser '{self.users.current_user}' logged out.\n")
        self.users.logout()

    # ---------- files ----------
    def cmd_dir(self, args):
        print(f"\nDirectory of {self.fs.pwd()}\n")
        items = self.fs.list_dir()
        for name, node in items:
            tag = "<DIR>" if node["type"] == "dir" else f"{len(node['content'])} bytes"
            print(f"  {tag:<12}{name}")
        print(f"\n  {len(items)} item(s)\n")

    def cmd_mkdir(self, args):
        self.need(args, 1, "mkdir <folder>")
        self.fs.mkdir(args[0]); print("Directory created.\n")

    def cmd_create(self, args):
        self.need(args, 1, "create <file>")
        self.fs.create(args[0]); print("File created.\n")

    def cmd_read(self, args):
        self.need(args, 1, "read <file>")
        content = self.fs.read(args[0])
        print(f"\n{content if content else '(file is empty)'}\n")

    def cmd_delete(self, args):
        self.need(args, 1, "delete <file or folder>")
        kind = self.fs.delete(args[0]); print(f"{kind} deleted.\n")

    def cmd_write(self, args):
        self.need(args, 2, "write <file> <text>")
        self.fs.write(args[0], " ".join(args[1:]), append=True); print("Text written to file.\n")

    def cmd_rename(self, args):
        self.need(args, 2, "rename <old> <new>")
        self.fs.rename(args[0], args[1]); print("Renamed successfully.\n")

    def cmd_cd(self, args):
        self.need(args, 1, "cd <folder>")
        self.fs.cd(args[0]); print(f"Current directory: {self.fs.pwd()}\n")

    def cmd_pwd(self, args):
        print(self.fs.pwd() + "\n")

    # ---------- processes ----------
    def cmd_process(self, args):
        procs = self.procs.list()
        if not procs:
            print("No running processes.\n"); return
        print(f"\n{'PID':<7}{'NAME':<16}{'STATUS':<10}STARTED")
        for p in procs:
            print(f"{p.pid:<7}{p.name:<16}{p.status:<10}{p.started}")
        print()

    def cmd_run(self, args):
        self.need(args, 1, "run <program>")
        p = self.procs.run(args[0])
        print(f"\nProcess started.\n\nPID: {p.pid}\nName: {p.name}\nStatus: {p.status}\n")

    def cmd_kill(self, args):
        self.need(args, 1, "kill <pid>")
        pid = self.procs.kill(args[0]); print(f"Process {pid} terminated.\n")

    # ---------- memory ----------
    def cmd_memory(self, args):
        print("\n" + self.mem.status() + "\n")

    def cmd_allocate(self, args):
        self.need(args, 1, "allocate <MB>")
        n = self.mem.allocate(args[0]); print(f"{n} MB allocated.\n")

    def cmd_free(self, args):
        self.need(args, 1, "free <MB>")
        n = self.mem.free(args[0]); print(f"{n} MB released.\n")

if __name__ == "__main__":
    MiniOS().start()
