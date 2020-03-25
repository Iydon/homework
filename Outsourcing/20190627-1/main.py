# -*- coding: utf-8 -*-
# License: GNU GPLv3
# Time: 2019-06-27
print("""
# -*- coding: utf-8 -*-
# License: GNU GPLv3
# Time: 2019-06-27
""")

import turtle as te
print("import turtle as te")
from bs4 import BeautifulSoup
import numpy as np
import cv2
import os


WriteStep = 15  # number of samples of the Bessel function
Speed = 1000
Width = 300
Height = 600
Xh = 0
Yh = 0
scale = (1, 1)
first = True
K = 32
filename = "target.jpg"
print("""
WriteStep = 15  # number of samples of the Bessel function
Speed = 1000
Width = 300
Height = 600
Xh = 0
Yh = 0
""")


def Bezier(p1, p2, t):
    # 一阶贝塞尔函数
    return p1*(1-t) + p2*t
print("""
def Bezier(p1, p2, t):
    # first order Bessel function
    return p1*(1-t) + p2*t
""")


def Bezier_2(x1, y1, x2, y2, x3, y3):
    # 二阶贝塞尔函数
    te.goto(x1, y1)
    te.pendown()
    for t in range(0, WriteStep+1):
        x = Bezier(Bezier(x1, x2, t/WriteStep),
                   Bezier(x2, x3, t/WriteStep), t/WriteStep)
        y = Bezier(Bezier(y1, y2, t/WriteStep),
                   Bezier(y2, y3, t/WriteStep), t/WriteStep)
        te.goto(x, y)
    te.penup()
print("""
def Bezier_2(x1, y1, x2, y2, x3, y3):
    # second order Bessel function
    te.goto(x1, y1)
    te.pendown()
    for t in range(0, WriteStep+1):
        x = Bezier(Bezier(x1, x2, t/WriteStep),
                   Bezier(x2, x3, t/WriteStep), t/WriteStep)
        y = Bezier(Bezier(y1, y2, t/WriteStep),
                   Bezier(y2, y3, t/WriteStep), t/WriteStep)
        te.goto(x, y)
    te.penup()
""")


def Bezier_3(x1, y1, x2, y2, x3, y3, x4, y4):
    # 三阶贝塞尔函数
    x1 = -Width/2 + x1
    y1 = Height/2 - y1
    x2 = -Width/2 + x2
    y2 = Height/2 - y2
    x3 = -Width/2 + x3
    y3 = Height/2 - y3
    x4 = -Width/2 + x4
    y4 = Height/2 - y4  # 坐标变换
    te.goto(x1, y1)
    te.pendown()
    for t in range(0, WriteStep + 1):
        x = Bezier(Bezier(Bezier(x1, x2, t/WriteStep), Bezier(x2, x3, t/WriteStep), t/WriteStep),
                   Bezier(Bezier(x2, x3, t/WriteStep), Bezier(x3, x4, t/WriteStep), t/WriteStep), t/WriteStep)
        y = Bezier(Bezier(Bezier(y1, y2, t/WriteStep), Bezier(y2, y3, t/WriteStep), t/WriteStep),
                   Bezier(Bezier(y2, y3, t/WriteStep), Bezier(y3, y4, t/WriteStep), t/WriteStep), t/WriteStep)
        te.goto(x, y)
    te.penup()
print("""
def Bezier_3(x1, y1, x2, y2, x3, y3, x4, y4):
    # third order Bessel function
    x1 = -Width/2 + x1
    y1 = Height/2 - y1
    x2 = -Width/2 + x2
    y2 = Height/2 - y2
    x3 = -Width/2 + x3
    y3 = Height/2 - y3
    x4 = -Width/2 + x4
    y4 = Height/2 - y4  # coordinate transformation
    te.goto(x1, y1)
    te.pendown()
    for t in range(0, WriteStep + 1):
        x = Bezier(Bezier(Bezier(x1, x2, t/WriteStep), Bezier(x2, x3, t/WriteStep), t/WriteStep),
                   Bezier(Bezier(x2, x3, t/WriteStep), Bezier(x3, x4, t/WriteStep), t/WriteStep), t/WriteStep)
        y = Bezier(Bezier(Bezier(y1, y2, t/WriteStep), Bezier(y2, y3, t/WriteStep), t/WriteStep),
                   Bezier(Bezier(y2, y3, t/WriteStep), Bezier(y3, y4, t/WriteStep), t/WriteStep), t/WriteStep)
        te.goto(x, y)
    te.penup()
""")


def Moveto(x, y):
    # 移动到svg坐标下（x，y）
    te.penup()
    te.goto(-Width/2+x, Height/2-y)
    te.pendown()
print("""
def Moveto(x, y):
    # move to coordinate (x, y)
    te.penup()
    te.goto(-Width/2+x, Height/2-y)
    te.pendown()
""")


def Moveto_r(dx, dy):
    te.penup()
    te.goto(te.xcor()+dx, te.ycor()-dy)
    te.pendown()
