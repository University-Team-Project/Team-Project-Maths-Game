import tkinter
from tkinter import *
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import os
import glob
import csv
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
        self.trophy = tkinter.PhotoImage(file="tropy.png")
        self.button = Button(self.screen, image=self.trophy, command=self.getScores, background="#ffffff",borderwidth=0, highlightthickness=0)
        self.button.place(x=width -60, y=10)

    def getGames(self):
        for game in glob.glob('Games/*.txt'):
            name = os.path.basename(game).split('.')[0]
            f = open(game)
            data = [line[:-1] for line in f.readlines()] # Gets data in list then removes new line
            f.close()
            dict = {}
            for i in range(len(data)):
                line = data[i].rsplit(': ', 1)
                print(line)
                if line[0] == "image" or "game":
                    line[1] = "Games"+line[1]
                dict[line[0]] = line[1]
            self.games[name] = dict
            print(self.games)

    def getScores(self):
        header = ["Game","Player Name", "Score"]
        f = open("highscores.csv", "w", newline='')
        writer = csv.writer(f)
        writer.writerow(header)
        #get game from games dict
        for game in self.games:
            #get the scores for each game from the games dict
            path = self.games[game]["scores"]
            #open the path csv file
            with open(path, 'r') as csvfile:
                #store the values in a dict
                reader = csv.reader(csvfile)

                #skip the first line
                #next(reader)
                for row in reader:
                    print(game)
                    row[0] = game
                    writer.writerow(row)
        f.close()
        self.loadScores()
    # creates new window 500x500 on top of the main window
    def loadScores(self):
        self.highscores = Toplevel(self.screen)
        self.highscores.title("Python - Import CSV File To Tkinter Table")
        width = 500
        height = 400
        screen_width = self.highscores.winfo_screenwidth()
        screen_height = self.highscores.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.highscores.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.highscores.resizable(0, 0)
        TableMargin = Frame(self.highscores, width=500)
        TableMargin.pack(side=TOP)
        scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
        scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
        tree = ttk.Treeview(TableMargin, columns=("Game", "Player Name", "Score"), height=400,
                            selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('Game', text="Game", anchor=W)
        tree.heading('Player Name', text="Player Name", anchor=W)
        tree.heading('Score', text="Score", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=200)
        tree.column('#2', stretch=NO, minwidth=0, width=200)
        tree.column('#3', stretch=NO, minwidth=0, width=300)
        tree.pack()
        with open('highscores.csv') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                game = row['Game']
                player = row['Player Name']
                score = row['Score']
                tree.insert("", 0, values=(game, player, score))




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
                print(self.after(1, self.move(self.ind, 7.5, 0)))
                self.update()
                self.loadScreenInfo()
            print(self.current)


    def moveImageLeft(self):
        if self.current > 0:
            self.current -= 1
            print(self.current)
            for i in range(25):
                self.after(1, self.move(self.Photo, 40, 0))
                self.after(1, self.move(self.ind, -7.5, 0))
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
        game_dir = game_dir.replace("/", "\\")
        print(os.getcwd()+game_dir)
        print(main_game_dir)
        import subprocess
        process = subprocess.Popen(os.getcwd()+game_dir, cwd=main_game_dir)
        poll = process.poll()
        print(poll)
        if poll is None:
            self.screen.deiconify()


    def loadScreenInfo(self):
        self.game_name_label['text'] = str(list(self.games)[self.current])
