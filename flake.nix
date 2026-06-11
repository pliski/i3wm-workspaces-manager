{
  description = "A GTK-based workspace manager for i3wm";

  inputs = {
    # Resolves via the local flake registry, so it reuses the system's
    # nixpkgs (no download). Override with --override-input if desired.
    nixpkgs.url = "nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python3;

        i3wm-workspaces-manager = python.pkgs.buildPythonApplication {
          pname = "i3wm-workspaces-manager";
          version = "0.1.0";
          pyproject = true;

          src = ./.;

          build-system = [ python.pkgs.poetry-core ];

          # GUI tests need a running i3/GTK display, so skip them at build time.
          doCheck = false;

          nativeBuildInputs = [
            pkgs.wrapGAppsHook3
            pkgs.gobject-introspection
          ];

          buildInputs = [
            pkgs.gtk3
          ];

          dependencies = with python.pkgs; [
            pygobject3
            i3ipc
          ];

          meta = with pkgs.lib; {
            description = "A GTK-based workspace manager for i3wm";
            license = licenses.mit;
            mainProgram = "i3wm-workspaces-manager";
          };
        };
      in
      {
        packages.default = i3wm-workspaces-manager;
        packages.i3wm-workspaces-manager = i3wm-workspaces-manager;

        apps.default = {
          type = "app";
          program = "${i3wm-workspaces-manager}/bin/i3wm-workspaces-manager";
        };

        devShells.default = pkgs.mkShell {
          inputsFrom = [ i3wm-workspaces-manager ];
          packages = [
            pkgs.poetry
            python.pkgs.pytest
          ];
        };
      });
}
