import tkinter
from carousel import Carousel


def show(event):
    print(event.x, event.y)


class Application(tkinter.Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.bind('<Left>', moveImageLeft)
        self.bind('<Right>', moveImageRight) #twest


def moveImageRight(event):
    global car
    if car.current == 4:
        pass
    else:
        car.moveImageRight()


def moveImageLeft(event):
    global car
    if car.current == 1:
        pass
    else:
        car.moveImageLeft()


def main():
    global car
    app = Application('Maths Games for Outreach')
    car = Carousel(app)
    app.mainloop()


if __name__ == "__main__":
    main()
