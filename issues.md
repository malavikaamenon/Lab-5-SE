# Issues found (Lab 5: scheduler_system.py)

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| `os.system("cat " + file)` (B605) | Security, High | 43 | Shell command built from a string; injection risk | Open the file and print its contents |
| Bare `except: pass` (B110, E722, W0702) | Security / Bug | 26-28 | Hides every error, including real bugs | Catch `KeyError` only and report "not found" |
| Mutable default `equipment_list=[]` (W0102) | Bug | 11 | Same list shared across calls | Default to `None`, copy into a new list |
| `open()` without `with` / encoding (R1732, W1514) | Resource leak | 35, 40 | `logConflicts` never closes its file | `with open(..., encoding="utf-8")` |
| `global next_reservation` (W0603) | Design | 12 | Hidden mutable global state | Keep counter in a `_state` dict |
| `logConflicts`, unused `a`/`a_more`/`c`, missing docstrings, `%` formatting | Style | various | Naming, dead variables, missing docs | Rename to `log_conflicts`, remove unused vars, add docstrings, use f-strings |
| E302, E305, E501 | Flake8 formatting | various | Blank lines and lines over 79 chars | Reformat |
| Backwards slot `"14-12"` accepted | Logic bug (not flagged) | 48 | Slot length printed as -2 | `parse_slot` validates start < end |
| Slot `1530` (int) accepted | Logic bug (not flagged) | 50 | Would crash `slot_hours` | `parse_slot` requires `HH-HH` |
| Equipment never checked | Logic bug (not flagged) | 15-16 | Pool could go negative; unknown item raised KeyError | Check availability before taking equipment |
| Double-booking still booked | Logic bug (not flagged) | 13-14 | Conflict logged but room booked anyway | Reject the booking and log the conflict |
| Conflicts never cleared | Logic bug (not flagged) | 39-41 | Old conflicts re-logged on each call | `conflicts.clear()` after logging |
| `main()` runs on import | Design | 59 | Side effect on import | `if __name__ == "__main__":` guard |

Note: Flake8 reports 0 issues after the fixes, so `flake8_after.txt` is empty.
