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

### 4. Submitting Your Profile
Contributions are welcome! Feel free to submit them via pull requests.
