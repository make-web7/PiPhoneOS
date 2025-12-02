import tkinter as tk
from apps.camera.camera_app import CameraApp
from apps.photos.photos_app import PhotosApp
from apps.settings.settings_app import SettingsApp

class Launcher:
    def __init__(self, root):
        self.root = root
        self.root.title("PiPhone")
        self.root.geometry("800x480")
        self.root.configure(bg="black")

        tk.Label(root, text="PiPhone", fg="white", bg="black", font=("Arial", 32)).pack(pady=20)

        tk.Button(root, text="Camera", font=("Arial", 20), width=15, command=self.open_camera).pack(pady=10)
        tk.Button(root, text="Photos", font=("Arial", 20), width=15, command=self.open_photos).pack(pady=10)
        tk.Button(root, text="Settings", font=("Arial", 20), width=15, command=self.open_settings).pack(pady=10)

    def open_camera(self):
        CameraApp(self.root)

    def open_photos(self):
        PhotosApp(self.root)

    def open_settings(self):
        SettingsApp(self.root)

root = tk.Tk()
Launcher(root)
root.mainloop()

