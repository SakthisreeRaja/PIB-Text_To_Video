import subprocess
import sys
import os
import time


INTERPRETER_1_PATH = os.path.normpath("./venv_v2_2_1/Scripts/python.exe")
INTERPRETER_2_PATH = os.path.normpath("./venv_v1_1_3/Scripts/python.exe")


MAIN_SCRIPT_PATH = os.path.normpath("plain2output/main.py")
VIDEO_SCRIPT_PATH = os.path.normpath("text2video/text_imge.py")


WORKFLOW = [
   
    ("Phase 1: Audio Generation & Duration Calculation", INTERPRETER_1_PATH, MAIN_SCRIPT_PATH, ["audio"]),
    
    
    ("Phase 2: Video Creation (Duration Sync)", INTERPRETER_2_PATH, VIDEO_SCRIPT_PATH, []),
    
    
    ("Phase 3: Merge, Subtitles (if needed), & Finalize", INTERPRETER_1_PATH, MAIN_SCRIPT_PATH, ["merge"]),
]

def run_step(step_name, interpreter_path, program_path, args):
    
    
    command = [interpreter_path, program_path] + args
    
    print("-" * 50)
    print(f"STARTING STEP: {step_name}")
    print(f"Using Interpreter: {os.path.basename(os.path.dirname(interpreter_path))}")
    print(f"Executing: {' '.join(command)}")
    print("-" * 50)
    
    try:
        
        subprocess.check_call(command, stdout=sys.stdout, stderr=sys.stderr)
        
        print(f" SUCCESS: {step_name} completed successfully.")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f" ERROR: {step_name} FAILED with exit code {e.returncode}.")
        print("Please check the output above for the specific error from the subprocess.")
        return False
    except FileNotFoundError:
        print(f" FATAL ERROR: Interpreter or script not found.")
        print(f"Interpreter checked: {interpreter_path}")
        print(f"Script checked: {program_path}")
        print("Ensure the paths are correct and the environments are created.")
        return False


def main():
    
    start_time = time.time()
    
    for step_name, interpreter_path, program_path, args in WORKFLOW:
        if not run_step(step_name, interpreter_path, program_path, args):
            print("\n--- WORKFLOW HALTED ---")
            print(f"The step '{step_name}' failed. Please check the error details above.")
            sys.exit(1)

    print("\n====================================================")
    print(f" ALL STEPS COMPLETED! Final reel generation successful.")
    print(f"Total time taken: {time.time() - start_time:.2f} seconds.")
    print("====================================================")

if __name__ == "__main__":
    main()