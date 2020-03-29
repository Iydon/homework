import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np


zh_font = FontProperties(fname='/usr/share/fonts/wenquanyi/wqy-microhei/wqy-microhei.ttc')

xticks = ('震惊 (31)', '内幕 (11)', '锤 (50)', '抑郁 (15)', '盗 (95)', '赞 (67)')
x = tuple(range(len(xticks)))
y_orm = np.array((0.06143573300141725, 0.06093079700076487, 0.05296121200080961, 0.05191942199962796, 0.06305324099957943, 0.062044757996773114))
y_sql = np.array((0.025273589002608787, 0.030472476002614712, 0.02612491799663985, 0.02173666300222976, 0.022270457997365156, 0.01979598100297153))
y_ram = np.array((0.01080189799904474, 0.0133085259985819, 0.012458743000024697, 0.012985498000489315, 0.013328812001418555, 0.015257447001204127))
t_json = 0.974
t_csv = 0.0136

plt.semilogy(x, y_orm)
plt.semilogy(x, y_sql)
plt.semilogy(x, y_ram)
plt.semilogy(x, y_ram+t_json)
plt.semilogy(x, y_ram+t_csv)

plt.title('DBMS vs RAM (select * from Video as v where v.title like ...)')
plt.legend(('ORM', 'SQL', 'Only RAM', 'Json to RAM', 'CSV to RAM'))
plt.xticks(x, xticks, fontproperties=zh_font)
plt.xlabel('Keywords (times)')
plt.ylabel('Time (seconds)')
plt.savefig(__file__.replace('.py', '.png'))