print("""
def Moveto_r(dx, dy):
    te.penup()
    te.goto(te.xcor()+dx, te.ycor()-dy)
    te.pendown()
""")


def line(x1, y1, x2, y2):
    # 连接svg坐标下两点
    te.penup()
    te.goto(-Width/2+x1, Height/2-y1)
    te.pendown()
    te.goto(-Width/2+x2, Height/2-y2)
    te.penup()
print("""
def line(x1, y1, x2, y2):
    # connect (x1, y1) and (x2, y2)
    te.penup()
    te.goto(-Width/2+x1, Height/2-y1)
    te.pendown()
    te.goto(-Width/2+x2, Height/2-y2)
    te.penup()
""")


def Lineto_r(dx, dy):
    # 连接当前点和相对坐标（dx，dy）的点
    te.pendown()
    te.goto(te.xcor()+dx, te.ycor()-dy)
    te.penup()
print("""
def Lineto_r(dx, dy):
    # connect (x0, y0) and (x0+dx, y0+dy)
    te.pendown()
    te.goto(te.xcor()+dx, te.ycor()-dy)
    te.penup()
""")


def Lineto(x, y):
    # 连接当前点和svg坐标下（x，y）
    te.pendown()
    te.goto(-Width/2+x, Height/2-y)
    te.penup()
print("""
def Lineto(x, y):
    # connect (x0, y0) and (x, y)
    te.pendown()
    te.goto(-Width/2+x, Height/2-y)
    te.penup()
""")


def Curveto(x1, y1, x2, y2, x, y):
    # 三阶贝塞尔曲线到（x，y）
    te.penup()
    X_now = te.xcor() + Width/2
    Y_now = Height/2 - te.ycor()
    Bezier_3(X_now, Y_now, x1, y1, x2, y2, x, y)
    global Xh
    global Yh
    Xh = x - x2
    Yh = y - y2
print("""
def Curveto(x1, y1, x2, y2, x, y):
    # third order Bessel function to(x, y)
    te.penup()
    X_now = te.xcor() + Width/2
    Y_now = Height/2 - te.ycor()
    Bezier_3(X_now, Y_now, x1, y1, x2, y2, x, y)
    global Xh
    global Yh
    Xh = x - x2
    Yh = y - y2
""")


def Curveto_r(x1, y1, x2, y2, x, y):
    # 三阶贝塞尔曲线到相对坐标（x，y）
    te.penup()
    X_now = te.xcor() + Width/2
    Y_now = Height/2 - te.ycor()
    Bezier_3(X_now, Y_now, X_now + x1, Y_now + y1,
             X_now + x2, Y_now + y2, X_now + x, Y_now + y)
    global Xh
    global Yh
    Xh = x - x2
    Yh = y - y2
print("""
def Curveto_r(x1, y1, x2, y2, x, y):
    # third order Bessel function to(x0+x, y0+y)
    te.penup()
    X_now = te.xcor() + Width/2
    Y_now = Height/2 - te.ycor()
    Bezier_3(X_now, Y_now, X_now + x1, Y_now + y1,
             X_now + x2, Y_now + y2, X_now + x, Y_now + y)
    global Xh
    global Yh
    Xh = x - x2
    Yh = y - y2
""")


def transform(w_attr):
    funcs = w_attr.split(" ")
    for func in funcs:
        func_name = func[0: func.find("(")]
        if func_name == "scale":
            global scale
            scale = (float(func[func.find("(") + 1: -1].split(",")[0]),
                     -float(func[func.find("(") + 1: -1].split(",")[1]))


def readPathAttrD(w_attr):
    ulist = w_attr.split(" ")
    for i in ulist:
        if i.isdigit() or i.isalpha():
            yield float(i)
        elif i[0].isalpha():
            yield i[0]
            yield float(i[1:])
        elif i[-1].isalpha():
            yield float(i[0: -1])
        elif i[0] == "-":
            yield float(i)


