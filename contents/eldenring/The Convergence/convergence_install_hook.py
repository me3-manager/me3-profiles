import logging
import shutil

log = logging.getLogger(__name__)


def on_post_install(context):
    """
    Post-install hook for Convergence ER.

    Goals:
    1. Organize DLLs/configs into a 'dll' folder.
    2. Flatten 'mod' folder contents to the root.
    3. Cleanup unused folders (modengine2, Resources).
    """
    mods_dir = context["mods_dir"]

    # Files to move into the 'dll' subfolder
    dll_files = [
        "altsaves.toml",
        "CMI.dll",
        "eldenring_alt_saves.dll",
        "erd_tools.ini",
        "ErdTools.dll",
        "erdyes.dll",
        "erdyes.ini",
        "ertransmogrify.dll",
        "ertransmogrify.ini",
        "Scripts-Data-Exposer-FS.dll",
    ]

    # Find the Convergence folder
    # We look for a folder that likely contains the mod structure
    target_folder = _find_convergence_folder(mods_dir)

    if not target_folder:
        log.warning("[Convergence Hook] Could not find Convergence folder.")
        return

    log.info("[Convergence Hook] Processing %s", target_folder.name)

    mod_dir = target_folder / "mod"

    if not mod_dir.exists():
        log.warning("[Convergence Hook] 'mod' folder not found in %s", target_folder)
        return

    # 1. Create 'dll' folder and move files
    dll_dir = mod_dir / "dll"
    dll_dir.mkdir(exist_ok=True)

    log.info("[Convergence Hook] Moving DLLs to %s", dll_dir)
    for file_name in dll_files:
        src = mod_dir / file_name
        if src.exists():
            dst = dll_dir / file_name
            shutil.move(str(src), str(dst))
        else:
            log.debug("File not found: %s", file_name)

    # 2. Flatten: Move everything from 'mod' to root
    log.info("[Convergence Hook] Flattening 'mod' folder to root")
    for item in mod_dir.iterdir():
        dest = target_folder / item.name

        # If destination exists, remove it first to avoid collision errors
        if dest.exists():
            if dest.is_dir():
                shutil.rmtree(dest)
            else:
                dest.unlink()

        shutil.move(str(item), str(dest))

    # 3. Cleanup
    # Remove empty 'mod' folder
    if mod_dir.exists():
        shutil.rmtree(mod_dir)

    # Remove unused folders provided by the download
    for unused in ["modengine2", "Resources"]:
        unused_path = target_folder / unused
        if unused_path.exists():
            shutil.rmtree(unused_path)
            log.info("Removed unused folder: %s", unused)

    log.info("[Convergence Hook] Installation cleanup complete.")


def _find_convergence_folder(base_path):
    """
    Helper to find the main Convergence folder.
    Prioritizes 'ConvergenceER' but accepts variations if necessary.
    """
    # 1. Direct check
    candidate = base_path / "ConvergenceER"
    if candidate.exists() and candidate.is_dir():
        return candidate

    # 2. Search for any folder starting with Convergence containing a 'mod' subfolder
    for child in base_path.iterdir():
        if child.is_dir() and "convergence" in child.name.lower():
            if (child / "mod").exists():
                return child

    return None
