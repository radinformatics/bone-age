#!/usr/bin/env python3

import argparse
from glob import glob
import pickle
import os
import sys

def get_parser():

    parser = argparse.ArgumentParser(description="Predict bone age of an image.")

    parser.add_argument("--image", 
                        dest='image', 
                        help="Path to single bone image.", 
                        type=str,
                        default=None)

    parser.add_argument("--folder", 
                        dest='folder', 
                        help="Path to folder of images to parse.", 
                        type=str,
                        default=None)


    parser.add_argument("--gender", 
                        dest='gender', 
                        help="the gender of the individual (M or F), default is M (male)", 
                        type=str,
                        choices=["M","F"],
                        default="M")

    parser.add_argument("--width", 
                        dest='width', 
                        help="width of the image in pixels (default 256)", 
                        type=int,
                        default=256)

    parser.add_argument("--height", 
                        dest='height', 
                        help="height of the image in pixels (default 256)", 
                        type=int,
                        default=256)

    # Does the user want to have verbose logging?
    parser.add_argument('--debug', dest="debug", 
                        help="use verbose logging to debug.", 
                        default=False, action='store_true')

    return parser



def main():
    parser = get_parser()
    
    try:
        args = parser.parse_args()
    except:
        sys.exit(0)

    # if environment logging variable not set, make silent
    if args.debug == False:
        os.environ['MESSAGELEVEL'] = "CRITICAL"

    # Tell the user what is going to be used, in case is incorrect
    from logman import bot
    from predict_image import Model
    bot.logger.info("\n***STARTING BONE AGE PREDICTION****")

    # If the user has not provided an image, use an example
    image = args.image
    if image == None:
        from utils import select_example_image
        image = select_example_image(start=0,end=9)

    # Get the array of data (uint8)
    image = get_image(image_path=image,
                      warped_height=args.height,
                      warped_width=args.width)

    is_male = True
    if args.gender == "F":
        is_male = False

    model = Model()
    scores = model.get_scores(image,is_male=is_male)

    print('Predicted Age : %d Months' % np.argmax(scores))
    print('Weighted Prediction : %f Months' % model.calc_weighted_prediction(scores))

if __name__ == '__main__':
    main()
