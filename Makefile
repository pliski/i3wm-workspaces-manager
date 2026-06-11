.PHONY: install uninstall

PACKAGE_NAME := i3wm-workspaces-manager

# On NixOS, PyGObject/GTK can't be built or reused via pipx, so install the
# Nix flake into the user profile instead. Everywhere else, use pipx.
install:
	@if command -v nixos-version >/dev/null 2>&1; then \
		echo "NixOS detected: installing via Nix flake"; \
		nix profile remove $(PACKAGE_NAME) >/dev/null 2>&1 || true; \
		nix profile install .; \
	else \
		pipx install --force --system-site-packages .; \
	fi

uninstall:
	@if command -v nixos-version >/dev/null 2>&1; then \
		nix profile remove $(PACKAGE_NAME); \
	else \
		pipx uninstall $(PACKAGE_NAME); \
	fi
