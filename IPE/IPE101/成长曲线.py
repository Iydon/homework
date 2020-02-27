import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


labels = {1: '小学', 2: '初中', 3: '高中', 4: '大一', 5: '大二', 6: '大三'}
factors = {
    '身高': [1.45, 1.65, 1.75, 1.77, 1.77, 1.77],
    '近视度数': [.0, 175., 250., 275., 275., 275.],
    '离家距离': [.0, .0, .03, 1., 1., 1.],
    '中二程度': [.5, 1.3, 1.5, 1.2, 1.0, 1.0],
    '独立思考能力': [.0, .0, .1, .3, .7, 1.],
    '独立生活能力': [.0, .0, .5, .9, .95, 1.],
    '知识储备量': [.05, .1, .15, .35, .85, 1.],
    '努力程度': [.0, .5, 1.2, 0.9, 0.65, 1.],
}
font_path = '/usr/share/fonts/wenquanyi/wqy-microhei/wqy-microhei.ttc'

x = list(labels.keys())
font = FontProperties(fname=font_path)
for factor, value in factors.items():
    value = list(value)
    plt.plot(x, [v/value[-1] for v in value])
plt.title('成长曲线图', fontproperties=font)
plt.xticks(x, labels.values(), fontproperties=font)
plt.ylabel('以当前时间点为基准进行评价', fontproperties=font)
plt.legend(factors.keys(), prop=font)
plt.show()
