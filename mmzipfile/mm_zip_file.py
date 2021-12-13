from typing import List
from zipfile import ZipFile, ZipInfo
from .mmap_file import MmapFile


class MmZipFile:

    def __init__(
        self,
        filename: str
    ) -> None:
        fp = open(filename, 'r+b')
        mm_file = MmapFile(fp.fileno(), 0)
        zip_file = ZipFile(mm_file, mode='r')  # type: ignore

        self.fp = fp
        self.mm_file = mm_file
        self.zip_file = zip_file

    def open(self, name, **kwargs):
        return self.zip_file.open(name, **kwargs)

    def read(self, name, **kwargs):
        return self.zip_file.read(name, **kwargs)

    def namelist(self) -> List[str]:
        return self.zip_file.namelist()

    @property
    def filelist(self) -> List[ZipInfo]:
        return self.zip_file.filelist

    def close(self):
        self.zip_file.close()


class MmZipFileCollection:

    def __init__(
        self,
        filenames: list
    ) -> None:
        mm_zip_files = [MmZipFile(filename) for filename in filenames]

        index_map = {}

        for index, mm_zip_file in enumerate(mm_zip_files):
            names = mm_zip_file.namelist()
            for name in names:
                index_map[name] = index

        self.mm_zip_files = mm_zip_files
        self.index_map = index_map

    def open(self, name: str, **kwargs):
        index = self.index_map[name]
        return self.mm_zip_files[index].open(name, **kwargs)

    def read(self, name, **kwargs):
        index = self.index_map[name]
        return self.mm_zip_files[index].read(name, **kwargs)

    def namelist(self) -> List[str]:
        return list(self.index_map.keys())

    @property
    def filelist(self) -> List[ZipInfo]:
        return sum(f.filelist for f in self.mm_zip_files)

    def close(self):
        for mm_zip_file in self.mm_zip_files:
            mm_zip_file.close()
