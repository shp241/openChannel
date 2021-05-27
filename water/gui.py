#!/usr/bin/python
# _*_ coding:UTF-8 _*_

import tkinter as tk
from tkinter.filedialog import askopenfilename
# noinspection PyUnresolvedReferences
import cv2
from PIL import Image, ImageTk
import fuc

window = tk.Tk()
window.title('openChannel')
window.geometry('1920x1080')


def open_img():
    file_path = askopenfilename()
    Img = Image.open(file_path)
    Img = Img.resize((960, 720))
    img_png = ImageTk.PhotoImage(Img)
    you = "image\\" + file_path.split("image/")[1][0]
    adj = fuc.adjust_image(file_path.replace("/", "\\"), fuc.ori[you], fuc.x[you], fuc.a[you], fuc.k[you])
    a = file_path.split("/")[-1].split("_")[0]
    p = str(fuc.get_deep(adj, fuc.k[you]))
    m = str(format(fuc.use_model(adj, fuc.k[you]), '.1f'))
    Label_Show.configure(image=img_png)
    Label_Show.image = img_png
    t = "actual:" + a + ",line:" + p + ",model:" + m
    Label_Data.configure(text=t)
    Label_Data.text = t


Label_Show = tk.Label(window)

btn_Open = tk.Button(window,
                     text='打开图像',
                     width=15, height=2,
                     command=open_img)

Label_Data = tk.Label(window,
                      text="",
                      font=("Arial", 16, "bold"))

if __name__ == "__main__":
    Label_Show.pack()
    Label_Data.pack()
    btn_Open.pack()
    window.mainloop()
