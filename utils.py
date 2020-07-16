import sys


def project_root():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return '.'


PROJECT_ROOT = project_root()
