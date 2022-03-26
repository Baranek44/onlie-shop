import os

def set_dll_search_path():
    # Python 3.8 no longer searches for DLLs in PATH, so we have to add
    # everything in PATH manually. Note that unlike PATH add_dll_directory
    # has no defined order, so if there are two cairo DLLs in PATH we
    # might get a random one.
    # no library called "cairo" was found
    # cannot load library 'C:\Program Files\GTK3-Runtime Win64\bin\libcairo-2.dll': error 0x7e
    # cannot load library 'libcairo.so.2': error 0x7e
    # cannot load library 'libcairo.2.dylib': error 0x7e
    # cannot load library 'libcairo-2.dll': error 0x7e
    if os.name != "nt" or not hasattr(os, "add_dll_directory"):
        return
    for p in os.environ.get("PATH", "").split(os.pathsep):
        try:
            os.add_dll_directory(p)
        except OSError:
            pass


set_dll_search_path()