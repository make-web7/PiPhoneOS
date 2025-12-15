import os
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from picamera2 import Picamera2

PHOTOS_DIR = os.path.expanduser("~/PiPhoneOS/photos")

class CameraApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        os.makedirs(PHOTOS_DIR, exist_ok=True)

        # Initialize camera
        self.camera = Picamera2()
        config = self.camera.create_preview_configuration(
            main={"size": (640, 480)}
        )
        self.camera.configure(config)
        self.camera.start()

        # UI
        self.preview_label = tk.Label(self)
        self.preview_label.pack(fill="both", expand=True)

        self.capture_button = ttk.Button(
            self,
            text="📸 Take Photo",
            command=self.take_photo
        )
        self.capture_button.pack(pady=10)

        self.update_preview()

    def update_preview(self):
        frame = self.camera.capture_array()
        image = Image.fromarray(frame)
        image = image.resize((480, 360))
        self.photo = ImageTk.PhotoImage(image)
        self.preview_label.config(image=self.photo)
        self.after(30, self.update_preview)

    def take_photo(self):
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        filepath = os.path.join(PHOTOS_DIR, f"photo_{timestamp}.jpg")
        self.camera.capture_file(filepath)
        print(f"Saved photo: {filepath}")
