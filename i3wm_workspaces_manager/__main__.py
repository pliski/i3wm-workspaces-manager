import sys

from .core.app import I3WorkspacesManager


def main():
    app = I3WorkspacesManager()
    try:
        app.run()
    except KeyboardInterrupt:
        sys.exit(130)  # 128 + SIGINT


if __name__ == '__main__':
    main() 