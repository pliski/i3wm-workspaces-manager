import pytest
from unittest.mock import patch, MagicMock
from gi.repository import GLib
from i3wm_workspaces_manager.core.app import I3WorkspacesManager

def test_binding_events(mock_i3):
    with patch('i3ipc.Connection', return_value=mock_i3):
        app = I3WorkspacesManager()
        
        # Test workspace creator binding
        event = MagicMock()
        event.binding.command = 'nop workspace_creator'
        
        with patch('gi.repository.GLib.idle_add') as mock_idle_add:
            app._on_binding_event(None, event)
            mock_idle_add.assert_called_once_with(app._show_creator_window)
            
        # Test workspace switcher binding
        event.binding.command = 'nop workspace_switcher'
        with patch('gi.repository.GLib.idle_add') as mock_idle_add:
            app._on_binding_event(None, event)
            mock_idle_add.assert_called_once_with(app._show_switcher_window) 