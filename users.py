"""users.py - User management (login, whoami, users).
Passwords are stored as SHA-256 hashes, never as plain text."""
import hashlib
import getpass
import sys

def _hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

class UserManager:
    def __init__(self):
        # username -> {"hash": ..., "role": ...}
        self.accounts = {
            "admin":   {"hash": _hash("admin123"),   "role": "Administrator"},
            "student": {"hash": _hash("student123"), "role": "Standard User"},
        }
        self.current_user = None

    def authenticate(self, username, password):
        acc = self.accounts.get(username)
        if acc and acc["hash"] == _hash(password):
            self.current_user = username
            return True
        return False

    def role(self):
        return self.accounts[self.current_user]["role"] if self.current_user else "None"

    def logout(self):
        self.current_user = None

    def list_users(self):
        return [(u, a["role"]) for u, a in self.accounts.items()]

def read_password(prompt="Password: "):
    """Show * while typing on Windows CMD; fall back to getpass elsewhere."""
    try:
        import msvcrt  # Windows only
    except ImportError:
        return getpass.getpass(prompt)
    sys.stdout.write(prompt)
    sys.stdout.flush()
    chars = []
    while True:
        ch = msvcrt.getwch()
        if ch in ("\r", "\n"):
            sys.stdout.write("\n")
            return "".join(chars)
        if ch == "\003":
            raise KeyboardInterrupt
        if ch == "\b":
            if chars:
                chars.pop()
                sys.stdout.write("\b \b")
        else:
            chars.append(ch)
            sys.stdout.write("*")
        sys.stdout.flush()

def login_screen(users, os_name):
    """Ask for credentials (max 3 attempts). Returns True if login worked."""
    print("=" * 40)
    print(f"{'MiniOS Login':^40}")
    print("=" * 40)
    for _ in range(3):
        username = input("\nUsername: ").strip()
        password = read_password("Password: ")
        if users.authenticate(username, password):
            print("\nLogin successful.")
            print(f"\nWelcome, {username}!")
            return True
        print("Error: Invalid username or password.")
    print("\nToo many failed attempts. System locked.")
    return False
