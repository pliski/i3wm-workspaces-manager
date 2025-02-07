import pytest
from gi.repository import Gdk
from unittest.mock import patch, MagicMock
from i3wm_workspaces_manager.gui.workspace_creator_window import WorkspaceCreatorWindow
from i3wm_workspaces_manager.gui.workspace_switcher_window import WorkspaceSwitcherWindow

class TestWorkspaceCreatorWindow:
    @pytest.fixture
    def window(self, mock_i3):
        with patch('i3ipc.Connection', return_value=mock_i3):
            return WorkspaceCreatorWindow()
        
    @pytest.mark.i3required(reason="This test is not working because of the way i3ipc is mocked")
    def test_initial_state(self, window):
        assert not window.rename_check.get_active()

    @pytest.mark.i3required(reason="This test is not working because of the way i3ipc is mocked")
    def test_escape_key(self, window):
        event = MagicMock()
        event.keyval = Gdk.KEY_Escape
        with patch('gi.repository.Gdk.keyval_name', return_value='Escape'):
            assert window._on_key_press(None, event)
        
    @pytest.mark.i3required(reason="This test is not working because of the way i3ipc is mocked")
    def test_enter_key(self, window):
        event = MagicMock()
        event.keyval = Gdk.KEY_Return
        with patch('gi.repository.Gdk.keyval_name', return_value='Return'):
            with patch.object(window, '_on_activate') as mock_activate:
                assert window._on_key_press(None, event)
                mock_activate.assert_called_once_with(None)

class TestWorkspaceSwitcherWindow:
    @pytest.fixture
    def window(self, mock_i3):
        with patch('i3ipc.Connection', return_value=mock_i3):
            return WorkspaceSwitcherWindow()

    @pytest.mark.i3required(reason="This test is not working because of the way i3ipc is mocked")
    def test_navigation_keys(self, window):
        # Test Up key
        up_event = MagicMock()
        up_event.keyval = Gdk.KEY_Up
        with patch('gi.repository.Gdk.keyval_name', return_value='Up'):
            with patch.object(window, '_move_selection') as mock_move:
                assert window._on_key_press(None, up_event)
                mock_move.assert_called_once_with(-1)
            
        # Test Down key
        down_event = MagicMock()
        down_event.keyval = Gdk.KEY_Down
        with patch('gi.repository.Gdk.keyval_name', return_value='Down'):
            with patch.object(window, '_move_selection') as mock_move:
                assert window._on_key_press(None, down_event)
                mock_move.assert_called_once_with(1) 