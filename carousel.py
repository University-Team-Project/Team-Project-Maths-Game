import tkinter
from tkinter import *
from PIL import Image, ImageTk
import os
import glob
import time
import subprocess, sys

width = 1000  # Window Width
height = 600  # Window height

class Carousel(tkinter.Canvas):
    def __init__(self, master):
        super().__init__()
        self.screen = master
        self.games = {}
        self.config(width=width, height=height)
        self.pack()
        self.getGames()
        self.stitchImages()
        self.showPhoto()
        self.loadIndicator()
        self.current = 0
        self.game_name_label = tkinter.Label(self.screen, text="", font=("Inter", 24), bg="grey", fg="white")
        self.game_name_label.place(x=0 + 30, y=height - 75)
        self.loadScreenInfo()
        self.photo = tkinter.PhotoImage(file="Play_btn.png")
        self.button = Button(self.screen, image=self.photo, command=self.launch_game, background="#ffffff", borderwidth=0, highlightthickness=0)
        self.button.place(x=width / 2 - 50, y=height - 75)

    def getGames(self):
        for game in glob.glob('Games/*.txt'):
            name = os.path.basename(game).split('.')[0]
            f = open(game)
            data = [line[:-1] for line in f.readlines()] # Gets data in list then removes new line
            f.close()
            dict = {}
            for i in range(len(data)):
                line = data[i].rsplit(': ', 1)
                if line[0] == "image" or "game":
                    line[1] = "Games"+line[1]
                dict[line[0]] = line[1]
            self.games[name] = dict
            print(self.games)

    def stitchImages(self):

        # Load Images
        images = []
        for game in self.games:
            images.append(Image.open(self.games[game]['image']))
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
        if self.current < len(self.games) - 1:
            self.current += 1
            print(self.current)
            for i in range(25):
                print(self.after(1, self.move(self.Photo, -40, 0)))
                print(self.after(1, self.move(self.ind, 10, 0)))
                self.update()
                self.loadScreenInfo()
            print(self.current)


    def moveImageLeft(self):
        if self.current > 0:
            self.current -= 1
            print(self.current)
            for i in range(25):
                self.after(1, self.move(self.Photo, 40, 0))
                self.after(1, self.move(self.ind, -10, 0))
                self.update()
                self.loadScreenInfo()
            print(self.current)
        else:
            print("cant")

    def launch_game(self):
        self.screen.withdraw()
        running = True
        main_game_dir = os.getcwd()+"\\Games\\"+str(list(self.games)[self.current])
        game_dir = '\\'+str(self.games[list(self.games)[self.current]]["game"])
        game_dir.replace("/", "\\")
        import subprocess
        process = subprocess.Popen(os.getcwd()+game_dir, cwd=main_game_dir)
        poll = process.poll()
        print(poll)
        if poll is None:
            self.screen.deiconify()


    def loadScreenInfo(self):
        self.game_name_label['text'] = str(list(self.games)[self.current])
