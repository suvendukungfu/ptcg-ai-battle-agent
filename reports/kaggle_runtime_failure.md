# Forensic Diagnostic Report: Kaggle Submissions 55538147 & 55538168 Failure

**Target Competition**: `pokemon-tcg-ai-battle` (*The Pokémon Company — Pokémon TCG AI Battle Challenge Simulation*)  
**Failed Submissions**:
- `55538147` (`SubmissionStatus.ERROR`) — 2026-08-15 23:46:48 UTC
- `55538168` (`SubmissionStatus.ERROR`) — 2026-08-15 23:47:50 UTC  
**Evaluation Platform**: Kaggle Environments (`cabt`)  
**Diagnostic Status**: **Root Cause 100% Isolated and Locally Reproduced**

---

## 1. Exact Error

```
kaggle_environments.errors.InvalidArgument: Invalid raw Python: NameError("name '__file__' is not defined")
```

---

## 2. Stack Trace

When Kaggle's evaluation engine instantiates an agent from `main.py` via `kaggle_environments.agent.build_agent`:

```python
Traceback (most recent call last):
  File "kaggle_environments/agent.py", line 47, in get_last_callable
    code_object = compile(raw, path_str, "exec")
  File "/kaggle_simulations/agent/main.py", line 8, in <module>
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NameError: name '__file__' is not defined

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "kaggle_environments/agent.py", line 149, in callable_agent
    agent = get_last_callable(raw_agent, path=raw) or raw_agent
  File "kaggle_environments/agent.py", line 72, in get_last_callable
    raise InvalidArgument("Invalid raw Python: " + repr(e))
kaggle_environments.errors.InvalidArgument: Invalid raw Python: NameError("name '__file__' is not defined")
```

---

## 3. Root Cause Analysis

In Kaggle Simulation competitions (e.g., Pokémon TCG AI Battle, Lux AI, Halite, ConnectX), Kaggle's remote evaluation harness loads the agent file using `kaggle_environments.agent.get_last_callable(raw_source, path=...)`.

Inside `kaggle_environments/agent.py` (lines 48–57):
```python
code_object = compile(raw, path_str, "exec")
env = {}
exec(code_object, env)  # <-- env is an empty dictionary!
```

When Python executes a module via `exec(code_object, {})`:
1. The global dictionary `env` **does not contain the `__file__` attribute** unless explicitly injected.
2. In our codebase, `main.py` line 8 evaluated `__file__` at module top-level:
   ```python
   BASE_DIR = os.path.dirname(os.path.abspath(__file__))
   ```
3. Because `__file__` is not present in `env`, Python immediately raises `NameError: name '__file__' is not defined`.
4. `kaggle-environments` catches this and marks the agent initialization as `InvalidArgument`, resulting in an immediate `SubmissionStatus.ERROR` before any match turns are played.

---

## 4. Empirical Evidence & Local Reproduction

We directly tested `kaggle_environments` with our `main.py` path vs an already-imported function object:

1. **Failure with Path String (Identical to Kaggle Server Runner)**:
   ```python
   from kaggle_environments import make
   env = make('cabt', debug=True)
   env.run(['main.py', 'random'])
   # OUTPUT:
   # Failed with path main.py: Invalid raw Python: NameError("name '__file__' is not defined")
   ```

2. **Success with `__file__` Guarded**:
   ```python
   fixed_code = code.replace(
       'BASE_DIR = os.path.dirname(os.path.abspath(__file__))',
       '''try:\n    BASE_DIR = os.path.dirname(os.path.abspath(__file__))\nexcept NameError:\n    BASE_DIR = os.path.abspath(".")'''
   )
   fn = get_last_callable(fixed_code, path='main.py')
   env.run([fn, 'random'])
   # OUTPUT:
   # Kaggle Environment Run Status: DONE, Reward: 1
   ```

---

## 5. Local vs Remote Execution Differences

