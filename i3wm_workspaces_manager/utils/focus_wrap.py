#!/usr/bin/env python3

from i3ipc import Connection, Event
import sys

def get_windows_on_output(tree, output_name):
    """Get all windows on a specific output."""
    windows = []
    current_window = None
    
    def collect_windows(container):
        nonlocal current_window
        
        # Check if this is a window container
        if (container.window and 
            container.type == 'con' and 
            container.parent and 
            container.parent.type != 'dockarea'):
            
            # Find the output for this container
            node = container
            while node and node.type != 'output':
                node = node.parent
                
            # If this window is on the desired output, add it
            if node and node.name == output_name:
                windows.append(container)
                if container.focused:
                    current_window = container
        
        # Recursively check children
        for child in container.nodes:
            collect_windows(child)
        # Check floating containers too
        for child in container.floating_nodes:
            collect_windows(child)
    
    # Start traversal from the root
    collect_windows(tree)
    
    return windows, current_window

def find_current_output(tree):
    """Find the output containing the focused window."""
    focused = tree.find_focused()
    if not focused:
        return None
    
    # Find the output containing the focused window
    node = focused
    while node and node.type != 'output':
        node = node.parent
    
    return node

def order_windows(windows):
    """Order windows by their x position."""
    return sorted(windows, key=lambda x: (x.rect.x, x.rect.y))

def main(direction):
    i3 = Connection()
    tree = i3.get_tree()
    
    # Find the current output
    output = find_current_output(tree)
    if not output:
        print("No active output found")
        return
    
    # Get windows on the current output
    windows, current_window = get_windows_on_output(tree, output.name)
    
    if not windows:
        print(f"No windows found on output {output.name}")
        return
    
    if not current_window:
        print("No focused window found")
        return
    
    # Order windows by position
    ordered = order_windows(windows)
    
    try:
        index = ordered.index(current_window)
    except ValueError:
        print("Current window not found in ordered list")
        return
    
    # Determine the next window to focus
    if direction == 'right':
        new_index = (index + 1) % len(ordered)
    elif direction == 'left':
        new_index = (index - 1) % len(ordered)
    else:
        print(f"Invalid direction: {direction}")
        return
    
    # Focus the new window
    ordered[new_index].command('focus')

def cli():
    if len(sys.argv) < 2:
        print("Usage: i3wm-focus-wrap [left|right]")
        sys.exit(1)
    main(sys.argv[1])

if __name__ == "__main__":
    cli()