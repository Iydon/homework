import json
import os
import time

import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score

from model import FaceNet


# 参数设置
root = 'images'
threshold = 1
output = 'result.json'
validation = '验证集.csv'


# 数据读取
y_true = dict(zip(*map(
    lambda x: x[-1], pd.read_csv(os.path.join(root, validation)).items()
)))
y_pred = dict()
tic = time.time()
# 使用模型
fn = FaceNet(mtcnn=dict(post_process=True, keep_all=False))
for dirname, _, filenames in os.walk(root):
    if filenames and validation not in filenames and '.DS_Store' not in filenames:
        print(dirname)
        key = int(os.path.split(dirname)[-1])
        for filename in filenames:
            path = os.path.join(dirname, filename)
            fn.add_image(fn.imread(path), key)
        x, y = fn._kwargs['data'][key]
        flag = int((x-y).norm() < threshold)
        y_pred[key] = flag
        fn._kwargs['data'].clear()
# 结果写入
with open(output, 'w') as f:
    toc = time.time() - tic
    keys = sorted(y_pred)
    true, pred = tuple(y_true[k] for k in keys), tuple(y_pred[k] for k in keys)
    data = dict(
        y=dict(true=true, pred=pred), time=toc,
        score=dict(
            accuracy=accuracy_score(true, pred), precision=precision_score(true, pred),
            recall=recall_score(true, pred), roc_auc=roc_auc_score(true, pred),
        ),
    )
    json.dump(data, f, ensure_ascii=False, indent=2)