def drawSVG(filename, w_color):
    global first
    SVGFile = open(filename, "r")
    SVG = BeautifulSoup(SVGFile.read(), "lxml")
    Height = float(SVG.svg.attrs["height"][0: -2])
    Width = float(SVG.svg.attrs["width"][0: -2])
    transform(SVG.g.attrs["transform"])
    if first:
        te.setup(height=Height, width=Width)
        print("te.setup(height={0}, width={1})".format(Height, Width))
        te.setworldcoordinates(-Width/2, 300, Width/2, -Height+300)
        print("te.setworldcoordinates(-{1}/2, 300, {1}/2, -{0}+300)".format(Height, Width))
        first = False
    te.tracer(100)
    print("te.tracer(100)")
    te.pensize(1)
    print("te.pensize(1)")
    te.speed(Speed)
    print("te.speed({0})".format(Speed))
    te.penup()
    print("te.penup()")
    te.color(w_color)
    print("te.color('{0}')".format(w_color))

    for i in SVG.find_all("path"):
        attr = i.attrs["d"].replace("\n", " ")
        f = readPathAttrD(attr)
        lastI = ""
        for i in f:
            if i == "M":
                te.end_fill()
                print("te.end_fill()")
                next1f = next(f)
                next2f = next(f)
                nextf = [next1f, next2f]
                Moveto(next1f*scale[0], next2f*scale[1])
                print("Moveto({0}*{2}, {1}*{3})".format(*nextf, *scale))
                te.begin_fill()
                print("te.begin_fill()")
            elif i == "m":
                te.end_fill()
                print("te.end_fill()")
                next1f = next(f)
                next2f = next(f)
                nextf = [next1f, next2f]
                Moveto_r(next1f*scale[0], next2f*scale[1])
                print("Moveto_r({0}*{2}, {1}*{3})".format(*nextf, *scale))
                te.begin_fill()
                print("te.begin_fill()")
            elif i == "C":
                next1f = next(f)
                next2f = next(f)
                next3f = next(f)
                next4f = next(f)
                next5f = next(f)
                next6f = next(f)
                nextf = [next1f, next2f, next3f, next4f, next5f, next6f]
                Curveto(next1f*scale[0], next2f*scale[1],
                        next3f*scale[0], next4f*scale[1],
                        next5f*scale[0], next6f*scale[1])
                print("Curveto({0}*{6}, {1}*{7}, {2}*{6}, {3}*{7}, {4}*{6}, {5}*{7})".format(*nextf, *scale))
                lastI = i
            elif i == "c":
                next1f = next(f)
                next2f = next(f)
                next3f = next(f)
                next4f = next(f)
                next5f = next(f)
                next6f = next(f)
                nextf = [next1f, next2f, next3f, next4f, next5f, next6f]
                Curveto_r(next1f*scale[0], next2f*scale[1],
                        next3f*scale[0], next4f*scale[1],
                        next5f*scale[0], next6f*scale[1])
                print("Curveto_r({0}*{6}, {1}*{7}, {2}*{6}, {3}*{7}, {4}*{6}, {5}*{7})".format(*nextf, *scale))
                lastI = i
            elif i == "L":
                next1f = next(f)
                next2f = next(f)
                nextf = [next1f, next2f]
                Lineto(next1f*scale[0], next2f*scale[1])
                print("Lineto({0}*{2}, {1}*{3})".format(*nextf, *scale))
            elif i == "l":
                next1f = next(f)
                next2f = next(f)
                nextf = [next1f, next2f]
                Lineto_r(next1f*scale[0], next2f*scale[1])
                print("Lineto_r({0}*{2}, {1}*{3})".format(*nextf, *scale))
                lastI = i
            elif lastI == "C":
                next1f = next(f)
                next2f = next(f)
                next3f = next(f)
                next4f = next(f)
                next5f = next(f)
                nextf = [next1f, next2f, next3f, next4f, next5f]
                Curveto(i*scale[0], next1f*scale[1],
                        next2f*scale[0], next3f*scale[1],
                        next4f*scale[0], next5f*scale[1])
                print("Curveto({0}*{6}, {1}*{7}, {2}*{6}, {3}*{7}, {4}*{6}, {5}*{7})".format(i, *nextf, *scale))
            elif lastI == "c":
                next1f = next(f)
                next2f = next(f)
                next3f = next(f)
                next4f = next(f)
                next5f = next(f)
                nextf = [next1f, next2f, next3f, next4f, next5f]
                Curveto_r(i*scale[0], next1f*scale[1],
                        next2f*scale[0], next3f*scale[1],
                        next4f*scale[0], next5f*scale[1])
                print("Curveto_r({0}*{6}, {1}*{7}, {2}*{6}, {3}*{7}, {4}*{6}, {5}*{7})".format(i, *nextf, *scale))
            elif lastI == "L":
                next1f = next(f)
                nextf = [next1f]
                Lineto(i*scale[0], next1f*scale[1])
                print("Lineto({0}*{2}, {1}*{3})".format(i, *nextf, *scale))
            elif lastI == "l":
                next1f = next(f)
                nextf = [next1f]
                Lineto_r(i*scale[0], next1f*scale[1])
                print("Lineto_r({0}*{2}, {1}*{3})".format(i, *nextf, *scale))
    te.penup()
    print("te.penup()")
    te.hideturtle()
    print("te.hideturtle()")
    te.update()
    print("te.update()")
    SVGFile.close()


def drawBitmap(w_image):
    Z = w_image.reshape((-1, 3))

    # convert to np.float32
    Z = np.float32(Z)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS, 10, 1.0)
    global K
    ret,label,center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res = res.reshape(w_image.shape)
    no = 1
    for i in center:
        no += 1
        res2 = cv2.inRange(res, i, i)
        res2 = cv2.bitwise_not(res2)
        cv2.imwrite(".tmp.bmp", res2)
        os.system("potrace .tmp.bmp -s --flat")
        drawSVG(".tmp.svg", "#%02x%02x%02x" % (i[2], i[1], i[0]))
    te.done()


if __name__ == "__main__":
    bitmap = cv2.imread(filename)
    drawBitmap(bitmap)