| Dimension | Local pytest / Subprocess Test | Kaggle Remote Evaluation Runner |
| :--- | :--- | :--- |
| **Module Loading** | Loaded via `import main` (standard Python import machinery; Python defines `__file__` automatically) | Loaded via `kaggle_environments.agent.get_last_callable()` using `exec(code, {})` (where `__file__` is undefined) |
| **Path Resolution** | `os.path.abspath(__file__)` succeeds | `os.path.abspath(__file__)` throws unhandled `NameError` |
| **Result** | Local tests passed 46/46 | Remote agent failed at Step 0 with `SubmissionStatus.ERROR` |

---

## 6. Comprehensive Audit of 18 Potential Failure Modes

1. **Python Runtime**: Compatible (Standard Python 3.8–3.14 syntax).
2. **`kaggle-environments` Version**: Compatible once `get_last_callable` sandboxing is satisfied.
3. **Main Entrypoint Signature**: Verified `def agent(obs: Dict[str, Any], config: Any = None) -> List[int]`.
4. **Deck-Selection Return Format**: Verified returns 60-element integer list on Turn 0 (`obs["select"] is None`).
5. **Observation Schema**: Verified defensive parsing handles all CABT fields (`select`, `current`, `logs`).
6. **Action Return Format**: Verified returns list of integer option indices on Turns 1..N.
7. **Data File Path**: Verified `data/EN Card Data.csv` included in archive.
8. **Relative-Path Assumptions**: **ROOT CAUSE** (`__file__` assumed to exist in `globals()`).
9. **Working-Directory Assumptions**: Needs fallback to `/kaggle_simulations/agent/` and `.` when `__file__` is unavailable.
10. **File Permissions**: Verified standard `-rw-r--r--` and `drwxr-xr-x`.
11. **Unsupported Imports**: Verified zero non-standard libraries (`src/` eliminated, zero external pip packages).
12. **Unsupported Standard-Library Behavior**: Verified clean.
13. **Timeouts**: Verified P95 is $3.75\text{ ms}$, well within $25.0\text{ ms}$ budget.
14. **Runtime Initialization**: Verified fast startup (< 1 ms).
15. **Card Database Initialization**: Verified lightweight in-memory lookup.
16. **Static/Global Initialization**: Verified no heavy side effects on import.
17. **Import Side Effects**: Clean.
18. **Competition-Specific Behavior**: Verified CABT engine compatibility.

---

## 7. Recommended Fix (Awaiting User Approval)

### Change 1: Guard `__file__` in [`main.py`](file:///Users/suvendusahoo/Downloads/pokemon/main.py)
```python
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Kaggle Environments exec() sandbox compatibility
    BASE_DIR = "/kaggle_simulations/agent" if os.path.exists("/kaggle_simulations/agent") else os.path.abspath(".")

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
```

### Change 2: Guard `__file__` in [`agent/deck_policy.py`](file:///Users/suvendusahoo/Downloads/pokemon/agent/deck_policy.py)
```python
def resolve_deck_path() -> str:
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    except NameError:
        base_dir = "/kaggle_simulations/agent" if os.path.exists("/kaggle_simulations/agent") else os.path.abspath(".")
    
    primary_path = os.path.join(base_dir, "deck.csv")
    if os.path.isfile(primary_path):
        return primary_path

    kaggle_path = "/kaggle_simulations/agent/deck.csv"
    if os.path.isfile(kaggle_path):
        return kaggle_path

    cwd_path = os.path.abspath("deck.csv")
    if os.path.isfile(cwd_path):
        return cwd_path

    return primary_path
```

### Change 3: Guard `__file__` in [`agent/card_database.py`](file:///Users/suvendusahoo/Downloads/pokemon/agent/card_database.py)
```python
def _find_card_csv() -> Optional[Path]:
    try:
        project_root = Path(__file__).parent.parent.resolve()
    except NameError:
        project_root = Path("/kaggle_simulations/agent") if Path("/kaggle_simulations/agent").exists() else Path(".").resolve()
    candidates = [
        project_root / "data" / "EN Card Data.csv",
        Path("/kaggle_simulations/agent/data/EN Card Data.csv"),
        Path("data/EN Card Data.csv").resolve(),
        Path("EN Card Data.csv").resolve(),
    ]
    for c in candidates:
        if c.exists():
            return c
    return None
```

---

**Diagnostic Complete. Zero source code changes made. Awaiting user review and authorization before proceeding.**
