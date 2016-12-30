''' utils.py

Utility functions for bone age prediction demo

'''

import os
from logman import bot
from PIL import Image
import sys


def get_image(image_path,warped_height=256,warped_width=256):
    '''get_image will return an image array (using import image)
    after checking that the image exists.
    :param image_path: the path to the image file
    :param warped_width: the width of the image, in pixels
    :param warped_height: the height of the image, in pixels
    '''
    image = os.path.abspath(image_path)

    # Make sure it exists
    if os.path.exists(image) == False:
        bot.logger.error("Error, cannot find %s, exiting!",image)
        sys.exit(1)

    return import_image(img_path=image, 
                        warped_height=height, 
                        warped_width=width)

def import_image(img_path, warped_height=256, warped_width=256):
    '''import image will return the ind-th image specified by 
    list img_names - uint8 array
    :param image_path: the path to the image file
    :param warped_width: the width of the image, in pixels
    :param warped_height: the height of the image, in pixels
    '''    
    # Must have ints for sizes
    warped_width = check_type(warped_width,int)
    warped_height = check_type(warped_height,int)

    # image resize is specified with width then height in PIL Image
    img_data = Image.open(img_path).resize((warped_width,warped_height))
    img_array = np.array(img_data.convert('L'))

    # In rare cases the image has three channels instead of 1
    if len(img_array.shape) > 2:
        bot.logger.info('Converting img %s to Grayscale...',imgnames[i])
        bot.logger.debug(img_array.shape)

    # Must be uint8 to continue
    if img_array.dtype != np.uint8:
        bot.logger.error("Image array data type is not uint8. Exiting.")
        sys.exit(1)

    return img_array


def select_example_image(basepath=None,start=0,end=9,extension=None):
    '''select_example_image will select an image from start to finish
    in some basepath folder. If none provided, defaults are used.
    :param basepath: the base path to select image from (default /code/example_images/
    :param start: the first image (default 0)
    :param end: the last image (default 9)
    :param extension: the extension of the image (without dot). default is png
    '''
    from random import sample
    image = None
    if basepath == None:
        basepath = '/code/example_images'

    if extension == None:
        extension = "png"
    contenders = list(range(start,end))

    # Keep going until we get an image, then return it
    while image == None:
        selection = "%s/%s.%s" %(basepath,
                                 sample(contenders,1)[0],
                                 extension)
        if os.path.exists(selection):
            image = selection

    return image


def check_type(variable,desired_type):
    '''check_type will check if a variable is a desired type. If not,
    if will convert and return the fixed variable.
    :param variable: the input to check
    :param desired_type: the desired type
    '''
    if not isinstance(variable,desired_type):
        variable = desired_type(variable)
    return variable
