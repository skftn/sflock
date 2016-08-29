# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import File
from sflock.unpack import Zipfile

def f(filename):
    return File.from_path("tests/files/%s" % filename)

class TestZipfile(object):
    def test_zip_plain(self):
        assert "Zip archive" in f("zip_plain.zip").magic
        z = Zipfile(f("zip_plain.zip"))
        assert z.handles() is True
        files = list(z.unpack())
        assert len(files) == 1
        assert files[0]["file"].filepath == "sflock.txt"
        assert files[0]["file"].contents == "sflock_plain_zip\n"
        assert files[0]["file"].password is None
        assert files[0]["file"].magic == "ASCII text"

        s = f("zip_plain.zip").signature()
        assert s == {"family": "zip", "mode": "", "unpacker": "zipfile"}

    def test_zip_encrypted(self):
        assert "Zip archive" in f("zip_encrypted.zip").magic
        z = Zipfile(f("zip_encrypted.zip"))
        assert z.handles() is True
        files = list(z.unpack())
        assert len(files) == 1
        assert files[0]["file"].filepath == "sflock.txt"
        assert files[0]["file"].contents == "sflock_encrypted_zip\n"
        assert files[0]["file"].password == "infected"
        assert files[0]["file"].magic == "ASCII text"

        s = f("zip_encrypted.zip").signature()
        assert s == {"family": "zip", "mode": "", "unpacker": "zipfile"}

    def test_zip_encrypted2(self):
        assert "Zip archive" in f("zip_encrypted2.zip").magic
        z = Zipfile(f("zip_encrypted2.zip"))
        assert z.handles() is True
        files = list(z.unpack())
        assert len(files) == 1
        assert files[0]["file"].mode == "failed"
        assert files[0]["file"].description == "Error decrypting file"
        assert files[0]["file"].magic is None

        z = Zipfile(f("zip_encrypted2.zip"))
        assert z.handles() is True
        files = list(z.unpack(password="sflock"))
        assert len(files) == 1
        assert files[0]["file"].filepath == "sflock.txt"
        assert files[0]["file"].contents == "sflock_encrypted_zip\n"
        assert files[0]["file"].password == "sflock"
        assert files[0]["file"].magic == "ASCII text"

        s = f("zip_encrypted2.zip").signature()
        assert s == {"family": "zip", "mode": "", "unpacker": "zipfile"}
