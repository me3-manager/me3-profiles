import logging
import shutil

log = logging.getLogger(__name__)


def on_post_install(context):
    """
    Post-install hook for MMV + SoTE & DS3 Weapons.
    Merges the Compatibility Patch and SoTE & DS3 Weapons into the
    More Map Variations mod folder, then cleans up leftovers.
    """
    mods_dir = context["mods_dir"]
    log.info("[MMV Hook] Starting post-install in: %s", mods_dir)

    mmv_folder = _find_folder(mods_dir, ["More Map Variations"])
    compat_folder = _find_folder(mods_dir, ["Compatibility Patch for More Weapons"])
    sote_folder = _find_folder(mods_dir, ["Sote & DS3 Weapons", "SotE and ds3 weapons", "Sote and DS3 Weapons"])

    if not mmv_folder:
        log.warning("[MMV Hook] Could not find More Map Variations folder.")
        return

    _merge_into(mmv_folder, sote_folder, "SoTE & DS3 Weapons")
    _merge_into(mmv_folder, compat_folder, "Compatibility Patch")

    _cleanup_leftovers(
        mods_dir,
        mmv_folder,
        [
            "Compatibility Patch for More Weapons",
            "Sote & DS3 Weapons",
            "SotE and ds3 weapons",
            "Sote and DS3 Weapons",
        ],
    )

    final_name = "MMV + SoTE & DS3 Weapons"
    final_path = mmv_folder.parent / final_name
    if mmv_folder.exists():
        if final_path.exists():
            shutil.rmtree(final_path)
        mmv_folder.rename(final_path)
        log.info("[MMV Hook] Renamed folder to: %s", final_name)
    else:
        log.warning("[MMV Hook] MMV folder disappeared before rename.")

    log.info("[MMV Hook] Done.")


def _find_folder(base_path, names):
    if not base_path or not base_path.exists():
        return None
    candidates = [n.casefold() for n in names]
    for child in base_path.iterdir():
        if child.is_dir() and child.name.casefold() in candidates:
            return child
    for child in base_path.iterdir():
        if child.is_dir():
            for grandchild in child.iterdir():
                if grandchild.is_dir() and grandchild.name.casefold() in candidates:
                    return grandchild
    return None


def _cleanup_leftovers(base_path, keep, names):
    for child in list(base_path.iterdir()):
        if child.is_dir() and child != keep and child.name.casefold() in {n.casefold() for n in names}:
            try:
                shutil.rmtree(child)
                log.info("[MMV Hook] Cleaned up leftover: %s", child.name)
            except Exception as e:
                log.warning("[MMV Hook] Could not remove %s: %s", child.name, e)


def _merge_into(target, source, label):
    if not source or not source.exists():
        log.warning("[MMV Hook] %s folder not found, skipping.", label)
        return

    log.info("[MMV Hook] Merging %s into %s", label, target.name)
    for item in source.iterdir():
        dest = target / item.name
        if dest.exists():
            if dest.is_dir():
                shutil.rmtree(dest)
            else:
                dest.unlink()
        shutil.move(str(item), str(dest))

    try:
        shutil.rmtree(source)
        log.info("[MMV Hook] Cleaned up %s folder.", label)
    except Exception as e:
        log.warning("[MMV Hook] Could not remove %s: %s", label, e)
