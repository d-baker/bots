from PIL import Image, ImageDraw
import random

class ColorGenerator():
    def __init__(self):
        self.graymin = 1
        self.graymax = 14

        self.gothmin = 0
        self.gothmax = 1

    def gen_grayscale(self):
        colors = []
        for a in range(self.graymin, self.graymax):
            for b in range(self.graymin, self.graymax):
                for c in range(self.graymin, self.graymax):
                    for d in range(self.graymin, self.graymax):
                        colors.append("#" + 
                            str(hex(a))[2:] + 
                            str(hex(b))[2:] +
                            str(hex(a))[2:] + 
                            str(hex(c))[2:] + 
                            str(hex(a))[2:] + 
                            str(hex(d))[2:] 
                        )

        with open("everygothcolor/grayscale.txt", "w+") as fp:
            [fp.write(c + "\n") for c in colors]

    def gen_gothscale(self):
        colors = []
        for a in range(self.gothmin, self.gothmax):
            for b in range(0, 16):
                for c in range(0, 16):
                    for d in range(0, 16):
                        colors.append("#" + 
                            str(hex(a))[2:] + 
                            str(hex(b))[2:] +
                            str(hex(a))[2:] + 
                            str(hex(c))[2:] + 
                            str(hex(a))[2:] + 
                            str(hex(d))[2:] 
                        )

        with open("everygothcolor/gothscale.txt", "w+") as fp:
            [fp.write(c + "\n") for c in colors]


class ImageGenerator():
    def __init__(self, color):
        self.color = color
        self.width = 522
        self.height = 300

    def create_png(self, filepath):
        img = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(img)

        draw.rectangle( [(0,0),(self.width, self.height)], fill=self.color)

        img.save(filepath + ".png", "PNG")


def everygothcolor():
    colors = []
    with open ("everygothcolor/gothscale.txt") as fp:
        colors = list(line.strip() for line in fp.readlines())

    for color in colors:
        image = ImageGenerator(color)
        image.create_png("everygothcolor/gothscale/" + color[1:])

def everyshadeofgray():
    colors = []
    with open ("everyshadeofgray/grayscale.txt") as fp:
        colors = list(line.strip() for line in fp.readlines())

    for color in colors:
        image = ImageGenerator(color)
        image.create_png("everyshadeofgray/grayscale/" + color[1:])


if __name__ == "__main__":
    goth = ColorGenerator()
    gray = ColorGenerator()

    goth.gen_gothscale()
    gray.gen_grayscale()

    #everygothcolor()
    everyshadeofgray()
