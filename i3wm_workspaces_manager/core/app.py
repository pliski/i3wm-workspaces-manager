import i3ipc
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib


class I3WorkspacesManager:
    def __init__(self):
        self.i3 = i3ipc.Connection()
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
        
        self.creator_window = WorkspaceCreatorWindow()
        self.switcher_window = WorkspaceSwitcherWindow()
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