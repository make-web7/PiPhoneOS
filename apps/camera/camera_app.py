import cv2
import os
from tkinter import Toplevel, Label, Button, Frame
from PIL import Image, ImageTk
from datetime import datetime

class CameraApp:
    def __init__(self, root):
        self.root = root
        
        # Create camera window
        self.window = Toplevel(root)
        self.window.title("Camera")
        self.window.geometry("800x480")
        self.window.configure(bg="black")

        # Create folder for photos
        os.makedirs("photos", exist_ok=True)

        # Start camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("❌ ERROR: Camera not detected!")
        
        # UI Elements
        self.preview_label = Label(self.window, bg="black")
        self.preview_label.pack(fill="both", expand=True)

        btn_frame = Frame(self.window, bg="black")
        btn_frame.pack(side="bottom", pady=10)

        self.capture_btn = Button(
            btn_frame,
            text="Capture Photo",
            font=("Arial", 14),
            command=self.capture_photo
        )
        self.capture_btn.pack(side="left", padx=10)

        self.exit_btn = Button(
            btn_frame,
            text="Exit",
            font=("Arial", 14),
            command=self.close_camera
        )
        self.exit_btn.pack(side="left", padx=10)

        # Start preview loop
        self.update_frame()

    def update_frame(self):
        """Grab frame from camera and update preview"""
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            self.preview_label.imgtk = imgtk
            self.preview_label.configure(image=imgtk)

        # Repeat after 10ms
        self.window.after(10, self.update_frame)

    def capture_photo(self):
        """Save current frame as an image"""
        ret, frame = self.cap.read()
        if ret:
            file_name = datetime.now().strftime("photo_%Y%m%d_%H%M%S.jpg")
            path = os.path.join("photos", file_name)
            cv2.imwrite(path, frame)
            print(f"📸 Saved: {path}")

    def close_camera(self):
        """Cleanup camera and close window"""
        if self.cap.isOpened():
            self.cap.release()
        self.window.destroy()

