import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from .base_window import BaseWindow
from ..core.workspace_manager import WorkspaceManager

class WorkspaceSwitcherWindow(BaseWindow):
    def __init__(self):
        super().__init__(title="i3wm Workspace Switcher")
        self.workspace_manager = WorkspaceManager()
        self.previously_focused_window = None
        
        # Create main vertical box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(main_box)
        
        # Create workspace listbox
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(200)
        # Prevent ScrolledWindow from capturing focus
        scrolled.set_can_focus(False)
        main_box.pack_start(scrolled, True, True, 0)
        
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.listbox.set_can_focus(True)
        scrolled.add(self.listbox)
        
        # Add move to workspace button
        self.move_button = Gtk.Button(label="Move Window to Workspace")
        self.move_button.connect('clicked', self._on_move_to_workspace_activated)
        main_box.pack_start(self.move_button, False, False, 0)
        
        # Add CSS styling
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            .focused-list:focus {
                border-color: #215d9c;
            }
            .focused-list:focus row:selected {
                background-color: white;
                color: black;
            }
            .focused-button:focus {
                background-color: #215d9c;
                color: white;
            }
        """)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        # Add style classes
        self.listbox.get_style_context().add_class('focused-list')
        self.move_button.get_style_context().add_class('focused-button')
        
        # Connect signals
        self.listbox.connect('row-activated', self._on_row_activated)
        self.connect('show', self._on_show)
        self.connect('hide', self._on_hide)
        
    def _on_show(self, widget):
        """Populate workspace list and store focused window when window is shown"""
        tree = self.workspace_manager.i3.get_tree()
        self.previously_focused_window = tree.find_focused()
        
        self._populate_workspace_list()
        # Ensure initial focus and selection
        self.listbox.grab_focus()
        first_row = self.listbox.get_row_at_index(0)
        if first_row:
            self.listbox.select_row(first_row)
        
    def _on_hide(self, widget):
        """Reset state when window is hidden"""
        self.previously_focused_window = None
        self.listbox.unselect_all()
        
    def _populate_workspace_list(self):
        """Populate the workspace listbox"""
        # Clear existing items
        for row in self.listbox.get_children():
            self.listbox.remove(row)
            
        # Add workspace items
        for workspace in self.workspace_manager.get_existing_workspaces():
            label = Gtk.Label(label=workspace, xalign=0)
            label.set_margin_start(6)
            label.set_margin_end(6)
            label.set_margin_top(3)
            label.set_margin_bottom(3)
            self.listbox.add(label)
            
        self.listbox.show_all()
        
    def _on_move_to_workspace_activated(self, button):
        """Move previously focused window to selected workspace"""
        if not self.previously_focused_window:
            return
            
        selected_row = self.listbox.get_selected_row()
        if not selected_row:
            return
            
        workspace_label = selected_row.get_child()
        target_workspace = workspace_label.get_text()
        
        # Move the window to the selected workspace
        self.workspace_manager.move_window_to_workspace(
            self.previously_focused_window.id,
            target_workspace
        )
        self.hide()
        
    def _on_key_press(self, widget, event):
        """Handle keyboard navigation"""
        keyval_name = Gdk.keyval_name(event.keyval)
        
        if keyval_name == 'Escape':
            self.hide()
            return True
        elif keyval_name == 'Return':
            focused_widget = self.get_focus()
            if focused_widget == self.move_button:
                self._on_move_to_workspace_activated(self.move_button)
            elif focused_widget == self.listbox:
                selected_row = self.listbox.get_selected_row()
                if selected_row:
                    self._on_row_activated(self.listbox, selected_row)
            return True
        elif keyval_name in ['Up', 'Down']:
            focused_widget = self.get_focus()
            if focused_widget == self.listbox:
                self._move_selection(1 if keyval_name == 'Down' else -1)
                # Ensure listbox keeps focus after selection
                self.listbox.grab_focus()
            return True
        elif keyval_name == 'Tab':
            # Direct focus switching between listbox and button
            if self.get_focus() == self.listbox:
                self.move_button.grab_focus()
            else:
                self.listbox.grab_focus()
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
            # Make sure the selected row is visible
            next_row.get_parent().get_parent().get_vadjustment().set_value(
                next_index * next_row.get_allocated_height()
            )
        
    def _on_row_activated(self, listbox, row):
        """Handle workspace selection"""
        label = row.get_child()
        self.workspace_manager.switch_to_workspace(label.get_text())
        self.hide() 