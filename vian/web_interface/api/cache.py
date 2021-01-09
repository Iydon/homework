import os
import pathlib


class Cache:
    def __init__(self, cache_dir):
        self._cache_dir = pathlib.Path(cache_dir)

    def getsize(self):
        '''Return the total size of cache directory

        Returen:
            - byte
        '''
        return sum(
            path.stat().st_size for path in self._iter()
        )

    def clear_zip_tsv(self):
        '''Clear zip and tsv cache
        '''
        try:
            for path in self._iter():
                path.suffix in ('.zip', '.tsv') and path.unlink()
            return True
        except:
            return False

    def _iter(self):
        for dirname, _, filenames in os.walk(self._cache_dir):
            dirname = pathlib.Path(dirname)
            for filename in filenames:
                path = dirname / filename
                path.is_file() and (yield path)
