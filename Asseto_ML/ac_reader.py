import mmap
import ctypes
from ac_structs import SPageFilePhysics, SPageFileGraphics, SPageFileStatic

class ACReader:
    def __init__(self):
        self.mm_phy = None
        self.mm_gfx = None
        self.mm_stc = None

    def connect(self):
        try:
            self.mm_phy = mmap.mmap(0, ctypes.sizeof(SPageFilePhysics), "acpmf_physics", access=mmap.ACCESS_READ)
            self.mm_gfx = mmap.mmap(0, ctypes.sizeof(SPageFileGraphics), "acpmf_graphics", access=mmap.ACCESS_READ)
            self.mm_stc = mmap.mmap(0, ctypes.sizeof(SPageFileStatic), "acpmf_static", access=mmap.ACCESS_READ)
            return True
        except:
            return False

    def read_all(self):
        def _read(mm, struct_type):
            mm.seek(0)
            obj = struct_type()
            ctypes.memmove(ctypes.addressof(obj), mm.read(ctypes.sizeof(struct_type)), ctypes.sizeof(struct_type))
            return obj
        
        return _read(self.mm_phy, SPageFilePhysics), \
               _read(self.mm_gfx, SPageFileGraphics), \
               _read(self.mm_stc, SPageFileStatic)