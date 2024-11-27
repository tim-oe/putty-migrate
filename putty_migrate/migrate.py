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
import traceback
from pyutil import filereplace
import subprocess

from putty_migrate.SessionData import SessionData

START_SESSION_RE = '\\[HKEY_CURRENT_USER\\\\Software\\\\SimonTatham\\\\PuTTY\\\\Sessions\\\\(.*)\\]'
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
                sd: SessionData = SessionData(name=match.group(1))
                
                baseDir: Path = Path("sessions")
                baseDir.mkdir(parents=True, exist_ok=True)

                while line := file.readline():
                    l: str = line.rstrip()
                    if l != "":
                        kv = re.search(KV_RE, l)
                        v = kv.group(2)
                        d = re.search(DWORD_RE, v)
                        if d:
                            v = int()

                        match kv.group(1):
                            case "HostName":
                                sd.host = v
                            case "UserName":
                                sd.user = v
                            case "PublicKeyFile":
                                key = re.search(KEY_RE, v)
                                if key:
                                    v = key.group(1)
                                sd.key = v
                            case "WinTitle":
                                sd.title = v
                    else:    
                        break

                tf: Path = Path(SESSION_TEMPLATE_FILE)
                #print(f"tempalte file : {tf.resolve()}")        

                outFile: Path = Path(shutil.copy(tf, f"sessions/{match.group(1)}"))

                print(f"outfile: {outFile}")        
                # try:
                #     result = subprocess.run(["ssh-keygen", "-D", sd.host], capture_output=True, text=True)
                #     print(result.stdout)

                #     result = subprocess.run(["ssh-keyscan", "-T", "10", "-H", "-D", sd.host, ">>", "~/.ssh/known_hosts"], capture_output=True, text=True)
                #     print(result.stdout)
                # except Exception as e:
                #     print("An error occurred:")
                #     print(e)
                #     traceback.print_exc()                

                t: str = sd.title
                if t == "":
                    t = match.group(1)
                filereplace(outFile.resolve(), "__window-title_", t)
                filereplace(outFile.resolve(), "__host__", sd.host)
                filereplace(outFile.resolve(), "__user-name__", sd.user)
                filereplace(outFile.resolve(), "__key-file__", f"/home/tcronin/.ssh/aws/{sd.key}")

                keys.add(sd.key)

    for element in keys:
        print(element)    

