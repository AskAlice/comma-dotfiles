## comma.ai command-line additions and practical tooling for all

improving the dev workflow friction is paramount to innovating [openpilot](https://github.com/commaai/openpilot)

***PRs accepted!** What cool shit do you do to your ssh session with your car??*

This repo is very much in active development! Expect it to evolve greatly over the next few weeks

<img src="https://emu.bz/xmf" alt="" />

# Getting Started

```bash
bash <(curl -fsSL install.emu.sh) # the brain of the bird
source /home/.bashrc
```

<img src="https://thumbs.gfycat.com/DopeyHairyGeese-size_restricted.gif" alt ="" />

---
Read the README for <https://github.com/b-ryan/powerline-shell>. You will need to [install the fonts on the computer/terminal emulator that you SSH from](https://github.com/powerline/fonts)

Alternately, you can install [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts), as it provides more icons than powerline fonts, and is more maintained.

The default directory of your bash/ssh session is now `/data/openpilot`. Much easier to git pull after shelling in.

# welcome to the family

<img src="https://emu.bz/gay" alt="" height="250px" />

Emu my neo!
You should now be able to use the `emu` command.

# Updating

Once you've installed, you can update via the utility

```bash
emu update
```

This will essentially perform a git pull and replace all current files in the `/data/community/.oh-my-comma` directory with new ones, if an update is available, as well as check the integrity of the files that must remain elsewhere on the filesystem such as the .bashrc and powerline configs

# Commands

### General
- `emu update`: 🎉 Updates this tool, recommended to restart ssh session
- `emu uninstall`: 👋 Uninstalls emu
### Fork management
- [`emu fork`](#emu-fork-manage-installed-forks-or-install-a-new-one): 🍴 Manage installed forks, or install a new one
### Panda
- [`emu panda`](#emu-panda): 🐼 panda interfacing tools
### Debugging
- [`emu debug`](#emu-debug): de-🐛-ing tools
- [`emu device`](#emu-device): 📈 Statistics about your device
---

#### `emu fork`: 🍴 Manage installed forks, or install a new one
- `emu fork switch`: 🍴 Switch between any openpilot fork
  - Arguments 💢:
    - username: 👤 The username of the fork's owner to install
    - branch (optional): 🌿 Branch to switch to, will use default branch if not provided
  - Example 📚:
    - `emu fork switch stock devel`
- `emu fork list`: 📜 See a list of installed forks and branches
  - Arguments 💢:
    - fork (optional): 🌿 See branches of specified fork
  - Example 📚:
    - `emu fork list stock`

#### `emu panda`: 🐼 panda interfacing tools
- `emu panda flash`: 🐼 flashes panda with make recover (usually works with the C2)
- `emu panda flash2`: 🎍 flashes panda using Panda module (usually works with the EON)

#### `emu debug`: de-🐛-ing tools
- `emu debug controlsd`: logs controlsd to /data/output.log by default
  - Arguments 💢:
    - -o, --output: Name of file to save log to
  - Example 📚:
    - `emu debug controlsd /data/controlsd_log`

#### `emu device`: 📈 Statistics about your device
- `emu device battery`: 🔋 see information about the state of your battery
- `emu device reboot`: ⚡ safely reboot your device
- `emu device shutdown`: 🔌 safely shutdown your device

# Git config

In a rw filesystem, you can edit your git config so you can push your changes up easily.

```bash
mount -o rw,remount /system
git config --global user.name "your_username"
git config --global user.email "your_email_address@example.com"
git config --global credential.helper store
git pull
mount -o r,remount /system
```

if the git pull fails, just do some action on git that requires authentication, and you should be good to go
