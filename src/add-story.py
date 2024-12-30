import os
import sys
import time
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))

# -> change your default settings
DEFAULT_FONT = os.path.join(BASE, "../fonts/43-DecoType-Naskh-Variants.ttf")
QUEUE_FOLDER = os.path.join(BASE, "../queue")
DEFAULT_PIC = os.path.join(os.path.expanduser("~"), "Pictures/grey_bg.jpg")
DEFAULT_CAP = "This is not me, l Bot rah ytelef wahdo. DM if you see this story"
MAX_LINES = 19

class MaxLinesException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

# building the story picture
def build_story_picture(bg_path=DEFAULT_PIC, caption=DEFAULT_CAP, output="story"):
    # load the background image
    image = Image.open(bg_path)

    # create a drawing object to draw on the image
    draw = ImageDraw.Draw(image)

    # define the font and size (you can specify the path to a TTF font file if needed)
    font_size = 65
    font = ImageFont.truetype(DEFAULT_FONT, font_size)

    # define the text to add and position
    text_color = (0, 0, 0)  # White color (use RGB values)

    # the size of the image
    image_size = image.size

    # add the text to the image
    draw_text_with_wrapping_centered(draw, caption, font, image_size, text_color)

    # save the edited image
    output_image_path = f"{QUEUE_FOLDER}/{output}"
    image.save(output_image_path)

    return output_image_path


def draw_text_with_wrapping_centered(draw, text, font, image_size, fill):
    # split the text into words
    words = text.split(' ')
    
    # initialize variables for handling lines of text
    lines = []
    current_line = ""
    # add margin (100 px)
    max_width = image_size[0] - 100  

    # iterate over the words and construct lines
    for word in words:
        test_line = current_line + word + " "
        # use textbbox to get the bounding box of the text
        text_bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        
        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    
    if current_line:
        lines.append(current_line)

    # verify if the number of lines exceeded the max
    if len(lines) > MAX_LINES:
        raise MaxLinesException(f"The number of lines exceeded the max: {MAX_LINES}")
        

    # calculate total height of the text block
    text_block_height = sum([font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines])
    
    # calculate the Y position to center the text vertically
    y_offset = (image_size[1] - text_block_height) // 2

    # draw each line, centering it horizontally
    for line in lines:
        text_bbox = draw.textbbox((0, 0), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x_offset = (image_size[0] - text_width) // 2  
        draw.text((x_offset, y_offset), line, font=font, fill=fill)
        y_offset += text_height

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("[!] Usage: add-story.py story1 [story2] [story3] ...")
        exit(0)
    # check if output directory exists
    if not os.path.exists(QUEUE_FOLDER):
        try:
            os.makedirs(QUEUE_FOLDER, exist_ok=False)
        except OSError as e:
            print("[!] Error while creating directory")
            exit(-1)
    # stories will by named using timestamp
    ts = int(time.time())
    for i in range(len(sys.argv) - 1):
        # adding caption to the background image
        try:
            build_story_picture(caption=sys.argv[i+1], output=f"{str(ts)}-{str(i)}.jpg")
        except MaxLinesException as e:
            print(f"[!] Exception: {e}")
            exit(-1)