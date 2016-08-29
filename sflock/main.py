# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import click
import glob
import os.path

def analyize_file(filepath, contents=None, normalize_containers=False):
    from sflock.abstracts import File
    from sflock.unpack import plugins

    f = File(filepath=filepath, contents=contents)
    signature = f.signature()

    if signature:
        container = plugins[signature["unpacker"]](f)

        if normalize_containers:
            pass

        return container.unpack(mode=signature["mode"])
    else:
        return f

def process_directory(dirpath):
    for rootpath, directories, filenames in os.walk(dirpath):
        for filename in filenames:
            analyize_file(os.path.join(rootpath, filename))

@click.command()
@click.argument("files", nargs=-1)
def main(files):
    for pattern in files:
        for path in glob.iglob(pattern):
            if os.path.isdir(path):
                process_directory(path)
            else:
                analyize_file(filepath=path)


# if filename.endswith((".zip", ".gz", ".tar", ".tar.gz", ".bz2", ".tgz")):
#     f = File(filepath=filename, contents=data)
#     signature = f.get_signature()
#
#     container = None
#     if signature["family"] == "rar":
#         container = Rarfile
#     elif signature["family"] == "zip":
#         container = Zipfile
#     elif signature["family"] == "tar":
#         container = Tarfile
#     else:
#         return f
#
#     container = container(f=f)
#     f.children = container.unpack(mode=signature["mode"],
#                                   duplicates=duplicates)
#     return f
#
# return File(filepath=filename, contents=data)