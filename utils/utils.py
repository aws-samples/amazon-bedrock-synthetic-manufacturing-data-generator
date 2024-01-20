import os
import zipfile

FILE_BLACK_LIST = [".DS_Store", "__pycache__", ".venv"]


def zip_repo(src, dst):
    """ZIP the repository

    Args:
        src:              The source folder path
        dst:              The destination ZIP file name

    Returns:
        No return
    """
    zf = zipfile.ZipFile(f"{dst}.zip", "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            if filename in FILE_BLACK_LIST:
                continue
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1 :]
            zf.write(absname, arcname)
    zf.close()
