import subprocess
import os
from bot.config import PJSUA_PATH, SIP_USER, SIP_PASS, DYLD_LIB_PATH
import logging
import asyncio

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
    try:
        result = subprocess.run(command, env={**os.environ, **env}, capture_output=True, text=True, timeout=60)
        success = result.returncode == 0
        error_message = ""
        if not success:
            error_message = f"Call failed with code {result.returncode}. Stderr: {result.stderr.strip()}"
    except FileNotFoundError:
        success = False
        error_message = "Call binary not found. Please check PJSUA_PATH."
    except subprocess.TimeoutExpired:
        success = False
        error_message = "Call process timed out."
    except Exception as e:
        success = False
        error_message = f"Unexpected error: {e}"
    log_entry = (
        f"CALL: {caller_id} → {target}\n"
        f"CMD: {' '.join(command)}\n"
        f"SUCCESS: {success}\n"
        f"ERROR: {error_message}\n"
        f"{'='*40}\n"
    )
    with open("logs/calls.log", "a") as log:
        log.write(log_entry)
    return success, error_message

async def place_call(target, caller_id):
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
    transcript = []
    last_state = None
    try:
        process = await asyncio.create_subprocess_exec(
            *command,
            env={**os.environ, **env},
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )
        async for line in process.stdout:
            decoded = line.decode().strip()
            transcript.append(decoded)
            state = None
            if "Trying" in decoded:
                state = "🔄 Trying..."
            elif "Ringing" in decoded:
                state = "🔔 Ringing..."
            elif "answered" in decoded:
                state = "✅ Call answered!"
            elif "Busy" in decoded:
                state = "🚫 Busy signal."
            elif "Call ended" in decoded:
                state = "📞 Call ended."
            elif "Authentication" in decoded and "error" in decoded:
                state = "🔒 Authentication error."
            elif "failed" in decoded or "ERROR" in decoded:
                state = f"❌ Call failed: {decoded}"
            # Only yield if state changed
            if state and state != last_state:
                yield state
                last_state = state
        returncode = await process.wait()
        # Final summary
        if returncode == 0:
            yield "✅ Call process finished successfully."
        else:
            yield f"❌ Call process exited with code {returncode}."
    except FileNotFoundError:
        yield "❌ Call binary not found. Please check PJSUA_PATH."
    except asyncio.TimeoutError:
        yield "❌ Call process timed out."
    except Exception as e:
        yield f"❌ Unexpected error: {e}"
    # Log the full transcript
    log_entry = (
        f"CALL: {caller_id} → {target}\n"
        f"CMD: {' '.join(command)}\n"
        f"TRANSCRIPT:\n" + "\n".join(transcript) + "\n"
        f"{'='*40}\n"
    )
    with open("logs/calls.log", "a") as log:
        log.write(log_entry)