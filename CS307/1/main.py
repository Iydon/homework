import os
from PIL import Image


images = ('1.jpg', '2.jpg')
pdf_name = 'cs307-1-11711217.pdf'

Is = [Image.open(image) for image in images]
if not os.path.exists(pdf_name):
	Is[0].save(pdf_name, 'PDF', resolution=100.0, save_all=True, append_images=Is[1:])
