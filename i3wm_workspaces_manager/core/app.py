import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

import i3ipc
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

CONNECT_TIMEOUT_SEC = 5


def _get_i3_socket_path():
    """Resolve i3/sway IPC socket path without blocking on X11."""
    path = os.environ.get('I3SOCK') or os.environ.get('SWAYSOCK')
    if path:
        return path
    try:
        out = subprocess.run(
            ['i3', '--get-socketpath'],
            capture_output=True,
            text=True,
            timeout=2,
        )
        if out.returncode == 0 and out.stdout:
            return out.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


class I3WorkspacesManager:
    def __init__(self):
        print('i3 Workspaces Manager: starting…', flush=True)
        socket_path = _get_i3_socket_path()
        if socket_path:
            print(f'i3 Workspaces Manager: using socket {socket_path}', flush=True)

        def connect_and_test():
            conn = i3ipc.Connection(socket_path=socket_path)
            conn.get_workspaces()
            return conn

        try:
            with ThreadPoolExecutor(max_workers=1) as ex:
                fut = ex.submit(connect_and_test)
                self.i3 = fut.result(timeout=CONNECT_TIMEOUT_SEC)
        except FuturesTimeoutError:
            print('Error: Connection to i3 timed out.', file=sys.stderr, flush=True)
            print(
                'Make sure i3 is running and, if needed, set I3SOCK to the IPC socket path.',
                file=sys.stderr,
                flush=True,
            )
            sys.exit(1)
        except Exception as e:
            print(f'Error: Could not connect to i3: {e}', file=sys.stderr, flush=True)
            print('Make sure i3 is running and accessible.', file=sys.stderr, flush=True)
            sys.exit(1)

        print('i3 Workspaces Manager: connected. Listening for keybindings.', flush=True)
        self.creator_window = None
        self.switcher_window = None
        
    def run(self):
        """Start the application and listen for events"""
        # Subscribe to custom IPC events
        self.i3.on('binding', self._on_binding_event)
        
        # Start GTK main loop
        GLib.idle_add(self._setup_gui)
        
        # Start i3ipc event loop in a separate thread
        from threading import Thread
        Thread(target=self.i3.main, daemon=True).start()
        
        Gtk.main()
        
    def _setup_gui(self):
        """Initialize GUI components"""
        from i3wm_workspaces_manager.gui.workspace_switcher_window import (         
            WorkspaceSwitcherWindow
        )
        from i3wm_workspaces_manager.gui.workspace_creator_window import (
            WorkspaceCreatorWindow,         
        )
        
        self.creator_window = WorkspaceCreatorWindow(self.i3)
        self.switcher_window = WorkspaceSwitcherWindow(self.i3)
        return False  # Don't repeat this idle callback
        
    def _on_binding_event(self, i3conn, event):
        """Handle custom IPC events from i3wm"""
        if event.binding.command == 'nop workspace_creator':
            GLib.idle_add(self._show_creator_window)
        elif event.binding.command == 'nop workspace_switcher':
            GLib.idle_add(self._show_switcher_window)
            
    def _show_creator_window(self):
        """Show the workspace creator window"""
        self.creator_window.show_all()
        return False
        
    def _show_switcher_window(self):
        """Show the workspace switcher window"""
        self.switcher_window.show_all()
        return False 