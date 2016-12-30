from resnet import Resnet50
import numpy as np
import cv2

# Add enhanced coloring clahe at each of the three channels
def clahe_augment(img):
    clahe_low = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8,8))
    clahe_medium = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    clahe_high = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8,8))
    img_low = clahe_low.apply(img)
    img_medium = clahe_medium.apply(img)
    img_high = clahe_high.apply(img)
    augmented_img = np.array([img_low, img_medium, img_high])
    augmented_img = np.swapaxes(augmented_img,0,1)
    augmented_img = np.swapaxes(augmented_img,1,2)
    return augmented_img

    
class Model:

    def __init__(self):
        checkpoint_path = 'data/bone-age-checkpoint.ckpt-19999'
        self.model = Resnet50(checkpoint_path)


    def get_result(self, image_path, image, is_male, include_scores=False):
        '''get_result will return a json structure with the image, gender,
        max score, and prediction, intended for saving to file.

        Args:
            image : numpy array to be downsized and processed
            image_path : the path to the image for the image array
            is_male : boolean indicating whether or not image of male patient
        Return:
            result: json object with scores, image, and gender
        '''
        scores = self.get_scores(image=image,is_male=is_male)
        weighted_prediction = self.calc_weighted_prediction(scores)

        gender = "M"
        if is_male == False:
            gender = "F"

        result = {'image':image_path,
                  'predicted_age':np.argmax(scores),
                  'predicted_weight':weighted_prediction,
                  'gender':gender}        

        if include_scores == True:
            result['scores'] = scores

        return result

    def get_scores(self, image, is_male):
        '''get_scores
        Returns the prediction scores after running the image through the model
        
        Args:
            image : numpy array to be downsized and processed
            is_male : boolean indicating whether or not image of male patient
        Return:
            scores : array of scores corresponding to probability of each month
        '''
        image = clahe_augment(image)
        return self.model.predict(image, is_male)


    def calc_weighted_prediction(self, scores):
        '''calc_weighted_prediction 
        Returns the weighted prediction based on input scores

        Args:
            scores : array of scores corresponding to probability of each month
        Return:
            weighted_pred : float of weighted prediction based on scores
        '''

        result = np.arange(len(scores)) * scores
        return np.sum(result)

if __name__ == '__main__':
    from utils import select_example_image
    # Note - I currently force image 5, since we know is male
    image = select_example_image(start=5,end=6)
    image = import_image(image, 256, 256)
    model = Model()
    scores =  model.get_scores(image, is_male=True)
    print('Predicted Age : %d Months' % np.argmax(scores))
    print('Weighted Prediction : %f Months' % model.calc_weighted_prediction(scores))
