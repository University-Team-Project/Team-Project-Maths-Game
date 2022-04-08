import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import glob

width = 1000  # Window Width
height = 600  # Window height


class Carousel(tkinter.Canvas):
    def __init__(self, master):
        super().__init__()
        self.config(width=width, height=height)
        self.pack()
        self.stitchImages()
        self.showPhoto()
        self.loadIndicator()
        self.current = 1

    def stitchImages(self):

        # Load Images
        images = []
        for filename in glob.glob('images/*.jpg'):
            images.append(Image.open(filename))
        # Resize Images
        for i in range(len(images)):
            images[i] = images[i].resize((width, height), Image.ANTIALIAS)
        # Stitch Image
        widths, heights = zip(*(i.size for i in images))
        print(widths, heights)
        total_width = sum(widths)
        max_height = max(heights)
        self.stitched = Image.new('RGB', (total_width, max_height))
        x_offset = 0
        for im in images:
            self.stitched.paste(im, (x_offset, 0))
            x_offset += im.size[0]
        self.stitched = self.stitched.resize((len(images) * 1000, 600))
        self.length = len(images)

    def showPhoto(self):
        # Show Stitched Image
        self.stitched = ImageTk.PhotoImage(self.stitched)
        self.Photo = self.create_image((0, 0), image=self.stitched, anchor='nw')

    def loadIndicator(self):
        # Indicator
        self.ind = self.create_rectangle(1, 590, 250, 600, fill='white', outline='white')

    def moveImageRight(self):
        if self.current < 4:
            self.current += 1
            for i in range(25):
                self.after(1, self.move(self.Photo, -40, 0))
                self.after(1, self.move(self.ind, 10, 0))
                self.update()


    def moveImageLeft(self):
        if self.current > 0:
            self.current -= 1
            for i in range(25):
                self.after(1, self.move(self.Photo, 40, 0))
                self.after(1, self.move(self.ind, -10, 0))
                self.update()
