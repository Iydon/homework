import os

from model import FaceNet


root = 'images'
threshold = 1
output = 'result.csv'

result = dict()
fn = FaceNet(mtcnn=dict(post_process=True, keep_all=False))
for dirname, _, filenames in os.walk(root):
    if filenames:
        print(dirname)
        key = int(os.path.split(dirname)[-1])
        for filename in filenames:
            path = os.path.join(dirname, filename)
            fn.add_image(fn.imread(path), key)
        x, y = fn._kwargs['data'][key]
        flag = int((x-y).norm() < threshold)
        result[key] = flag
        fn._kwargs['data'].clear()
with open(output, 'w') as f:
    for key in sorted(result):
        f.write(f'{key},{result[key]}\n')
