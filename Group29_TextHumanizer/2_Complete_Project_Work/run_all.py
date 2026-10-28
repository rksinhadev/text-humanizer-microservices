import subprocess
import sys
import time
import os

services = [
    ["python", "auth_service.py"],
    ["python", "history_service.py"],
    ["python", "ai_service.py"],
    ["python", "gateway.py"]
]

procs = []

def start():
    for cmd in services:
        p = subprocess.Popen(cmd)
        procs.append(p)
    
    try:
        while True:
            for p in procs:
                ret = p.poll()
                if ret is not None:
                    print(f"Service {p.args} exited with code {ret}")
                    sys.exit(ret)
            time.sleep(1)
    except KeyboardInterrupt:
        for p in procs:
            p.terminate()

if __name__ == "__main__":
    start()
