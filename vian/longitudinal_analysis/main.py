import collections

import numpy as np

from models import Dataset, Symbol


def example():
    dataset = Dataset()

    meta, data = dataset.at(0, xy=False)
    symbol = Symbol(meta, data)
    symbols = (
        symbol['count'].apply(np.log)
        ==
        symbol[['age', 'smoke']].interact(lambda x: x[0]*x[1], name='age_smoke') +
        symbol['age'] + symbol['smoke'] + symbol['drug'] + symbol['partners'] + symbol['cesd']
    )
    return symbols


def example_1_2_6():
    # 数据预处理
    meta, data= Dataset().at(4, xy=False)
    mapper = collections.Counter(data['id'])
    for id in mapper:
        index = data['id'] == id
        data.loc[index, 'weight'] = data.loc[index, 'weight'].mean()
    # 线性模型的符号表示
    symbol = Symbol(meta, data)
    symbols = (
        symbol['weight']
        ==
        symbol['gender'] + symbol['dose'] +
        symbol['id'].apply(lambda xs: [mapper[x] for x in xs], 'size')
    )
    return symbols


if __name__ == '__main__':
    symbols = example_1_2_6()
