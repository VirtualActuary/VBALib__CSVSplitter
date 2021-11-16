import tempfile
from pathlib import Path
from zebra_vba_packager import decompile_xl, is_locked, pack
import locate
import os

locate.allow_relative_location_imports(".")
from util import backup_last_50_files # noqa

# Filenames
files = [locate.this_dir().parent.joinpath("src.xlsb")]
dirs = [locate.this_dir().parent.joinpath("src")]

for d in dirs:
    if is_locked(d):
        raise ValueError(f"Dir '{d}' cannot be overwritten; make sure it's not open in another program.")

    # Backup the directory
    with tempfile.TemporaryDirectory() as outdir:
        if d.is_dir():
            pack(d, zipname := Path(outdir).joinpath(d.name+".7z"))
            backup_last_50_files(zipname)

for f,d in zip(files, dirs):
    # Decompile and remove zebra files)
    decompile_xl(f, d)

    for i in d.rglob("*"):
        if i.is_file() and i.name.startswith("z") and str(i)[-4:].lower() in [".txt", ".bas", ".cls"]:
            os.remove(i)
