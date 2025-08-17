import tkinter as tk 
from PIL import Image, ImageTk
from itertools import count

class AnimatedGif(tk.Label):

    def __init__ (self, master, gif_path, delay=100):
        super().__init__(master)
        self.gif = Image.open(gif_path)
        self.delay = delay
        self.frames = []

        try:
            for i in count(1):
                frame = ImageTk.PhotoImage(self.gif.copy())
                self.frames.append(frame)
                self.gif.seek(i)
        except EOFError:
            pass

        self.frame_index = 0
        self.update_frame()

    def update_frame(self):
        self.configure(image=self.frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.after(self.delay, self.update_frame)

