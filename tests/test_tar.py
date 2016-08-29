# Copyright (C) 2015-2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

from sflock.abstracts import File
from sflock.unpack import Tarfile

def f(filename):
    return File.from_path("tests/files/%s" % filename)

class TestTarfile(object):
    def test_tar_plain(self):
        assert "POSIX tar" in f("tar_plain.tar").magic
        t = Tarfile(f("tar_plain.tar"))
        assert t.handles() is True
        files = list(t.unpack())
        assert len(files) == 1
        assert files[0]["file"].filepath == "sflock.txt"
        assert files[0]["file"].contents == "sflock_plain_tar\n"
        assert files[0]["file"].magic == "ASCII text"

        # TODO A combination of file extension, file magic, and initial bytes
        # signature should be used instead of just the bytes (as this call
        # should not yield None).
        assert f("tar_plain.tar").signature() is None

    def test_tar_plain2(self):
        assert "POSIX tar" in f("tar_plain2.tar").magic
        t = Tarfile(f("tar_plain2.tar"))
        assert t.handles() is True
        files = list(t.unpack())
        assert len(files) == 2
        assert files[0]["file"].filepath == "sflock.txt"
        assert files[0]["file"].contents == "sflock_plain_tar\n"
        assert files[0]["file"].magic == "ASCII text"
        assert files[1]["file"].filepath == "sflock2.txt"
        assert files[1]["file"].contents == "sflock_plain_tar2\n"
        assert files[1]["file"].magic == "ASCII text"

        # TODO See item above for tar_plain.tar.
        assert f("tar_plain2.tar").signature() is None

    def test_tar_plain2_gz(self):
        assert "gzip compr" in f("tar_plain2.tar.gz").magic
        t = Tarfile(f("tar_plain2.tar.gz"))
        assert t.handles() is True
        files = list(t.unpack())
        assert len(files) == 2
        assert files[0]["file"].filepath == "sflock.txt"
        assert files[0]["file"].contents == "sflock_plain_tar\n"
        assert files[0]["file"].magic == "ASCII text"
        assert files[1]["file"].filepath == "sflock2.txt"
        assert files[1]["file"].contents == "sflock_plain_tar2\n"
        assert files[1]["file"].magic == "ASCII text"

        s = f("tar_plain2.tar.gz").signature()
        assert s == {"family": "tar", "mode": "r:gz", "unpacker": "tarfile"}

    def test_tar_plain2_bz2(self):
        assert "bzip2 compr" in f("tar_plain2.tar.bz2").magic
        t = Tarfile(f("tar_plain2.tar.bz2"))
        assert t.handles() is True
        files = list(t.unpack())
        assert len(files) == 2
        assert files[0]["file"].filepath == "sflock.txt"
        assert files[0]["file"].contents == "sflock_plain_tar\n"
        assert files[0]["file"].magic == "ASCII text"
        assert files[1]["file"].filepath == "sflock2.txt"
        assert files[1]["file"].contents == "sflock_plain_tar2\n"
        assert files[1]["file"].magic == "ASCII text"

        s = f("tar_plain2.tar.bz2").signature()
        assert s == {"family": "tar", "mode": "r:bz2", "unpacker": "tarfile"}
