# Community Profiles Guide
The goal of this guide is to create a collection of mods with correct setups using `.me3` files, 
making it easy for users to install and configure mods reliably. Share your mod setups with the community! 
This guide explains how to manually create lightweight `.me3` profiles using Nexus Mods links.

## 1. Creating a Profile

You can create a `.me3` file using any text editor (VS Code, Notepad++, etc.). The file uses the **TOML** format.

### Basic Structure
Every profile starts with these required fields:

```toml
profileVersion = "v1"
description = "A short description of this profile (e.g., 'Hard Mode + QoL')."

[[supports]]
game = "nightreign"  # The game slug (e.g., eldenring, nightreign, darksouls3)
```

### Adding Mods (`[[natives]]` vs `[[packages]]`)

You will list your mods under `[[natives]]` or `[[packages]]`.

- **`[[natives]]`**: Use this for **DLL mods** or mods that require direct file placement (e.g., `SeamlessCoop.dll`).
- **`[[packages]]`**: Use this for **general mods** (folders, archives, texture replacements) that are loaded via ModEngine.

#### Example: Adding a Mod with a Nexus Link
When you include a `nexus_link`, ME3 Manager will prompt the user to download the mod if they don't have it.

```toml
[[packages]]
nexus_link = "https://www.nexusmods.com/eldenring/mods/541"
mod_folder = "path/in/archive" # Optional: if the mod is inside a subfolder in the downloaded zip
```

#### Example: Exposing Config Files
You can list configuration files so users can edit them directly in ME3 Manager.

```toml
[[natives]]
nexus_link = "https://www.nexusmods.com/eldenring/mods/146"
config = ["Storm Control/config.ini"]
```

## 2. Testing Your Profile Locally

Before submitting your profile, you should verify it works:

1.  **Save your file** as `MyProfile.me3`.
2.  **Open ME3 Manager**.
3.  **Drag and drop** your `.me3` file into the application window (or use the Import feature if available).
4.  **Verify**:
    - Does it appear in the profile list?
    - Do the mods download correctly?
    - Does the game launch with the mods active?

## 3. Submitting Your Profile
Contributions are welcome! Feel free to submit them via pull requests.

## 4. Advanced: Custom Install Scripts
For complex mods that require specific installation logic (like moving files, cleaning up folders, or dynamic configuration), you can bundle a Python script with your profile.

### Enabling the Script
Add a `[metadata]` section to your `.me3` file and point to your script file:

```toml
[metadata]
install_script = "install_hook.py"
```

Ensure `install_hook.py` is included in the same folder as your `.me3` file (or in the same directory if submitting a PR).

### Script Structure
The script works by defining "hooks" that ME3 Manager calls at specific points. It runs using the manager's internal Python environment.

**Available Hooks:**
- `on_prepare_install(context)`: Runs *before* the main installation. Return `False` to cancel.
- `on_post_install(context)`: Runs *after* all files have been installed (but before the transaction is finalized).

**The `context` Dictionary:**
The `context` argument provides useful information:
- `mods_dir`: `Path` object to the game's mods directory.
- `profile_data`: Dictionary containing the parsed `.me3` profile data.
- `installed`: List of files/folders that were installed.
- `game_name`: Name of the game being modified.

### Example Script
```python
import logging
import shutil
from pathlib import Path

log = logging.getLogger(__name__)

def on_post_install(context):
    """
    Example: Flatten a nested folder structure after install.
    """
    mods_dir = context["mods_dir"]
    log.info("Running post-install script for %s", context["game_name"])
    
    # Example logic: Move contents of 'NestedFolder' to root
    target_dir = mods_dir / "ComplexMod" / "NestedFolder"
    dest_dir = mods_dir / "ComplexMod"
    
    if target_dir.exists():
        for item in target_dir.iterdir():
            dest = dest_dir / item.name
            if dest.exists():
                if dest.is_dir():
                    shutil.rmtree(dest)
                else:
                    dest.unlink()
            shutil.move(str(item), str(dest))
        
        # Cleanup empty folder
        shutil.rmtree(target_dir)
        log.info("Files moved successfully!")
```

### Important Notes
- **Libraries**: You can only import modules from the **Python Standard Library** (e.g., `os`, `shutil`, `json`, `re` and **PySide6**. You cannot use external packages like `numpy` or `requests` unless they happen to be bundled with the manager.
- **Safety**: Users will be prompted to approve the script before it runs.
- **Logging**: Use `logging.getLogger(__name__)` to write to the application log.

## 5. Contributing
We use [uv](https://github.com/astral-sh/uv) for Python project management and [Ruff](https://github.com/astral-sh/ruff) for linting.

> [!NOTE]
> **Only required if you are including a Python install script.**
> If you are only submitting a `.me3` profile without a custom script, you do not need to install `uv` or run these checks.

### Running CI Checks Locally
To verify your changes before submitting a pull request, you can run the linter locally:

1. **Install uv** (if not already installed):
   ```bash
   pip install uv
   ```

2. **Linting & Formatting**:
   ```bash
   # Run linter
   uv run ruff check .

   # Run formatter
   uv run ruff format .
   ```
