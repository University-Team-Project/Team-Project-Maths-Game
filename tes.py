import tkinter as tk


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Slideshow")
        self.geometry("256x256")
        self.resizable(width=False, height=False)
        self.current_slide = tk.Label(self)
        self.current_slide.pack()
        self.duration_ms = 1000

    def set_image_directory(self, path):
        from pathlib import Path
        from PIL import Image, ImageTk
        from itertools import cycle

        image_paths = Path(path).glob("*.jpg")
        self.images = cycle(zip(map(lambda p: p.name, image_paths), map(ImageTk.PhotoImage, map(Image.open, image_paths))))

    def display_next_slide(self):
        name, self.next_image = next(self.images)
        self.current_slide.config(image=self.next_image)
        self.title(name)
        self.after(self.duration_ms, self.display_next_slide)

    def start(self):
        self.display_next_slide()

def main():

    application = Application()
    application.set_image_directory("dir/to/images")
    application.start()
    application.mainloop()


if __name__ == "__main__":
    import sys
    sys.exit(main())