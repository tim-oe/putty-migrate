#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
#
#
"""
application entry point
"""

from pathlib import Path
import re
import shutil
from pyutil import filereplace

START_SESSION_RE = '\\[HKEY_CURRENT_USER\\\\Software\\\\[\\w]+\\\\PuTTY\\\\Sessions\\\\(.*)\\]'
KV_RE = '"([^"]*)"="?([^"]*)"?'
DWORD_RE = 'dword:(\\d+)'
KEY_RE = '.*\\\\((.*)\\.ppk)'

SESSION_TEMPLATE_FILE = "data/field-settings.putty"

# actual start point
if __name__ == "__main__":

    keys: set = set()

    with open("data/putty-sessions.reg", "r", encoding="UTF-8") as file:
        print("file open")            
        while line := file.readline():
            l: str = line.rstrip()
            match = re.search(START_SESSION_RE, l)
            if match:
                
                baseDir: Path = Path("sessions")
                baseDir.mkdir(parents=True, exist_ok=True)
                tf: Path = Path(SESSION_TEMPLATE_FILE)
                outFile: Path = Path(shutil.copy(tf, f"sessions/{match.group(1)}"))
                print(f"outfile: {outFile}")        

                while line := file.readline():
                    l: str = line.rstrip()
                    if l != "":
                        kv = re.search(KV_RE, l)
                        v = kv.group(2)
                        d = re.search(DWORD_RE, v)
                        if d:
                            v = int(d.group(1))

                        match kv.group(1):
                            case "HostName":
                                filereplace(outFile.resolve(), "__host__", v)
                            case "UserName":
                                filereplace(outFile.resolve(), "__user-name__", v)
                            case "PublicKeyFile":
                                key = re.search(KEY_RE, v)
                                if key:
                                    filereplace(outFile.resolve(), "__key-file__", f"/home/tcronin/.ssh/aws/{key.group(1)}")
                                    keys.add(key.group(1))
                            case "WinTitle":
                                t: str = v
                                if t == "":
                                    t = match.group(1)
                                filereplace(outFile.resolve(), "__window-title_", t)
                    else:    
                        break

                # try:
                #     result = subprocess.run(["ssh-keygen", "-D", sd.host], capture_output=True, text=True)
                #     print(result.stdout)

                #     result = subprocess.run(["ssh-keyscan", "-T", "10", "-H", "-D", sd.host, ">>", "~/.ssh/known_hosts"], capture_output=True, text=True)
                #     print(result.stdout)
                # except Exception as e:
                #     print("An error occurred:")
                #     print(e)
                #     traceback.print_exc()                

    for element in keys:
        print(element)    

