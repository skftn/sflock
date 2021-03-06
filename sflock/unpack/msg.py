# Copyright (C) 2016 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import io
import olefile
import os.path

from sflock.abstracts import Unpacker, File
from sflock.exception import UnpackException
from sflock.pick import picker

class MsgFile(Unpacker):
    name = "msgfile"
    exts = ".msg"

    def supported(self):
        return True

    def handles(self):
        return picker(self.f.filepath) == self.name

    def get_stream(self, *filename):
        if self.ole.exists(os.path.join(*filename)):
            return self.ole.openstream(os.path.join(*filename)).read()

    def get_string(self, *filename):
        ascii_filename = "%s001E" % "/".join(filename)
        unicode_filename = "%s001F" % "/".join(filename)

        return (
            self.get_stream(unicode_filename).decode("utf16") or
            self.get_stream(ascii_filename)
        )

    def get_attachment(self, dirname):
        filename = (
            self.get_string(dirname, "__substg1.0_3707") or
            self.get_string(dirname, "__substg1.0_3704") or
            "att1"
        )
        contents = self.get_stream(dirname, "__substg1.0_37010102")
        return filename, contents

    def unpack(self, password=None, duplicates=None):
        seen, entries = [], []

        try:
            self.ole = olefile.OleFileIO(io.BytesIO(self.f.contents))
        except IOError as e:
            raise UnpackException(e)

        for dirname in self.ole.listdir():
            if dirname[0].startswith("__attach") and dirname[0] not in seen:
                filename, contents = self.get_attachment(dirname[0])
                entries.append(File(filename, contents))
                seen.append(dirname[0])

        return self.process(entries, duplicates)
