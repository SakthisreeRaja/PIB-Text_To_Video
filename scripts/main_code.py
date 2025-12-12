import subprocess
import sys
import os
import time

CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_SCRIPT_DIR)

print(f"[DEBUG] Script Location: {CURRENT_SCRIPT_DIR}")
print(f"[DEBUG] Project Root:    {PROJECT_ROOT}")

SCRIPT_MAIN = os.path.join(CURRENT_SCRIPT_DIR, "plain2output", "main.py")
SCRIPT_TEXT2VIDEO = os.path.join(CURRENT_SCRIPT_DIR, "text2video", "text_imge.py")

VENV_AUDIO = os.path.join(CURRENT_SCRIPT_DIR, "venv_v2_2_1", "Scripts", "python.exe")
VENV_VIDEO = os.path.join(CURRENT_SCRIPT_DIR, "venv_v1_1_3", "Scripts", "python.exe")

print(f"[CHECK] Audio venv: {VENV_AUDIO}")
if os.path.exists(VENV_AUDIO):
    print("   [OK] FOUND!")
else:
    print("   [FAIL] NOT FOUND")

print(f"[CHECK] Video venv: {VENV_VIDEO}")
if os.path.exists(VENV_VIDEO):
    print("   [OK] FOUND!")
else:
    print("   [FAIL] NOT FOUND")

print(f"[CHECK] Looking for Audio Script: {SCRIPT_MAIN}")
if os.path.exists(SCRIPT_MAIN):
    print("   [OK] FOUND!")
else:
    print("   [FAIL] NOT FOUND (Check folder 'plain2output')")

print(f"[CHECK] Looking for Video Script: {SCRIPT_TEXT2VIDEO}")
if os.path.exists(SCRIPT_TEXT2VIDEO):
    print("   [OK] FOUND!")
else:
    print("   [FAIL] NOT FOUND (Check folder 'text2video')")

WORKFLOW = [
    ("Phase 1: Audio Gen", VENV_AUDIO, SCRIPT_MAIN, ["audio"]),
    ("Phase 2: Video Gen", VENV_VIDEO, SCRIPT_TEXT2VIDEO, []),
    ("Phase 3: Merging",   VENV_AUDIO, SCRIPT_MAIN, ["merge"]),
]

def run_step(step_name, interpreter, script, args):
    print("-" * 50)
    print(f"STEP: {step_name}")
    
    if not os.path.exists(script):
        print(f"[ABORT] Script missing: {script}")
        return False

    command = [interpreter, script] + args
    
    try:
        subprocess.check_call(command, cwd=PROJECT_ROOT) 
        print(f"[SUCCESS] {step_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] {step_name} exit code: {e.returncode}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def main():
    if not os.path.exists(SCRIPT_MAIN) or not os.path.exists(SCRIPT_TEXT2VIDEO):
        print("\n[CRITICAL] One or more scripts are missing. Check logs above.")
        sys.exit(1)

    start = time.time()
    print("\n[START] Starting Generation Pipeline...")
    
    for step, python, script, args in WORKFLOW:
        if not run_step(step, python, script, args):
            print("[STOP] Pipeline failed.")
            sys.exit(1)

    print("=" * 50)
    print(f"[DONE] Finished in {time.time() - start:.1f}s")
    print("=" * 50)

if __name__ == "__main__":
    main()  