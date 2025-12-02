import tkinter as tk
from picamera2 import Picamera2
from PIL import Image, ImageTk
import time
import os

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_still_configuration())
        self.camera.start()

        self.win = tk.Toplevel(root)
        self.win.title("Camera")

        self.preview_label = tk.Label(self.win)
        self.preview_label.pack()

        self.update_preview()

        tk.Button(self.win, text="📸 Capture", font=("Arial", 24), command=self.take_photo).pack(pady=10)

    def update_preview(self):
        frame = self.camera.capture_array()
        img = Image.fromarray(frame)
        img = img.resize((800, 450))
        tk_img = ImageTk.PhotoImage(img)
        self.preview_label.configure(image=tk_img)
        self.preview_label.image = tk_img
        self.preview_label.after(30, self.update_preview)

    def take_photo(self):
        folder = "/home/pi/PiPhonePhotos"
        os.makedirs(folder, exist_ok=True)
        filename = f"{folder}/photo_{int(time.time())}.jpg"
        self.camera.capture_file(filename)
        print("Saved:", filename)

