# -*- encode: utf-8 -*-
import time


class Timer:
    def __enter__(self):
        self.TIC_TOC = time.time()
        return self

    def __exit__(self, type, value, traceback):
        self.TIC_TOC = time.time() - self.TIC_TOC

    def toc(self):
        return self.TIC_TOC
