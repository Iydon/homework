#!/usr/bin/python3
from collections import defaultdict
import requests

import jieba
from wordcloud import WordCloud, STOPWORDS


# stopwords_url = 'https://raw.githubusercontent.com/goto456/stopwords/master/中文停用词表.txt'
stopwords_file = 'stopwords.txt'
data_files = ('现代性.txt', '工具理性.txt')
target_files = ('现代性.png', '工具理性.png')
font_file = '/usr/share/fonts/wenquanyi/wqy-zenhei/wqy-zenhei.ttc'
size = {'width': 1024, 'height': 512}


_locals = locals()
stopwords = STOPWORDS
if 'stopwords_url' in _locals:
    stopwords = stopwords.union(
        set(requests.get(_locals['stopwords_url']).text.splitlines()))
elif 'stopwords_file' in _locals:
    with open(_locals['stopwords_file'], 'r') as f:
        stopwords = stopwords.union(set(f.read().splitlines()))

for data_file, target_file in zip(data_files, target_files):
    wc = WordCloud(font_path=font_file, background_color='white', **size)
    with open(data_file, 'r') as f:
        frequencies = defaultdict(int)
        for line in f.readlines():
            for word in jieba.cut(line.strip()):
                if word not in stopwords:
                    frequencies[word] += 1
    wordcloud = wc.generate_from_frequencies(frequencies)
    wordcloud.to_file(target_file)
