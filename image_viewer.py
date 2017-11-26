import tkinter as tk


class ImageViewer(tk.Tk):
    def __init__(self, interval):
        tk.Tk.__init__(self)
        self.frames = list()
        self.picture_display = tk.Label(self)
        self.picture_display.pack()
        self.current_frame = None
        self.interval = interval

    def add_frame(self, image):
        self.frames.append(image)

    def next(self):
        if len(self.frames) > 0:
            self.current_frame = self.frames.pop(0)
            self.picture_display.config(image=self.current_frame)
        self.after(self.interval, self.next)

    def slide_show(self):
        self.mainloop()


if __name__ == '__main__':
    v = ImageViewer(interval=3000)
    v.add_frame(tk.PhotoImage('../face-recognition/orl_faces/s1/1.pgm'))
    v.add_frame(tk.PhotoImage('../face-recognition/orl_faces/s1/2.pgm'))
    v.add_frame(tk.PhotoImage('../face-recognition/orl_faces/s1/3.pgm'))
    v.add_frame(tk.PhotoImage('../face-recognition/orl_faces/s1/4.pgm'))
    v.add_frame(tk.PhotoImage('../face-recognition/orl_faces/s1/5.pgm'))
    v.next()
    v.slide_show()