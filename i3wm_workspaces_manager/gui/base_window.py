import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class BaseWindow(Gtk.Window):
    def __init__(self, title):
        super().__init__(title=title)
        
        # Set up window properties
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_keep_above(True)
        self.set_skip_taskbar_hint(True)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        
        # Connect key events
        self.connect('key-press-event', self._on_key_press)
        # Connect focus out event
        self.connect('focus-out-event', self._on_focus_out)
        
    def _on_key_press(self, widget, event):
        """Handle key press events"""
        keyval = event.keyval
        keyval_name = Gdk.keyval_name(keyval)
        
        if keyval_name == 'Escape':
            self.hide()
            return True
            
        return False
        
    def _on_focus_out(self, widget, event):
        """Hide window when it loses focus"""
        self.hide()
        return False 