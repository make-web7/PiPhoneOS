import os
import tkinter as tk
from PIL import Image, ImageTk

PHOTOS_DIR = os.path.expanduser("~/PiPhoneOS/photos")
THUMB_SIZE = (120, 120)

class PhotosApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.title = tk.Label(self, text="Photos", font=("Arial", 18))
        self.title.pack(pady=10)

        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.load_photos()

    def load_photos(self):
        self.thumbnails = []

        if not os.path.exists(PHOTOS_DIR):
            return

        files = sorted(
            [f for f in os.listdir(PHOTOS_DIR) if f.lower().endswith(".jpg")],
            reverse=True
        )

        for idx, filename in enumerate(files):
            path = os.path.join(PHOTOS_DIR, filename)

            image = Image.open(path)
            image.thumbnail(THUMB_SIZE)
            thumb = ImageTk.PhotoImage(image)
            self.thumbnails.append(thumb)

            btn = tk.Button(
                self.scrollable_frame,
                image=thumb,
                command=lambda p=path: self.open_photo(p),
                relief="flat"
            )
            btn.grid(row=idx // 3, column=idx % 3, padx=5, pady=5)

    def open_photo(self, path):
        viewer = tk.Toplevel(self)
        viewer.attributes("-fullscreen", True)

        image = Image.open(path)
        screen_width = viewer.winfo_screenwidth()
        screen_height = viewer.winfo_screenheight()
        image.thumbnail((screen_width, screen_height))

        photo = ImageTk.PhotoImage(image)

        label = tk.Label(viewer, image=photo)
        label.image = photo
        label.pack(expand=True)

        close_btn = tk.Button(
            viewer,
            text="✕ Close",
            command=viewer.destroy,
            font=("Arial", 16)
        )
        close_btn.pack(pady=20)
