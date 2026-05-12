.PHONY: install uninstall

PACKAGE_NAME := i3wm-workspaces-manager

install:
	pipx install --force --system-site-packages .

uninstall:
	pipx uninstall $(PACKAGE_NAME)
