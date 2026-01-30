import sys
from pathlib import Path

import tomlkit
from tomlkit.exceptions import ParseError, TOMLKitError


def validate_profile(file_path: Path) -> bool:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            tomlkit.parse(content)
        # print(f"✅ Valid: {file_path}")
        return True
    except (ParseError, TOMLKitError) as e:
        print(f"❌ Invalid: {file_path}")
        print(f"   Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False


def main():
    root_dir = Path(__file__).parent.parent
    contents_dir = root_dir / "contents"

    if not contents_dir.exists():
        print(f"Error: contents directory not found at {contents_dir}")
        sys.exit(1)

    print(f"Scanning for .me3 files in {contents_dir}...")

    me3_files = list(contents_dir.rglob("*.me3"))
    if not me3_files:
        print("No .me3 files found.")
        sys.exit(0)

    print(f"Found {len(me3_files)} .me3 files.")

    failed = False
    for me3_file in me3_files:
        if not validate_profile(me3_file):
            failed = True

    if failed:
        print("\n❌ Validation failed for one or more profiles.")
        sys.exit(1)
    else:
        print("\n✅ All profiles validated successfully.")
        sys.exit(0)


if __name__ == "__main__":
    main()
