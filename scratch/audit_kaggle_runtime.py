import os
import sys
import shutil
import subprocess

SUBMISSION_TAR = "/Users/suvendusahoo/Downloads/pokemon/submission.tar.gz"
TEST_DIR = "/tmp/kaggle_runtime_audit"

if os.path.exists(TEST_DIR):
    shutil.rmtree(TEST_DIR)
os.makedirs(TEST_DIR, exist_ok=True)

# Extract submission
subprocess.run(["tar", "-xzf", SUBMISSION_TAR, "-C", TEST_DIR], check=True)

print(f"Extracted archive into {TEST_DIR}. Files:")
for root, dirs, files in os.walk(TEST_DIR):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), TEST_DIR)
        print(f"  {rel}")

# Clean Python test subprocess with isolated cwd and clean env
test_script = """
import sys
import os
import traceback

print("CWD:", os.getcwd())
print("sys.path initially:", sys.path)

# Test import
try:
    import main
    print("SUCCESS: Imported main")
except Exception as e:
    print("FAILED import main:", e)
    traceback.print_exc()
    sys.exit(1)

# Test Turn 0 (Deck Submission)
try:
    deck = main.agent({"select": None})
    print(f"SUCCESS: Turn 0 returned {len(deck)} cards: {deck[:5]}...{deck[-5:]}")
    assert len(deck) == 60, f"Deck has {len(deck)} cards instead of 60"
except Exception as e:
    print("FAILED Turn 0 deck submission:", e)
    traceback.print_exc()
    sys.exit(1)

# Test Turn 1 with Kaggle CABT environment
try:
    from kaggle_environments import make
    env = make("cabt", debug=True)
    
    # Run 1 full game against random bot
    steps = env.run([main.agent, "random"])
    final_step = steps[-1]
    print(f"Game completed. Steps: {len(steps)}, Status: {final_step[0].status}, Reward: {final_step[0].reward}")
    
    for i, step in enumerate(steps[:5]):
        act_0 = step[0].action
        stat_0 = step[0].status
        print(f"  Step {i}: Action={act_0}, Status={stat_0}")

    if final_step[0].status == "ERROR" or final_step[0].status == "INVALID":
        print("FAILED: Step resulted in error/invalid status")
        sys.exit(1)
        
    print("SUCCESS: Full game executed with 0 errors and 0 invalid actions.")

except Exception as e:
    print("FAILED Kaggle Environment test:", e)
    traceback.print_exc()
    sys.exit(1)
"""

script_path = os.path.join(TEST_DIR, "test_runner.py")
with open(script_path, "w") as f:
    f.write(test_script)

env_clean = os.environ.copy()
env_clean.pop("PYTHONPATH", None)

proc = subprocess.run(
    ["/Users/suvendusahoo/Downloads/pokemon/.venv/bin/python", "test_runner.py"],
    cwd=TEST_DIR,
    env=env_clean,
    capture_output=True,
    text=True
)

print("\n--- Subprocess Output ---")
print(proc.stdout)
if proc.stderr:
    print("--- Subprocess Stderr ---")
    print(proc.stderr)

print("Exit code:", proc.returncode)
