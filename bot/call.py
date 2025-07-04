import subprocess
import os
from .config import PJSUA_PATH, SIP_USER, SIP_PASS, DYLD_LIB_PATH
from .logs import log_call

def place_call(target, caller_id):
    command = [
        PJSUA_PATH,
        "--id", f"sip:{caller_id}@didlogic.net",
        "--registrar", "sip:didlogic.net",
        "--realm", "*",
        "--username", SIP_USER,
        "--password", SIP_PASS,
        "--null-audio",
        f"sip:{target}@didlogic.net"
    ]
    env = { "DYLD_LIBRARY_PATH": DYLD_LIB_PATH }
    subprocess.Popen(command, env={**os.environ, **env})
    log_call(caller_id, target)