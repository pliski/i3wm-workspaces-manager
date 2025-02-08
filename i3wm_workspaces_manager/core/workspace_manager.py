import i3ipc

class WorkspaceManager:
    def __init__(self):
        self.i3 = i3ipc.Connection()

    def get_next_available_number(self):
        """Find the lowest available workspace number."""
        workspaces = self.i3.get_workspaces()
        used_numbers = set()
        
        for workspace in workspaces:
            try:
                num = int(workspace.name)
                used_numbers.add(num)
            except ValueError:
                # Workspace name is not a number, skip it
                continue
        
        # Find the first number that's not in use
        next_num = 1
        while next_num in used_numbers:
            next_num += 1
        
        return next_num

    def create_workspace(self, name):
        """Create a new workspace with the given name."""
        self.i3.command(f"workspace {name}")

    def rename_current_workspace(self, new_name):
        """Rename the current workspace."""
        self.i3.command(f"rename workspace to {new_name}")

    def get_existing_workspaces(self):
        """Get a list of existing workspace names."""
        return [ws.name for ws in self.i3.get_workspaces()]

    def switch_to_workspace(self, name):
        """Switch to a specific workspace."""
        self.i3.command(f"workspace {name}")

    def validate_workspace_name(self, name):
        """
        Validate workspace name against i3wm constraints.
        Returns (bool, str) tuple: (is_valid, error_message)
        """
        if not name:
            return False, "Workspace name cannot be empty"
        
        # Add more validation rules as needed
        return True, ""

    def move_window_to_workspace(self, window_id, workspace_name):
        """Move a window to a specific workspace."""
        command = f'[con_id="{window_id}"] move container to workspace {workspace_name}'
        self.i3.command(command) 