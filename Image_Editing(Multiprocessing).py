from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageFilter, ImageChops, ImageFont, ImageDraw
import logging
from time import perf_counter

# Constant (good practice to keep constants right below the imports)
THUMBNAIL_SIZE = (1200, 1200)
TEXT_FONT = 'Fonts/PlayfairDisplay-BlackItalic.ttf'
# TEXT_FONT = 'Fonts/PlayfairDisplay-Italic-VariableFont_wght.ttf'
# TEXT_FONT = 'Fonts/PlayfairDisplay-VariableFont_wght.ttf'


# Setting up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s: %(name)s: %(levelname)s: %(message)s')

file_handler = logging.FileHandler('Images-Edit.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Setting up the images path to be accessed as they get edited.
with open('ImageFilteredURLs.txt', 'r+') as f:
    img_names = [line.strip('\n').split('/')[3]+'.jpg' for line in f]
    img_paths = [f'Pictures\Downloaded\{img_name}' for img_name in img_names]


def edit_image(img_path: str):
    img = Image.open(img_path)
    # Adding a filter and inverting the colors.
    img = img.filter(ImageFilter.Kernel(
        (3, 3), (-1, -1, -1, -1, 9, -1, -1, -1, -1), 1, 0))
    img = ImageChops.invert(img)
    # Adding text setup.
    text_font = ImageFont.truetype(
        TEXT_FONT, 100)
    text = "Abstract Art\nMultiprocessing Project\nFaisal Al-Rayes"
    img_text_edit = ImageDraw.Draw(img)
    img_text_edit.text((20, 20), text, (237, 0, 0), text_font)

    img.thumbnail(THUMBNAIL_SIZE)
    edited_img_name = 'edited-' + img_path.split('\\')[2]
    img_pre_edit_name = img_path.split('\\')[2]
    img.save(f'Pictures\Processed\{edited_img_name}')
    logger.debug(f'"{img_pre_edit_name}" is now edited!')


def main():
    # Set the start time.
    t1 = perf_counter()

    # Using multiprocessing to edit the pictures more efficiently.
    with ProcessPoolExecutor() as executor:
        executor.map(edit_image, img_paths)

    # Set the end time.
    t2 = perf_counter()

    # Logging the elapsed time.
    elapsed_time = round(t2 - t1, 2)
    logger.info(f'Images took {elapsed_time} sec(s) to finish editing by multiprocessing.')

if __name__ == '__main__':
    main()
