import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from .base_window import BaseWindow
from ..core.workspace_manager import WorkspaceManager

class WorkspaceSwitcherWindow(BaseWindow):
    def __init__(self):
        super().__init__(title="i3wm Workspace Switcher")
        self.workspace_manager = WorkspaceManager()
        
        # Create scrolled window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(200)
        self.add(scrolled)
        
        # Create listbox
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        scrolled.add(self.listbox)
        
        # Connect signals
        self.listbox.connect('row-activated', self._on_row_activated)
        self.connect('show', self._on_show)
        self.connect('key-press-event', self._on_key_press)
        
    def _on_key_press(self, widget, event):
        """Handle keyboard navigation"""
        keyval_name = Gdk.keyval_name(event.keyval)
        
        if keyval_name == 'Escape':
            self.hide()
            return True
        elif keyval_name == 'Return':
            selected_row = self.listbox.get_selected_row()
            if selected_row:
                self._on_row_activated(self.listbox, selected_row)
            return True
        elif keyval_name == 'Up':
            self._move_selection(-1)
            return True
        elif keyval_name == 'Down':
            self._move_selection(1)
            return True
            
        return False
        
    def _move_selection(self, direction):
        """Move selection up or down"""
        selected_row = self.listbox.get_selected_row()
        if not selected_row:
            # If nothing is selected, select the first row
            first_row = self.listbox.get_row_at_index(0)
            if first_row:
                self.listbox.select_row(first_row)
            return
            
        current_index = selected_row.get_index()
        next_index = current_index + direction
        next_row = self.listbox.get_row_at_index(next_index)
        
        if next_row:
            self.listbox.select_row(next_row)
            # Ensure the selected row is visible
            next_row.grab_focus()
        
    def _on_show(self, widget):
        """Refresh workspace list and focus current workspace"""
        # Clear existing items
        for child in self.listbox.get_children():
            self.listbox.remove(child)
            
        # Get current workspace
        current_ws = None
        for ws in self.workspace_manager.i3.get_workspaces():
            if ws.focused:
                current_ws = ws.name
                break
            
        current_row = None
        
        # Add workspaces
        for ws_name in self.workspace_manager.get_existing_workspaces():
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=ws_name, xalign=0)
            label.set_margin_start(6)
            label.set_margin_end(6)
            label.set_margin_top(3)
            label.set_margin_bottom(3)
            row.add(label)
            self.listbox.add(row)
            
            # Store reference to current workspace's row
            if ws_name == current_ws:
                current_row = row
        
        self.listbox.show_all()
        
        # Select and focus current workspace's row
        if current_row:
            self.listbox.select_row(current_row)
            current_row.grab_focus()
        
    def _on_row_activated(self, listbox, row):
        """Handle workspace selection"""
        label = row.get_child()
        self.workspace_manager.switch_to_workspace(label.get_text())
        self.hide() 