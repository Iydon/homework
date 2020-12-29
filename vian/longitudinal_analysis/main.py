import json
import hashlib
import pathlib

import pandas as pd


class Dataset:
    def __init__(self, dirname='data', metaname='meta.json', encoding='utf-8'):
        self._dir = pathlib.Path(dirname)
        self._meta = json.loads((self._dir/metaname).read_text(encoding=encoding))

    def at(self, ith, xy=False):
        '''
        Return:
            {group: (x, y)} if xy else (meta, data)
        '''
        meta = self._meta[ith]
        content = (self._dir/meta['filename']).read_bytes()
        if hashlib.md5(content).hexdigest() != meta['filename']:
            raise Exception('MD5CheckFailed')
        data = getattr(pd, 'read_'+meta['format'])(content, **meta['kwargs'])
        if xy:
            if not meta['xyz']:
                raise NotImplementedError
            data = {
                id: (
                    group[meta['xyz']['x']].to_numpy(dtype='float64'),
                    group[meta['xyz']['y']].to_numpy(dtype='float64')
                )
                for id, group in data.groupby(meta['xyz']['z'])
            }
        return {key: meta[key] for key in ('description', 'header', 'xyz')}, data

    def filter(self, xy=False, **kwargs):
        for ith, meta in enumerate(self._meta):
            if len(kwargs) == sum(
                key in meta['attribute'] and meta['attribute'][key]==val
                for key, val in kwargs.items()
            ):
                yield self.at(ith, xy)

    def __getitem__(self, ith):
        return self.at(ith)

    def __iter__(self):
        for ith in range(len(self)):
            yield self.at(ith)

    def __len__(self):
        return len(self._meta)

    def __repr__(self):
        return f'<Dataset({len(self)}) @ {hash(self):#x}>'


if __name__ == '__main__':
    import os

    dataset = Dataset()
    for meta, data in dataset:
        print('=' * 64)
        length = max(map(len, data.columns))
        for column in data.columns:
            print(f'{column:{length}}:', meta['header'][column])
