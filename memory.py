"""memory.py - Simulated memory management (a simple memory counter)."""

class MemoryError_(Exception):
    pass

class MemoryManager:
    def __init__(self, total=1024, system_reserved=256):
        self.total = total
        self.system_reserved = system_reserved   # always used by the "kernel"
        self.user_allocated = 0

    @property
    def used(self):
        return self.system_reserved + self.user_allocated

    @property
    def free_mem(self):
        return self.total - self.used

    @staticmethod
    def _parse(text):
        try:
            amount = int(text)
        except ValueError:
            raise MemoryError_("Amount must be a whole number (in MB).")
        if amount <= 0:
            raise MemoryError_("Amount must be greater than 0.")
        return amount

    def allocate(self, text):
        amount = self._parse(text)
        if amount > self.free_mem:
            raise MemoryError_(f"Not enough memory. Only {self.free_mem} MB free.")
        self.user_allocated += amount
        return amount

    def free(self, text):
        amount = self._parse(text)
        if amount > self.user_allocated:
            raise MemoryError_(
                f"Cannot free {amount} MB. Only {self.user_allocated} MB is allocated by users.")
        self.user_allocated -= amount
        return amount

    def status(self):
        bar_len = 30
        filled = round(bar_len * self.used / self.total)
        bar = "#" * filled + "-" * (bar_len - filled)
        return (f"Memory Status\n{'-' * 24}\n"
                f"Total Memory: {self.total:>5} MB\n"
                f"Used Memory:  {self.used:>5} MB\n"
                f"Free Memory:  {self.free_mem:>5} MB\n"
                f"[{bar}] {100 * self.used // self.total}% used")
