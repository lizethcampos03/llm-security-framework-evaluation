import os, signal\n\n\ndef killProcess(processID):\n    '''\n    Kill the process with the given processID.\n    '''\n    os.kill(processID, signal.SIGKILL)
