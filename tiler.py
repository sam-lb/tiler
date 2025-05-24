from PIL import Image


def min_threshold(i):
    x = i - 192 >= 0
    return i * x

def max_threshold(i):
    x = i - 100 < 0
    return i * x


IMAGE_FILE = "./test_images/blue_bird.jpg"
im = Image.open(IMAGE_FILE)
print(im.format, im.size, im.mode)

box = (128, 128, 256, 256)
region = im.crop(box)
region = region.transpose(Image.Transpose.ROTATE_180)
im.paste(region, box)
im = im.point(max_threshold)

im.show()