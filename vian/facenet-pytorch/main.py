import cv2
import os

from model import FaceNet


filename = 'data/facenet.pickle'
video = 'data/test/video.mp4'
dirname = 'data/train'

if os.path.exists(filename):
    fn = FaceNet.load(filename)
else:
    fn = FaceNet().add_images_from_folder(dirname)
    fn.save(filename)

video = cv2.VideoCapture(video)
while True:
    success, frame = video.read()
    if not success:
        break
    image = fn.image_to_image(frame)
    cv2.imshow('Video', image)
    cv2.waitKey(50)
video.release()
cv2.destroyAllWindows()
