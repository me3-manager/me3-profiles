# Community Profiles Guide
The goal of this guide is to create a collection of mods with correct setups using `.me3` files, 
making it easy for users to install and configure mods reliably. Share your mod setups with the community! 
This guide explains how to manually create lightweight `.me3` profiles using Nexus Mods links.

## 1. Creating a Profile
You can create a `.me3` file using any text editor. The structure is simple and uses TOML format.

```toml
profileVersion = "v1"
description = "Storm Control with a two-part setup—config and profile, so both configurations appear in the mod config editor."
[[supports]]
game = "nightreign"


[[natives]]
nexus_link = "https://www.nexusmods.com/eldenringnightreign/mods/146"
config = ["Storm Control/StormControl/config.ini", "Storm Control/StormControl/profiles/NightfarerBots.ini"]
```

## 2. Global Settings (`Used by me3-manager`)
- `description`: A short explanation of what your profile does. This appears in the Community Search results.

## 3. Mod Entries (`Used by me3-manager`)
- `nexus_link`: Full URL to the Nexus mod page. ME3 Manager will prompt the user to download it.
- `mod_folder`: (Optional) Specify which subfolder inside the downloaded archive to install.
```toml
[[packages]]
nexus_link = "https://www.nexusmods.com/eldenring/mods/541"
mod_folder = "path/to/mod"
```

## 4. Submitting Your Profile
Contributions are welcome! Feel free to submit them via pull requests.

## 5. Advanced: Custom Install Scripts
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

## 6. Contributing
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
