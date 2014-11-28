from PIL import Image, ImageDraw
import random

class ColorGenerator():
    def __init__(self, limit):
        self.limit = limit

    def gen_grayscale(self):
        colors = []
        for a in range(0, 16):
            for b in range(0, 16):
                colors.append("#" + ( str(hex(a))[2:] + str(hex(b))[2:] ) * 3)

        with open("grayscale.txt", "w+") as fp:
            [fp.write(c + "\n") for c in colors]

    def gen_gothscale(self):
        colors = []
        for x in range(0, self.limit):
            for y in range(0, self.limit):
                for z in range(0, self.limit):
                    colors.append(
                        "#" +
                        str(hex(x))[2:].zfill(2) +
                        str(hex(y))[2:].zfill(2) +
                        str(hex(z))[2:].zfill(2)
                    )

        with open("gothscale.txt", "w+") as fp:
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
    with open ("gothscale.txt") as fp:
        colors = list(line.strip() for line in fp.readlines())

    for color in colors:
        image = ImageGenerator(color)
        image.create_png("swatches/gothscale/" + color[1:])

def everyshadeofgray():
    colors = []
    with open ("grayscale.txt") as fp:
        colors = list(line.strip() for line in fp.readlines())

    for color in colors:
        image = ImageGenerator(color)
        image.create_png("swatches/grayscale/" + color[1:])

if __name__ == "__main__":
    #goth = ColorGenerator(16)
    gray = ColorGenerator(256)

    #goth.gen_gothscale()
    gray.gen_grayscale()

    #everygothcolor()
    #everyshadeofgray()
