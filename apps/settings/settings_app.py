import tkinter as tk
import os

class SettingsApp:
    def __init__(self, root):
        self.root = root

        self.win = tk.Toplevel(root)
        self.win.title("Settings")
        self.win.geometry("800x480")

        tk.Label(self.win, text="Screen Brightness", font=("Arial", 24)).pack(pady=20)

        self.scale = tk.Scale(self.win, from_=20, to=255, orient=tk.HORIZONTAL, command=self.set_brightness, length=600)
        self.scale.pack()

        # Try reading current brightness
        try:
            with open("/sys/class/backlight/*/brightness", "r") as f:
                current = int(f.read().strip())
                self.scale.set(current)
        except:
            pass

    def set_brightness(self, value):
        try:
            os.system(f"sudo sh -c 'echo {value} > /sys/class/backlight/*/brightness'")
        except:
            pass

