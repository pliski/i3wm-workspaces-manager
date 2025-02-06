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
        
    def _on_key_press(self, widget, event):
        """Handle key press events"""
        keyval = event.keyval
        keyval_name = Gdk.keyval_name(keyval)
        
        if keyval_name == 'Escape':
            self.hide()
            return True
            
        return False 