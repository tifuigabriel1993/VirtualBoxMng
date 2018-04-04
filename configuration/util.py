from enum import Enum
import os
import shutil

class MachineLocker():
   def __init__(self, session, machine, locktype):
      self.session = session
      self.machine = machine
      self.locktype = locktype
   def __enter__(self):
      self.machine.lockMachine(self.session, self.locktype)
      return self.session
   def __exit__(self, exc_type, exc_val, exc_tb):
      self.session.unlockMachine()
      return False

def copy_and_rename(path, old_file, new_file):
    s = os.path.join(path, old_file)
    shutil.copy(s, os.path.join(path, new_file))

class ResourceConstants:
    CPU = "cpu"
    RAM = "ram"
    RESOURCES = "resources"
    SYSTEM = "system"
    APS = "apps"


if __name__ == "__main__":
    copy_and_rename("service/","vmconfig_template.service", "test.service")
