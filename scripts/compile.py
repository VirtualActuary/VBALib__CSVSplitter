from pathlib import Path
from zebra_vba_packager import Config, Source, compile_xl, is_locked, runmacro_xl, decompile_xl
import locate
import tempfile
from distutils.dir_util import copy_tree

locate.allow_relative_location_imports(".")
from util import backup_last_50_files, lib_source # noqa

# Filenames
files = [locate.this_dir().parent.joinpath("src.xlsb")]
dirs = [locate.this_dir().parent.joinpath("src")]


for i in files:
    if is_locked(i):
        raise ValueError(f"File '{i}' cannot be overwritten.")
    backup_last_50_files(i)


for f, d in zip(files, dirs):
    with tempfile.TemporaryDirectory() as outdir:
        copy_tree(str(d), str(outdir))
        Config(lib_source).run(Path(outdir).joinpath("_"))
        compile_xl(outdir, f)

    runmacro_xl(f)
