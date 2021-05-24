#!/usr/bin/python
# _*_ coding:UTF-8 _*_

import tkinter as tk
from tkinter.filedialog import askopenfilename
# noinspection PyUnresolvedReferences
from PIL import Image, ImageTk

window = tk.Tk()
window.title('aa')
window.geometry('800x600')


var = tk.StringVar()


def Open_Img():
    file_path = askopenfilename()
    Img = Image.open(file_path)
    Img = Img.resize((400,400))
    img_png = ImageTk.PhotoImage(Img)
    Label_Show.configure(image=img_png)
    Label_Show.image = img_png
    var.set(123124)


Label_Show = tk.Label(window,
                      width=200, height=200)

btn_Open = tk.Button(window,
                     text='打开图像',
                     width=15, height=2,
                     command=Open_Img)

Label_Data = tk.Label(window,
                      text=var)

btn_Open.pack()
Label_Show.pack()
# btn_Clear.pack()
Label_Data.pack()
window.mainloop()