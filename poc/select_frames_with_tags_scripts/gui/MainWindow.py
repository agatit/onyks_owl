from dataclasses import dataclass
import tkinter as tk

from PIL import Image, ImageTk


class MainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        labels_container = tk.Frame(self)
        self.labels_container = labels_container

        class_label = tk.Label(labels_container, text="class")
        class_label.pack(side=tk.LEFT, expand=True)
        self.class_label = class_label

        counter_label = tk.Label(labels_container, text="counter")
        counter_label.pack(side=tk.LEFT, expand=False)
        self.class_label = counter_label

        labels_container.pack(side=tk.TOP, fill=tk.X)

        image_canvas = tk.Canvas(self, bg="blue")
        image_canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.image_canvas = image_canvas

        self.original_image = None
        self.tk_image = None
        img_path = r"C:\Users\wrzezniczak\Desktop\wagon_project\testy\kamera_2\rectify_configs\hiv00000.png"
        self.load_image(img_path)

        self.bind("<Configure>", self.resize_event)

    def load_image(self, img_path):
        self.original_image = Image.open(img_path)
        self.tk_image = ImageTk.PhotoImage(self.original_image)

    def resize_event(self, event):
        self.refresh_image()


    def refresh_image(self):
        image_canvas = self.image_canvas

        image_canvas.update()
        canvas_size = image_canvas.winfo_width(), image_canvas.winfo_height()
        resized_image = self.original_image.resize(canvas_size)

        self.tk_image = ImageTk.PhotoImage(resized_image)
        image_canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
