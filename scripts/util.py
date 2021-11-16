import os
import shutil
import tempfile
from pathlib import Path
from zebra_vba_packager import Source
import time

lib_source = Source(
    url_source="https://github.com/VirtualActuary/VBALib/releases/download/0.1.1/VBALib.zip",
    url_md5="0a3ae372b8b6c3ee16e2c592c334a200",
    glob_include="**/*",
    auto_cls_rename=False,
    auto_bas_namespace=False,
)


def backup_last_50_files(fname):

    backup = Path(tempfile.gettempdir()).joinpath("niac-test-case-generator-backups")
    os.makedirs(backup, exist_ok=True)

    keep = sorted(backup.glob("*"))[-50:]
    for i in backup.glob("*"):
        if i not in keep:
            os.remove(i)

    timestr = time.strftime("%Y-%m-%d--%H-%M-%S")
    try:
        shutil.copy2(fname, backup.joinpath(f"{timestr}--{Path(fname).name}"))
    except:
        pass