import textwrap

from models import Dataset


dataset = Dataset()
attribute_mapper = {
    'balance': '平衡数据',
    'response_type': '响应变量的数据类型',
}
xyz_mapper = {
    't': '时间变量',
    'x': '协变量',
    'y': '响应变量',
    'z': '区分个体变量',
}

for meta, data in dataset:
    if len(data.columns) > 8:
        continue
    print('\\subsubsection{{{}}}'.format(meta['title']))
    print(meta['description'] + '\n')

    print('\\begin{itemize}')

    print('    \\item 表头说明：')
    print('        \\begin{enumerate*}[label=(\\alph*), itemjoin={；}]')
    for x, y in meta['header'].items():
        x = x.replace('_', '\_')
        print(f'            \\item {x}，{y}')
    print('        \\end{enumerate*}。' + '\n')

    print('    \\item 表头类型：')
    print('        \\begin{enumerate*}[label=(\\alph*), itemjoin={；}]')
    for x, y in meta['xyz'].items():
        if isinstance(y, list):
            y = '、'.join(map(lambda x: x.replace('_', '\\_'), y))
        else:
            y = str(y).replace('_', '\\_')
        print(f'            \\item {xyz_mapper[x]}，{y}')
    print('        \\end{enumerate*}。' + '\n')

    print('    \\item 属性说明：')
    print('        \\begin{enumerate*}[label=(\\alph*), itemjoin={；}]')
    for x, y in meta['attribute'].items():
        x = attribute_mapper[x].replace('_', '\_')
        print(f'            \\item {x}，{y}')
    print('        \\end{enumerate*}。')

    print('\\end{itemize}' + '\n')

    print('\\begin{table}[H]')
    print('    \\centering')
    print(textwrap.indent(
        data.describe().round(2).to_latex(), '    '
    ).rstrip())
    print('    \\caption{{{0}的描述性统计}}\\label{{T:dataset-{0}}}'.format(meta['title']))
    print('\\end{table}' + '\n' + '\n')
