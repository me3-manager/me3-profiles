"""
Cinders Mod Installation Script

This script merges the 'parts' folder from Cinders Models into the main Cinders folder
after both packages have been installed.
"""

import logging
import shutil

log = logging.getLogger(__name__)


def on_post_install(context):
    """
    Merge Cinders Models 'parts' folder into main Cinders folder.

    Expected structure after download:
    - Cinders/           (main mod files)
    - Cinders_Models_Temp/  (contains Cinders/parts)

    Result:
    - Cinders/           (main mod files + parts folder)
    """
    mods_dir = context["mods_dir"]
    log.info("Running post-install script for Cinders mod")

    # Paths
    cinders_main = mods_dir / "Cinders"
    cinders_models_temp = mods_dir / "Cinders_Models_Temp"

    # The Models archive extracts to Cinders_Models_Temp/Cinders/parts
    # We need to find the 'parts' folder within it
    parts_source = None

    # Check direct 'parts' folder
    if (cinders_models_temp / "parts").exists():
        parts_source = cinders_models_temp / "parts"
    # Check nested 'Cinders/parts' folder
    elif (cinders_models_temp / "Cinders" / "parts").exists():
        parts_source = cinders_models_temp / "Cinders" / "parts"

    if not parts_source:
        log.warning("Could not find 'parts' folder in Cinders_Models_Temp")
        # Try to find parts folder recursively
        for p in cinders_models_temp.rglob("parts"):
            if p.is_dir():
                parts_source = p
                log.info("Found parts folder at: %s", parts_source)
                break

    if parts_source and parts_source.exists():
        parts_dest = cinders_main / "parts"

        # Move or copy the parts folder
        if parts_dest.exists():
            log.info("Parts folder already exists, merging contents...")
            for item in parts_source.iterdir():
                dest = parts_dest / item.name
                if dest.exists():
                    if dest.is_dir():
                        shutil.rmtree(dest)
                    else:
                        dest.unlink()
                shutil.move(str(item), str(dest))
        else:
            log.info("Moving parts folder to Cinders main directory...")
            shutil.move(str(parts_source), str(parts_dest))

        log.info("Parts folder merged successfully!")
    else:
        log.warning("Parts source folder not found, skipping merge")

    # Cleanup: Remove the temporary models folder
    if cinders_models_temp.exists():
        try:
            shutil.rmtree(cinders_models_temp)
            log.info("Cleaned up temporary Cinders_Models_Temp folder")
        except Exception as e:
            log.warning("Could not remove temp folder: %s", e)
