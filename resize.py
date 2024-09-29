import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog
from PIL import Image
import os

class DragDropBox(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(relief="sunken", bd=2, width=400, height=200)
        self.pack_propagate(False)
        self.label = tk.Label(self, text="Drag and Drop Files Here")
        self.label.pack(expand=True)
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.drop)
        self.file_paths = []

    def drop(self, event):
        self.file_paths = event.data.split()
        self.label.config(text="\n".join(self.file_paths))

def resize_images(file_paths,message_label):
    if file_paths:
        for file_path in file_paths:
            try:
                img = Image.open(file_path)
                width, height = img.size

                directory, filename = os.path.split(file_path)
                name, ext = os.path.splitext(filename)

                half_width, half_height = width // 2, height // 2
                half_size = img.resize((half_width, half_height), Image.HAMMING)
                half_size.save(os.path.join(directory, f"{name}_{half_width}px{ext}"))

                quarter_width, quarter_height = width // 4, height // 4
                quarter_size = img.resize((quarter_width, quarter_height), Image.HAMMING)
                quarter_size.save(os.path.join(directory, f"{name}_{quarter_width}px{ext}"))

                message_label.config(text=f"Images resized and saved as {name}_{half_width}px{ext} and {name}_{quarter_width}px{ext} in {directory}")
            except Exception as e:
                message_label.config(text=f"Error resizing image {file_path}: {e}")
    else:
        message_label.config(text="No files to resize")

def create_gui():
    root = TkinterDnD.Tk()
    root.title("Image Resizer The Goat")

    drag_drop_box = DragDropBox(root)
    drag_drop_box.pack(pady=20)

    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, pady=10)

    message_label = tk.Label(root, text="")
    message_label.pack(pady=10)

    button1 = tk.Button(button_frame, text="Resize Images", command=lambda: resize_images(drag_drop_box.file_paths,message_label))
    button1.pack(side=tk.LEFT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
    