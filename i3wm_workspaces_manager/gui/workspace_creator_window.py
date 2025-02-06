import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from .base_window import BaseWindow
from ..core.workspace_manager import WorkspaceManager

class WorkspaceCreatorWindow(BaseWindow):
    def __init__(self):
        super().__init__(title="i3wm-workspaces-manager")
        self.workspace_manager = WorkspaceManager()
        
        # Create main container
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_margin_start(12)
        vbox.set_margin_end(12)
        vbox.set_margin_top(12)
        vbox.set_margin_bottom(12)
        self.add(vbox)
        
        # Create name entry
        name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        name_label = Gtk.Label(label="Workspace name:")
        self.name_entry = Gtk.Entry()
        name_box.pack_start(name_label, False, False, 0)
        name_box.pack_start(self.name_entry, True, True, 0)
        vbox.pack_start(name_box, True, True, 0)
        
        # Create rename checkbox
        self.rename_check = Gtk.CheckButton(label="Rename current workspace")
        vbox.pack_start(self.rename_check, True, True, 0)
        
        # Connect signals
        self.name_entry.connect('activate', self._on_activate)
        self.connect('show', self._on_show)
        
    def _on_show(self, widget):
        """Update the next available number when window is shown"""
        next_num = str(self.workspace_manager.get_next_available_number())
        self.name_entry.set_text(next_num)
        self.rename_check.set_active(False)        

    def _on_key_press(self, widget, event):
        """Handle key press events"""
        keyval = event.keyval
        keyval_name = Gdk.keyval_name(keyval)
        
        if keyval_name == 'Escape':
            self.hide()
            return True
        elif keyval_name == 'Return':
            self._on_activate(None)
            return True
            
        return False
        
    def _on_activate(self, widget):
        """Handle activation (Enter key or button click)"""
        name = self.name_entry.get_text()
        is_valid, error = self.workspace_manager.validate_workspace_name(name)
        
        if not is_valid:
            dialog = Gtk.MessageDialog(
                transient_for=self,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text=error
            )
            dialog.run()
            dialog.destroy()
            return
            
        if self.rename_check.get_active():
            self.workspace_manager.rename_current_workspace(name)
        else:
            self.workspace_manager.create_workspace(name)
            
        self.hide()
