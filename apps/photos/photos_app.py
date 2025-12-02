import tkinter as tk
from PIL import Image, ImageTk
import os
import glob

class PhotosApp:
    def __init__(self, root):
        self.root = root
        self.win = tk.Toplevel(root)
        self.win.title("Photos")
        self.win.geometry("800x480")

        self.folder = "/home/pi/PiPhonePhotos"
        os.makedirs(self.folder, exist_ok=True)

        self.photos = sorted(glob.glob(f"{self.folder}/*.jpg"))
        self.index = 0

        self.photo_label = tk.Label(self.win)
        self.photo_label.pack()

        tk.Button(self.win, text="◀", font=("Arial", 24), command=self.prev).pack(side="left", padx=10)
        tk.Button(self.win, text="▶", font=("Arial", 24), command=self.next).pack(side="right", padx=10)

        if self.photos:
            self.show()

    def show(self):
        img = Image.open(self.photos[self.index])
        img = img.resize((800, 450))
        tk_img = ImageTk.PhotoImage(img)
        self.photo_label.configure(image=tk_img)
        self.photo_label.image = tk_img

    def next(self):
        if self.photos:
            self.index = (self.index + 1) % len(self.photos)
            self.show()

    def prev(self):
        if self.photos:
            self.index = (self.index - 1) % len(self.photos)
            self.show()

