# i3wm-workspaces-manager

A simple GTK-based workspace manager for i3wm that helps you create, rename, and switch between workspaces efficiently.

## Features

- Quick workspace creation with automatic numbering
- Workspace renaming
- Fast workspace switching with keyboard navigation
- Minimal GTK interface
- Integrates with i3wm's IPC

## Installation

Clone the repository
```sh
git clone https://github.com/yourusername/i3wm-workspaces-manager.git
cd i3wm-workspaces-manager
```

Install dependencies
```sh
poetry install
```

Run the application
```sh
poetry run i3wm-workspaces-manager
```

## Configuration

Add the appropriate bindings to your i3 config file (`~/.config/i3/config`), for example:

```txt
# Workspace manager bindings
bindsym $mod+n nop workspace_creator # Show workspace creator
bindsym $mod+m nop workspace_switcher # Show workspace switcher
```

## Usage

- Press `$mod+n` to create/rename workspaces:
  - Enter a name or accept the suggested number
  - Check the "Rename current workspace" box to rename instead of create
  - Press `Enter` to confirm or `Escape` to cancel

- Press `$mod+m` to switch workspaces:
  - Use `Up`/`Down` arrows to navigate
  - Press `Enter` to switch to selected workspace
  - Press `Escape` to cancel

## Development

Run tests
```sh
poetry run pytest
```
Run the application
```sh
poetry run i3wm-workspaces-manager
```

### Dependencies

- [i3ipc-python](https://github.com/altdesktop/i3ipc-python)
- [PyGObject](https://github.com/GNOME/pygobject)
- [Poetry](https://python-poetry.org/)

## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE](LICENSE) file for details.