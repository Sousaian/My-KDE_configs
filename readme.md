# My KDE Plasma Configuration

Personal dotfiles for Arch Linux with KDE Plasma desktop environment.

## Contents

- `.bashrc` - Bash shell configuration
- `.zshrc` - Zsh shell configuration
- `kdeglobals` - KDE global settings (theme, colors, fonts)
- `kwinrc` - KWin window manager settings
- `plasma-org.kde.plasma.desktop-appletsrc` - Plasma desktop layout and widgets
- `kitty/` - Kitty terminal emulator configuration
  - `kitty.conf` - Main config
  - `theme.conf` - Color theme
  - `userprefs.conf` - User preferences

## Installation

### Clone the repository

```bash
git clone https://github.com/Sousaian/My-KDE_configs.git ~/dotfiles
cd ~/dotfiles
```

### Apply configurations

**Shell configs:**
```bash
cp .bashrc ~/
cp .zshrc ~/
```

**KDE configs:**
```bash
cp kdeglobals ~/.config/
cp kwinrc ~/.config/
cp plasma-org.kde.plasma.desktop-appletsrc ~/.config/
```

**Kitty config:**
```bash
mkdir -p ~/.config/kitty
cp kitty/* ~/.config/kitty/
```

### Apply changes

Log out and back in, or restart Plasma:
```bash
killall plasmashell && plasmashell &
```

## System Info

- **OS:** Arch Linux
- **DE:** KDE Plasma
- **Terminal:** Kitty
- **Shell:** Zsh / Bash

## Notes

These configs are personal and may require adjustment for your system.

Backup your existing configs before applying these.
