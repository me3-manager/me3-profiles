import logging
import shutil

log = logging.getLogger(__name__)


def on_post_install(context):
    """
    Post-install hook for Convergence ER.
    Goals:
    1. Locate 'ConvergenceER/mod' folder.
    2. Move specific DLLs/configs from 'mod' to 'mod/dll'.
    3. Move ALL contents of 'mod' to the root (flattening 'mods_dir/ConvergenceER').
    4. Delete the original 'ConsergenceER' container (if path structure created one) or just the empty 'mod' folder.
    """
    mods_dir = context["mods_dir"]
    log.info("[Convergence Hook] Starting post-install in: %s", mods_dir)

    # 1. Locate the inner content folder
    # We expect: mods_dir / "The Convergence" / "ConvergenceER" / "mod"
    # Or just: mods_dir / "ConvergenceER" / "mod"

    # Let's search for "ConvergenceER"
    convergence_root = _find_convergence_folder(mods_dir)
    if not convergence_root:
        log.warning("[Convergence Hook] Could not find ConvergenceER folder.")
        return

    mod_content_dir = convergence_root / "mod"
    if not mod_content_dir.exists():
        log.warning("[Convergence Hook] 'mod' folder not found at: %s", mod_content_dir)
        return

    log.info("[Convergence Hook] Found content at: %s", mod_content_dir)

    # 2. Create 'dll' folder inside 'mod' and move specific files
    dll_dir = mod_content_dir / "dll"
    dll_dir.mkdir(exist_ok=True)

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

    for fname in dll_files:
        src = mod_content_dir / fname
        if src.exists():
            dst = dll_dir / fname
            shutil.move(str(src), str(dst))

    # 3. Flatten!
    # We want the CONTENTS of 'mod' to become the contents of 'The Convergence' (the root of this mod installation)

    # The "root" of this mod installation is usually `convergence_root.parent` if the user installed it via a profile
    # named "The Convergence" which put files into "The Convergence" folder.

    # If the structure is: .../The Convergence/ConvergenceER/mod
    # We want: .../The Convergence/[contents of mod]

    install_root = convergence_root.parent
    log.info("[Convergence Hook] Flattening to: %s", install_root)

    for item in mod_content_dir.iterdir():
        dest = install_root / item.name
        if dest.exists():
            if dest.is_dir():
                shutil.rmtree(dest)
            else:
                dest.unlink()

        shutil.move(str(item), str(dest))

    # 4. Cleanup
    # Remove the now empty 'mod' folder and its parent 'ConvergenceER'
    try:
        shutil.rmtree(convergence_root)
        log.info("[Convergence Hook] Cleanup successful")
    except Exception as e:
        log.warning("Cleanup failed: %s", e)


def _find_convergence_folder(base_path):
    """
    Search recursively for a folder named 'ConvergenceER' that contains a 'mod' subfolder.
    """
    # Check immediate children first
    for child in base_path.iterdir():
        if child.is_dir():
            if child.name == "ConvergenceER" and (child / "mod").exists():
                return child
            # Also check if we are already inside? No, base_path is mods_dir

    # Check 1 level deep (common if unzipped into a folder)
    for child in base_path.iterdir():
        if child.is_dir():
            possible = child / "ConvergenceER"
            if possible.exists() and (possible / "mod").exists():
                return possible

    return None
