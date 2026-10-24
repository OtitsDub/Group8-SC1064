"""Run with:  python -m unittest discover tests   (from the MiniOS folder)"""
import os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from filesystem import FileSystem, FileSystemError
from processes import ProcessManager, ProcessError
from memory import MemoryManager, MemoryError_
from users import UserManager

class TestFiles(unittest.TestCase):
    def setUp(self):
        self.fs = FileSystem(os.path.join(tempfile.mkdtemp(), "d.json"))
    def test_create_read_delete(self):
        self.fs.create("a.txt"); self.fs.write("a.txt", "hi")
        self.assertEqual(self.fs.read("a.txt"), "hi")
        self.fs.delete("a.txt")
        with self.assertRaises(FileSystemError): self.fs.read("a.txt")
    def test_mkdir_cd(self):
        self.fs.mkdir("D"); self.fs.cd("D"); self.assertEqual(self.fs.pwd(), "/D")
    def test_duplicate(self):
        self.fs.create("x"); 
        with self.assertRaises(FileSystemError): self.fs.create("x")

class TestProcesses(unittest.TestCase):
    def test_run_kill(self):
        pm = ProcessManager(); p = pm.run("calc"); self.assertEqual(p.pid, 1)
        pm.kill("1"); self.assertEqual(pm.list(), [])
    def test_bad_pid(self):
        pm = ProcessManager()
        for bad in ("999", "abc"):
            with self.assertRaises(ProcessError): pm.kill(bad)

class TestMemory(unittest.TestCase):
    def test_alloc_free(self):
        m = MemoryManager(); m.allocate("200"); self.assertEqual(m.used, 456)
        m.free("200"); self.assertEqual(m.used, 256)
    def test_limits(self):
        m = MemoryManager()
        for bad in ("5000", "-5", "abc"):
            with self.assertRaises(MemoryError_): m.allocate(bad)
        with self.assertRaises(MemoryError_): m.free("10")

class TestUsers(unittest.TestCase):
    def test_login(self):
        u = UserManager()
        self.assertTrue(u.authenticate("admin", "admin123"))
        self.assertFalse(u.authenticate("admin", "wrong"))

if __name__ == "__main__":
    unittest.main()
