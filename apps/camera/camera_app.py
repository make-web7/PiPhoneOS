import os
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput


PHOTOS_DIR = os.path.expanduser("~/PiPhoneOS/Photos")
os.makedirs(PHOTOS_DIR, exist_ok=True)


class CameraApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)

        self.recording = False

        # ---- Camera setup ----
        self.picam2 = Picamera2()
        config = self.picam2.create_preview_configuration(
            main={"size": (640, 480)}
        )
        self.picam2.configure(config)
        self.picam2.start()

        # ---- UI ----
        self.preview_label = tk.Label(self)
        self.preview_label.pack(pady=10)

        controls = tk.Frame(self)
        controls.pack()

        self.photo_btn = ttk.Button(
            controls, text="📷 Take Photo", command=self.take_photo
        )
        self.photo_btn.grid(row=0, column=0, padx=5)

        self.video_btn = ttk.Button(
            controls, text="🎥 Start Video", command=self.toggle_video
        )
        self.video_btn.grid(row=0, column=1, padx=5)

        # Start preview loop
        self.update_preview()

    # ---- Live Preview ----
    def update_preview(self):
        frame = self.picam2.capture_array()
        image = Image.fromarray(frame)
        image = image.resize((480, 360))
        photo = ImageTk.PhotoImage(image)

        self.preview_label.configure(image=photo)
        self.preview_label.image = photo

        self.after(30, self.update_preview)

    # ---- Take Photo ----
    def take_photo(self):
        filename = time.strftime("photo_%Y%m%d_%H%M%S.jpg")
        path = os.path.join(PHOTOS_DIR, filename)
        self.picam2.capture_file(path)
        print(f"Saved photo: {path}")

    # ---- Video Recording ----
    def toggle_video(self):
        if not self.recording:
            filename = time.strftime("video_%Y%m%d_%H%M%S.h264")
            self.video_path = os.path.join(PHOTOS_DIR, filename)

            encoder = H264Encoder(bitrate=10000000)
            output = FileOutput(self.video_path)

            self.picam2.start_recording(encoder, output)
            self.video_btn.config(text="⏹ Stop Video")
            self.recording = True
            print("Recording started")

        else:
            self.picam2.stop_recording()
            self.video_btn.config(text="🎥 Start Video")
            self.recording = False
            print(f"Saved video: {self.video_path}")

    # ---- Cleanup ----
    def close(self):
        if self.recording:
            self.picam2.stop_recording()
        self.picam2.stop()

