"""filesystem.py - Simulated file system.
The disk is a tree of Python dictionaries saved to minios_disk.json,
so files survive between runs. No real Windows files are touched."""
import json
import os

class FileSystemError(Exception):
    pass

class FileSystem:
    def __init__(self, disk_file="minios_disk.json"):
        self.disk_file = disk_file
        self.root = {"type": "dir", "children": {}}
        self.cwd = []                     
        self._load()

    # persistence
    def _load(self):
        if os.path.exists(self.disk_file):
            try:
                with open(self.disk_file, "r", encoding="utf-8") as f:
                    self.root = json.load(f)
            except (OSError, ValueError):
                self.root = {"type": "dir", "children": {}}
        else:
            self.root["children"]["readme.txt"] = {
                "type": "file", "content": "Welcome to MiniOS!"}
            self._save()

    def _save(self):
        try:
            with open(self.disk_file, "w", encoding="utf-8") as f:
                json.dump(self.root, f, indent=2)
        except OSError:
            pass

    # pathhelpers
    def _normalize(self, path):
        parts = [] if path.startswith("/") else list(self.cwd)
        for p in path.split("/"):
            if p in ("", "."):
                continue
            if p == "..":
                if parts:
                    parts.pop()
            else:
                parts.append(p)
        return parts

    def _node(self, parts):
        node = self.root
        for p in parts:
            if node["type"] != "dir" or p not in node["children"]:
                raise FileSystemError("Path does not exist.")
            node = node["children"][p]
        return node

    def _parent_and_name(self, path):
        parts = self._normalize(path)
        if not parts:
            raise FileSystemError("Invalid name.")
        parent = self._node(parts[:-1])
        if parent["type"] != "dir":
            raise FileSystemError("Path does not exist.")
        return parent, parts[-1]

    # commands
    def pwd(self):
        return "/" + "/".join(self.cwd)

    def list_dir(self):
        node = self._node(self.cwd)
        return sorted(node["children"].items(),
                      key=lambda kv: (kv[1]["type"] != "dir", kv[0].lower()))

    def mkdir(self, path):
        parent, name = self._parent_and_name(path)
        if name in parent["children"]:
            raise FileSystemError("A file or directory with that name already exists.")
        parent["children"][name] = {"type": "dir", "children": {}}
        self._save()

    def create(self, path, content=""):
        parent, name = self._parent_and_name(path)
        if name in parent["children"]:
            raise FileSystemError("A file or directory with that name already exists.")
        parent["children"][name] = {"type": "file", "content": content}
        self._save()

    def read(self, path):
        parent, name = self._parent_and_name(path)
        node = parent["children"].get(name)
        if node is None:
            raise FileSystemError("File does not exist.")
        if node["type"] != "file":
            raise FileSystemError(f"'{name}' is a directory, not a file.")
        return node["content"]

    def write(self, path, text, append=False):
        parent, name = self._parent_and_name(path)
        node = parent["children"].get(name)
        if node is None:
            raise FileSystemError("File does not exist. Use 'create' first.")
        if node["type"] != "file":
            raise FileSystemError(f"'{name}' is a directory, not a file.")
        node["content"] = (node["content"] + "\n" + text) if append and node["content"] else text
        self._save()

    def delete(self, path):
        parent, name = self._parent_and_name(path)
        node = parent["children"].get(name)
        if node is None:
            raise FileSystemError("File or directory does not exist.")
        if node["type"] == "dir" and node["children"]:
            raise FileSystemError("Directory is not empty.")
        kind = "Directory" if node["type"] == "dir" else "File"
        del parent["children"][name]
        self._save()
        return kind

    def rename(self, old, new):
        parent, name = self._parent_and_name(old)
        if name not in parent["children"]:
            raise FileSystemError("File or directory does not exist.")
        if "/" in new:
            raise FileSystemError("New name cannot contain '/'.")
        if new in parent["children"]:
            raise FileSystemError("The new name already exists.")
        parent["children"][new] = parent["children"].pop(name)
        self._save()

    def cd(self, path):
        parts = self._normalize(path)
        node = self._node(parts)
        if node["type"] != "dir":
            raise FileSystemError("Not a directory.")
        self.cwd = parts
