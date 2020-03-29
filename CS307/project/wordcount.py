#!/usr/bin/python3
import fire
import logging
import os
import re


def word_count(path='.', punc='', ext=(), enc='utf-8', echo=False):
    '''Count chinese words.

    Argument:
        - path: str, project path, default is current directory
        - punc: str, chinese punctuations pattern
        - ext: list, extensions that read
        - enc: str, encoding, default is 'utf-8'
        - echo: bool, whether to display matching results
    '''
    chinese = '\u4e00-\u9fa5' + (punc or '，？！：；·「」“”‘’、（）×…')
    chinese_pattern = re.compile(f'[{chinese}]+')
    extension = ext or ('.tex', )
    count = 0
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            if os.path.splitext(filename)[-1] in extension:
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding=enc) as f:
                        group = chinese_pattern.findall(f.read())
                        if echo and group: print(f'{filepath}: {group}')
                        count += sum(map(len, group))
                except (UnicodeDecodeError, FileNotFoundError):
                    logging.error(f'BinaryOrRemovedFile:{filepath}')
    return count


if __name__ == '__main__':
    fire.Fire(word_count)
