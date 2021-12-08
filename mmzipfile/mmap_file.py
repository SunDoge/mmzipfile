from mmap import mmap

class MmapFile(mmap):

    def seekable(self):
        return True

    
    