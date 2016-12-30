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

    parser.add_argument("--output", 
                        dest='output', 
                        help="Path to output file to write results.", 
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
                        help="warped width to resize the image in pixels (default 256)", 
                        type=int,
                        default=256)

    parser.add_argument("--height", 
                        dest='height', 
                        help="warped height to resize the image in pixels (default 256)", 
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
    from utils import get_image, write_json
    print("\n*** Starting Bone Age Prediction ****")

    # Get the gender
    is_male = True
    if args.gender == "F":
        is_male = False

    # If the user has not provided an image, use an example
    image = args.image
    if image == None:
        print("No image selected, will use provided example...")
        from utils import select_example_image
        image = select_example_image(start=0,end=9)
        is_male = True # all examples male

    # Print parameters for user
    bot.logger.debug("is_male: %s", is_male)
    bot.logger.debug("image: %s", image)
    bot.logger.debug("height: %s", args.height)
    bot.logger.debug("width: %s", args.width)

    # Get the array of data (uint8) - H/W should be set to 256
    image = get_image(image_path=image,
                      warped_height=args.height,
                      warped_width=args.width)

    print("Building model, please wait.")
    model = Model()
    result = model.get_result(image,is_male=is_male)

    print('Predicted Age : %d Months' %result['predicted_age'])
    print('Weighted Prediction : %f Months' %result['predicted_weight'])

    if args.output != None:
        output = write_json(json_object=result,
                            filename=args.output)        
        bot.logger.debug('Result written to %s',args.output)

if __name__ == '__main__':
    main()
