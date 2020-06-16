import collections
import cv2
import numpy
import os
import tqdm

import torch
from torchvision import datasets

from facenet_pytorch import MTCNN, InceptionResnetV1


class FaceNet:
    '''Face Net
    '''
    def __init__(self, mtcnn=dict(), resnet=dict(), threshold=1, device='cpu', data=None):
        # default arguments
        default_mtcnn = dict(
            image_size=160, margin=80, min_face_size=20, thresholds=[0.6, 0.7, 0.7],
            factor=0.709, post_process=False, keep_all=True, device=device,
        )
        default_resnet = dict(pretrained='vggface2', device=device)
        default_mtcnn.update(mtcnn)
        default_resnet.update(resnet)
        data = data or collections.defaultdict(list)
        # assign values
        self._kwargs = dict(mtcnn=mtcnn, resnet=resnet, threshold=threshold, device=device, data=data)
        self._mtcnn = MTCNN(**default_mtcnn)
        self._resnet = InceptionResnetV1(**default_resnet).eval()

    def add_image(self, image, label):
        for embedding in self._embed(image):
            self._kwargs['data'][label].append(embedding)

    def add_images_from_folder(self, root, progress_bar=True):
        dataset = datasets.ImageFolder(root)
        idx_to_class = {v: k for k, v in dataset.class_to_idx.items()}
        for image, idx in (tqdm.tqdm(dataset) if progress_bar else dataset):
            self.add_image(image, idx_to_class[idx])
        return self

    def image_to_labels(self, image_or_path, key=None, crop=True):
        '''返回图片人脸的标签
        '''
        key = key or (lambda x: sum(x)/len(x))
        result = list()
        embeddings = self._embed(self.imread(image_or_path), crop=crop)
        for embedding in embeddings:
            distances = {k: key(v) for k, v in self._distances(embedding).items()}
            label = min(distances, key=lambda x: distances[x])
            result.append(label if distances[label]<self._kwargs['threshold'] else None)
        return result

    def image_to_image(self, image_or_path, mark=True, font=5, size=1, thickness=1, offset=(5, 5), color=(255, 0, 0)):
        '''返回人脸标注的图片

        Argument:
            - image_or_path: [str, numpy.ndarray]
            - mark: bool
            - font: int, default is cv2.FONT_HERSHEY_COMPLEX_SMALL
            - size: float
            - thickness: float
            - offset: Tuple[float]
            - color: Tuple[int]
        '''
        image = self.imread(image_or_path)
        boxes, _ = self._mtcnn.detect(image, landmarks=False)
        if isinstance(boxes, numpy.ndarray):
            for box in boxes.astype(numpy.int):
                image = cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), color)
                if mark:
                    crop = image[box[1]: box[3], box[0]: box[2], :]
                    try:
                        label, = self.image_to_labels(crop, crop=False)
                    except:
                        label = 'ERROR'
                    coord = tuple(int(box[i]-offset[i]) for i in range(2))
                    image = cv2.putText(image, label or 'other', coord, font, size, color, thickness)
        return image

    def image_to_crops(self, image_or_path):
        '''
        Argument:
            - image_or_path: [str, numpy.ndarray]
        '''
        result = list()
        image = self.imread(image_or_path)
        boxes, _ = self._mtcnn.detect(image, landmarks=False)
        if isinstance(boxes, numpy.ndarray):
            for box in boxes.astype(numpy.int):
                result.append(image[box[1]: box[3], box[0]: box[2], :])
        return result

    def save(self, path):
        with open(path, 'wb') as f:
            torch.save(self._kwargs, f)

    @classmethod
    def load(cls, path, **kwargs):
        with open(path, 'rb') as f:
            data = torch.load(f)
            data.update(kwargs)
            return cls(**data)

    @classmethod
    def imread(cls, image_or_path):
        if isinstance(image_or_path, str):
            return cv2.imread(image_or_path)[:, :, ::-1].copy()
        elif isinstance(image_or_path, numpy.ndarray):
            return image_or_path
        else:
            raise NotImplementedError

    def _embed(self, image, crop=True):
        # __import__('IPython').embed(colors='Linux')
        if crop:
            faces = self._mtcnn(image)
            if faces is None:
                return numpy.array(tuple())
        else:
            face = cv2.resize(image, (self._mtcnn.image_size, self._mtcnn.image_size))
            faces = (torch.Tensor(face.transpose(2, 1, 0)), )
        return self._resnet(
            torch.stack(tuple(faces)).to(self._kwargs['device'])
        ).detach().cpu()

    def _distances(self, embedding, **kwargs):
        return {
            k: tuple((embedding-v).norm(**kwargs) for v in vs)
            for k, vs in self._kwargs['data'].items()
        }
