
import os
os.system("pip install pillow")

from PIL import Image

def to_ansi(image, scale_factor = 10, width = None, height = None):

    scale_factor = round(scale_factor)
    chars = []
    
    img = Image.open(image)
    WIDTH, HEIGHT = img.size
    if not (width or height): # both width and height are None
        img.thumbnail((WIDTH / scale_factor, HEIGHT / scale_factor)) # scale down
    elif not width: # width not None
        img.thumbnail(width, HEIGHT)
    elif not height: # height not None
        img.thumnail(WIDTH, height)

    char_vals = list(img.getdata()) # sequence of color codes of "pixels", flattened
    char_vals = [(v, v, v) if isinstance(v, int) else v for v in char_vals] # turns any single values into tuples 
    
    for i in range(len(char_vals)):
        pv = char_vals[i]
        chars += ["\x1b[38;2;" + str(pv[0]) + ";" + str(pv[1]) + ";" + str(pv[2]) + "m" + "@@"] # add a "@@" for every pixel, colored with ANSI escape codes

    WIDTH = img.size[0] # update WIDTH (after thumbnail resizing)
    chars_rows = []
    for i in range(0, len(chars), WIDTH): # rows of WIDTH elements separated by newlines
        chars_rows += chars[i:i+WIDTH] + ["\n"]

    colored_ats = "".join(chars_rows)
    return colored_ats

print(to_ansi("images/lain_bear.jpg", 10))

# f = open("output/output.txt", "w")
# f.write(to_ansi("images/lain_bear.jpg", 10))
# f.close()