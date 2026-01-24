import logging
import shutil

log = logging.getLogger(__name__)


def on_post_install(context):
    """
    Post-install cleanup for Elden Ring Reforged.
    Structure: ModRoot > [contents of mod folder including dll]
    """
    mods_dir = context["mods_dir"]

    target_folder = _find_err_folder(mods_dir)
    if not target_folder:
        log.warning("[ERR Hook] Could not find ERRv* folder.")
        return

    log.info("[ERR Hook] Processing %s", target_folder.name)

    # 1. Move dll -> mod/dll
    # This prepares the 'mod' folder to have everything we want
    dll_dir = target_folder / "dll"
    mod_dir = target_folder / "mod"

    if dll_dir.exists() and mod_dir.exists():
        log.info("Moving dll into mod/dll")
        dest_dll = mod_dir / "dll"
        if dest_dll.exists():
            shutil.rmtree(dest_dll)
        shutil.move(str(dll_dir), str(dest_dll))

    # 2. Flatten: Move contents of 'mod' folder to root
    # We want: ModRoot/* (contents of mod)
    root_dir = target_folder.parent
    moved_success = False

    if mod_dir.exists():
        log.info("Flattening structure: Moving contents of %s to %s", mod_dir, root_dir)
        for item in mod_dir.iterdir():
            dest = root_dir / item.name
            if dest.exists():
                if dest.is_dir():
                    shutil.rmtree(dest)
                else:
                    dest.unlink()

            shutil.move(str(item), str(dest))
        moved_success = True
    else:
        log.warning(
            "'mod' folder not found inside %s, cannot flatten structure.",
            target_folder.name,
        )

    # 3. Clean up the rest (ERRv... folder)
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
