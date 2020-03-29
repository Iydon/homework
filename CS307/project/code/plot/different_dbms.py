import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np


zh_font = FontProperties(fname='/usr/share/fonts/wenquanyi/wqy-microhei/wqy-microhei.ttc')

xticks = ('检索小数据集', '检索大数据集', '使用关联对象', '聚合函数', '分组')
x = tuple(range(len(xticks)))
postgresql = (0.044339208999872426, 15.918189195999958, 4.733379002999982, 14.992970761999914, 0.0318434159999014)
mysql = (0.1703436640000291, 113.09160094000072, 9.877226518000498, 33.828511658000025, 0.14873496900054306)
sqlite = (6.609056770000279, 112.32629575900046, 4.307508287999553, 26.25732971999969, 0.07163010500062228)

plt.semilogy(x, postgresql)
plt.semilogy(x, mysql)
plt.semilogy(x, sqlite)

plt.title('Different DBMS (ORM)')
plt.legend(('PostgreSQL', 'MySQL', 'SQLite'))
plt.xticks(x, xticks, fontproperties=zh_font)
plt.xlabel('SQL Statements')
plt.ylabel('Time (seconds)')
plt.savefig(__file__.replace('.py', '.png'))
