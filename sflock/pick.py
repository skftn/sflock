# Copyright (C) 2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

def picker(filename):
    """Guesses the unpacker for this file based on its filename extension."""
    if not filename:
        return

    filename = filename.lower()

    if filename.endswith(".tar"):
        return "tarfile"

    if filename.endswith(".tar.gz"):
        return "targzfile"

    if filename.endswith(".tar.bz2"):
        return "tarbz2file"

    if filename.endswith(".zip"):
        return "zipfile"

    if filename.endswith(".rar"):
        return "rarfile"

    if filename.endswith(".7z"):
        return "7zfile"

    if filename.endswith(".ace"):
        return "acefile"

    if filename.endswith(".eml"):
        return "emlfile"

    if filename.endswith(".msg"):
        return "msgfile"

    if filename.endswith(".mso"):
        return "msofile"
