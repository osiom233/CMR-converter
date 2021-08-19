# CMR2PNG with GUI
# Author:Osiom
import tkinter as tk
import tkinter.filedialog as op
import tkinter.messagebox as msgbox
import os
import math
import zlib
import base64
import pathlib
from PIL import Image
from icon import img
from typing import Optional

top = None
top2 = None
bar = None
file = None
path = None


def select_file():
    global bar
    global file
    file = op.askopenfilename(title='选择目标文件', filetypes=[
                              ('cmr', '*.cmr'), ('png', '*.png')])
    if file:
        bar.set('已选择目标文件\n请选择输出路径')


def select_path():
    global bar
    if not file:
        msgbox.showerror(title='错误', message='未选择目标文件')
    else:
        global path
        path = op.askdirectory()
        bar.set('准备就绪\n请选择转换模式')


def mode():
    global top
    if not path or not file:
        msgbox.showerror(title='错误', message='未选择目标文件或输出路径')
    else:
        select(1)


def main():
    global bar
    global top
    top = tk.Tk()
    top.title('P2C')
    top.geometry('200x135')
    top.resizable(0, 0)
    tmp = open('tmp.ico', "wb+")
    tmp.write(base64.b64decode(img))
    tmp.close()
    top.iconbitmap('tmp.ico')
    os.remove('tmp.ico')
    bar = tk.StringVar()

    t1 = tk.Label(top, textvariable=bar, bg='white', fg='black',
                  font=('Arial', 12), width=30, height=2)
    t1.pack()
    bar.set('贴图转换工具\n作者：Osiom')
    a = tk.Button(top, text='1.选择目标文件', font=('Arial', 12),
                  width=30, height=1, command=select_file)
    a.pack()
    b = tk.Button(top, text='2.选择输出路径', font=('Arial', 12),
                  width=30, height=1, command=select_path)
    b.pack()
    c = tk.Button(top, text='3.选择转换模式', font=('Arial', 12),
                  width=30, height=1, command=mode)
    c.pack()

    top.mainloop()


def select(mode):
    global top2
    if mode == 1:
        top.destroy()
        top2 = tk.Tk()
        top2.title('P2C')
        top2.geometry('200x135')
        tmp = open('tmp.ico', "wb+")
        tmp.write(base64.b64decode(img))
        tmp.close()
        top2.iconbitmap('tmp.ico')
        os.remove('tmp.ico')
        top2.resizable(0, 0)
        bar2 = tk.StringVar()
        t = tk.Label(top2, textvariable=bar2, bg='white', fg='black',
                     font=('Arial', 12), width=30, height=2)
        t.pack()
        bar2.set('请选择转换模式')
        c1 = tk.Button(top2, text='PNG to CMR', font=('Arial', 12),
                       width=30, height=1, command=PNG2CMR)
        c1.pack()
        c2 = tk.Button(top2, text='CMR to PNG', font=('Arial', 12),
                       width=30, height=1, command=ctp)
        c2.pack()
        c3 = tk.Button(top2, text='CMR to PNG*', font=('Arial', 12),
                       width=30, height=1, command=ctp2)
        c3.pack()
        top2.mainloop()
    if mode == 0:
        top2.destroy()


def PNG2CMR():
    fileA = Image.open(file).transpose(Image.FLIP_TOP_BOTTOM)
    [width, height] = fileA.size
    pixellist = []
    for j in range(0, height):
        for i in range(0, width):
            tuplepixel = fileA.getpixel((i, j))
            if len(tuplepixel) == 3:
                tuplepixel = list(tuplepixel)+[255]
            pixellist += list(tuplepixel)
    bytespixel = bytes(pixellist)
    bytesencode = zlib.compress(bytespixel)
    filename = pathlib.Path(file).stem
    os.chdir(path)
    fileB = open(filename+".cmr", "wb+")
    fileB.write(bytesencode)
    msgbox.showinfo(title='成功', message=f'文件已保存至{path}')
    select(0)


def ctp():
    filename = pathlib.Path(file).stem

    def getrgba(i, j):
        global a
        a = (width*j+i)*4
        return (textbytes[a], textbytes[a+1], textbytes[a+2], textbytes[a+3])
    fileA = open(file, "rb+")
    raw = fileA.read()
    textbytes = zlib.decompress(raw)
    width = int(math.sqrt(len(textbytes)/4))
    height = width
    if len(textbytes) >= width*height*4:
        pass
    else:
        1/0
    img = Image.new("RGBA", (width, height), (255, 255, 255))
    for j in range(0, height):
        for i in range(0, width):
            img.putpixel((i, j), getrgba(i, j))
    os.chdir(path)

    img.transpose(Image.FLIP_TOP_BOTTOM).save(filename+".png")
    msgbox.showinfo(title='成功', message=f'文件已保存至{path}')
    select(0)


def ctp2():
    filename = pathlib.Path(file).stem

    def getrgba(i, j):
        global a
        a = (width*j+i)*4
        return (textbytes[a], textbytes[a+1], textbytes[a+2], textbytes[a+3])
    f1 = open(file, "rb+")
    raw = f1.read()
    textbytes = zlib.decompress(raw)
    width = int(math.sqrt(len(textbytes)/4))
    height = width * 2
    if len(textbytes) >= width*height*4:
        pass
    else:
        pass
        1/0
    img = Image.new("RGBA", (width, height), (255, 255, 255))
    for j in range(0, height):
        for i in range(0, width):
            img.putpixel((i, j), getrgba(i, j))
    os.chdir(path)

    img.transpose(Image.FLIP_TOP_BOTTOM).save(filename+".png")
    msgbox.showinfo(title='成功', message=f'文件已保存至{path}')
    select(0)


if __name__ == '__main__':
    main()
