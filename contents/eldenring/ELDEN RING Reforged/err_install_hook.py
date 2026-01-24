import logging
import shutil

log = logging.getLogger(__name__)


def on_prepare_install(context):
    """
    Organizes Elden Ring Reforged files (ERRv* -> Reforged).
    """
    mods_dir = context["mods_dir"]
    profile_data = context.get("profile_data", {})

    # 1. Locate ERR folder (Nexus install -> mods_dir, Local install -> root_path)
    target_folder = _find_err_folder(mods_dir) or _find_err_folder(context["root_path"])

    if not target_folder:
        log.warning("[ERR Hook] Could not find ERR version folder.")
        return

    log.info("[ERR Hook] Processing: %s", target_folder)

    # 2. Move dll -> mod/dll
    dll_dir = target_folder / "dll"
    mod_dir = target_folder / "mod"

    if dll_dir.exists() and mod_dir.exists():
        log.info("Moving dll folder into mod/dll")
        dest = mod_dir / "dll"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.move(str(dll_dir), str(dest))

    # 3. Rename to Reforged
    final_path = target_folder.parent / "Reforged"
    if target_folder != final_path:
        log.info("Renaming to %s", final_path.name)
        if final_path.exists():
            shutil.rmtree(final_path)
        target_folder.rename(final_path)

    # 4. Point profile to new path
    for pkg in profile_data.get("packages", []):
        pkg["path"] = "Reforged"
        pkg["id"] = "Reforged"


def _find_err_folder(base_path):
    if not base_path or not base_path.exists():
        return None
    return next(
        (p for p in base_path.iterdir() if p.is_dir() and p.name.startswith("ERRv")),
        None,
    )
