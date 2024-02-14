import os
import sys

def path(archive: str):
    if getattr(sys, 'frozen', False):
        return os.path.normpath(os.path.join(sys._MEIPASS, 'assets', archive))
    else:
        return os.path.normpath(os.path.join('assets', archive))