from io import BytesIO
import os
import numpy as np
import requests as req
from PIL import Image


from requests.models import Response
# gray scale level values from:
# http://paulbourke.net/dataformats/asciiart/

# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# 10 levels of gray
gscale2 = "@%#*+=-:. "


def get_pic_average(image):
    im = np.array(image)
    w, h = im.shape
    return np.average(im.reshape(w*h))


def InputFile(pic_url):
    path = pic_url
    if path.startswith("http"):
        response = req.get(path)
        image = Image.open(BytesIO(response.content)).convert("L")
    else:
        image = Image.open(path).convert("L")
    W, H = image.size[0], image.size[1]
    return image, W, H


def pic_to_ascii(image, W, H, scale):
    max_ = np.where(W > 1024, 1024, W)
    cols = max_
    cols = int(cols)
    w = W/cols
    h = w/scale
    rows = int(H/h)
    aimg = []
    for i in range(rows):
        y1 = int(h*i)
        y2 = int(h*(i+1))
        if i == rows-1:
            y2 = H
        for j in range(cols):
            x1 = int(w*j)
            x2 = int(w*(j+1))
            if j == cols-1:
                x2 = W
            img = image.crop((x1, y1, x2, y2))
            avg = int(get_pic_average(img))
            gsval = gscale2[int(avg*9/255)]
            aimg.append(gsval)
    return aimg, cols


def main(pic_url):
    scale = 0.43
    image, W, H = InputFile(pic_url)
    aimg, cols = pic_to_ascii(image, W, H, scale)
    savepath = os.getcwd()+"\\static\\img\\"
    filename = "pic.txt"
    f = open("{}{}".format(savepath, filename), "w")
    for i in range(len(aimg)):
        if i % cols == 0:
            n = "\n"
        else:
            n = ""
        f.write("{}{}".format(aimg[i], n))
    f.close()
