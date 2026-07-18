# Multi-Object Rigging Toolkit

A PySide2 tool for Autodesk Maya that batch-processes constraints, attribute connections, and skin weight transfers across paired lists of **Source** and **Target** objects — instead of doing it one object at a time through Maya's native menus.

![Python](https://img.shields.io/badge/Python-2.7%20%7C%203-blue)
![Maya](https://img.shields.io/badge/Maya-PySide2-informational)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## Overview

Rigging and skinning setups often involve repeating the same operation across many objects. The Multi-Object Rigging Toolkit wraps these workflows into a single dockable Maya window with three tabs:

- **Constraint** — create or delete Parent / Point / Orient / Scale constraints across a list of Source/Target pairs, with per-axis control.
- **Connection** — connect standard transform attributes (translate/rotate/scale) or arbitrary custom attributes between Source and Target objects.
- **Copy Skin** — transfer skin weights from Source meshes onto Target meshes with all the options native to maya. 

All three tabs share the same Source/Target object lists and pairing logic, so you load your selection once and apply multiple operations against it. Confirmation dialogs before create/delete, and the whole batch is wrapped in a single undo chunk (`cmds.undoInfo`) so one **Ctrl+Z** undoes the entire operation.

## Features

### Source / Target pairing
Two mutually exclusive pairing modes, available on every tab:

| Mode | Behavior |
|---|---|
| **By Order** | Positional pairing: `source[i] → target[i]`. If only one source object is loaded, it's used to drive every target. |
| **By Name** | Each source is paired with a target found by stripping the source's trailing `_<token>` suffix (e.g. `_JNT`) and appending a user-defined suffix, searched within the source's own top-level hierarchy. |

Object lists support loading the current Maya selection, reordering items (↑ / ↓), and clearing. Full DAG paths are tracked internally so renamed/duplicate short names don't cause mismatches.

### Constraint tab
- Parent, Point, Orient, and Scale constraints.
- Maintain Offset toggle.
- Per-axis Translate / Rotate / Scale checkboxes (with an "All" convenience toggle) to control which axes get constrained.
- Delete existing constraints from the Target list.


### Connection tab
- Batch-connect standard Translate / Rotate / Scale attributes between Source and Target, per axis.
- Custom attribute connections between arbitrary driver/driven attribute pairs.
- Disconnect existing connections from the Target list.

![Constraint/Connection Tab](gifs\Constraint_connection_usage.gif)
### Copy Skin tab
- Surface association: Closest Point, Ray Cast, or Closest Component.
- Three configurable influence association fallbacks (None, Closest Bone, Closest Joint, One To One, Label, Name), matching Maya's `copySkinWeights` options.
- Skips pairs cleanly when a source has no skin cluster instead of failing the whole batch.

![Copy Skin Tab](gifs\copy_skinusage.gif)

## Installation

Directly Setting up Maya PYTHONPATH
1. Copy [main.py](main.py) into a directory on Maya's `PYTHONPATH` (e.g. your Maya `scripts` folder).
2. In the Maya Script Editor (Python tab), run:

```python
import main
main.show_window()
```

Re-running `show_window()` automatically closes any previously opened instance before opening a new one, so it's safe to re-run while iterating.

Or can keep The project folder anywhere, and using absolute path. 
```python
import sys
import importlib

project_path = r"<Add your project folder path>"
if project_path not in sys.path:
    sys.path.append(project_path)

import main 
importlib.reload(main)
main.show_window()
```

## Usage

1. Select your driver objects in the viewport/Outliner and click **Load Selected Objects** under **Source Objects**.
2. Select your driven objects and click **Load Selected Objects** under **Target Objects**.
3. Choose a pairing mode (**By Order** or **By Name**).
4. Switch to the tab for the operation you need (Constraint, Connection, or Copy Skin), configure the options, and run the action.
5. Confirm the action in the dialog that appears.

## Project Structure
```
main.py         # Current, actively developed version of the tool (RiggingUtilityTool)
Plan/           # UI mockups and workflow diagrams across design iterations (V1–V3)
```

`main.py` is the entry point — it is self-contained and does not depend on any other module
