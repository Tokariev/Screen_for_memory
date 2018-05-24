from PIL import Image
import os, sys
import pyscreenshot as ImageGrab

im = ImageGrab.grab(childprocess=False)
im.save('big.jpeg')


size = 500, 333

try:
    im.thumbnail(size, Image.ANTIALIAS)
    im.save("small.jpeg")
except IOError:
    print ("Cannot create small image")