import logging
import shutil

log = logging.getLogger(__name__)


def on_post_install(context):
    """
    Post-install cleanup for Elden Ring Reforged.
    Structure: ModRoot > mod > dll
    """
    mods_dir = context["mods_dir"]
    profile_data = context.get("profile_data", {})

    target_folder = _find_err_folder(mods_dir)
    if not target_folder:
        log.warning("[ERR Hook] Could not find ERRv* folder.")
        return

    log.info("[ERR Hook] Processing %s", target_folder.name)

    # 1. Move dll -> mod/dll
    dll_dir = target_folder / "dll"
    mod_dir = target_folder / "mod"

    if dll_dir.exists() and mod_dir.exists():
        log.info("Moving dll into mod/dll")
        dest_dll = mod_dir / "dll"
        if dest_dll.exists():
            shutil.rmtree(dest_dll)
        shutil.move(str(dll_dir), str(dest_dll))

    # 2. Move 'mod' folder to root (flatten)
    # We want: ModRoot/mod
    # target_folder is ModRoot/ERRv2.X.X.X

    root_dir = target_folder.parent
    final_mod_path = root_dir / "mod"

    moved_success = False

    if mod_dir.exists():
        if final_mod_path.exists():
            # If we are re-installing or it exists, clear the old one to ensure we get the fresh one
            shutil.rmtree(final_mod_path)

        log.info("Moving mod folder to root: %s", final_mod_path)
        shutil.move(str(mod_dir), str(final_mod_path))
        moved_success = True
    else:
        log.warning(
            "'mod' folder not found inside %s, cannot flatten structure.",
            target_folder.name,
        )

    # 3. Update profile to point to 'mod'
    # Only if we actually have a 'mod' folder now
    if final_mod_path.exists():
        for pkg in profile_data.get("packages", []):
            pkg["path"] = "mod"
            pkg["id"] = "Reforged"

    # 4. Clean up the rest (ERRv... folder)
    # SAFETY: Only delete if we successfully moved the important stuff out,
    # OR if we are sure we want to delete the leftovers.
    if moved_success:
        log.info("Cleaning up old container %s", target_folder.name)
        shutil.rmtree(target_folder)
    else:
        log.warning(
            "Skipping cleanup of %s because 'mod' folder was not moved/found.",
            target_folder.name,
        )


def _find_err_folder(base_path):
    if not base_path or not base_path.exists():
        return None

    # Check immediate children (ERRv...)
    err = _scan(base_path)
    if err:
        return err

    # Check one level deep
    for child in base_path.iterdir():
        if child.is_dir():
            err = _scan(child)
            if err:
                return err
    return None


def _scan(path):
    return next(
        (p for p in path.iterdir() if p.is_dir() and p.name.startswith("ERRv")),
        None,
    )
