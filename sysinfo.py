"""sysinfo.py - Simulated system information."""
OS_NAME = "MiniOS Ekoms"
VERSION = "1.0"

def system_info(user, memory_total):
    line = "=" * 40
    return (f"{line}\n{'SYSTEM INFORMATION':^40}\n{line}\n\n"
            f"OS Name: {OS_NAME}\nVersion: {VERSION}\nArchitecture: 64-bit\n"
            f"CPU: Virtual CPU\nMemory: {memory_total} MB\nUser: {user}\n\n{line}")
