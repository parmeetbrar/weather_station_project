##################################################################################################################################

# Project:      Weather Station Project
# File Name:    cnn_model_for_pi.py

# Author:       Priyanshu Bhateja
# Purpose:      A program that runs the CNN model that is compatible with Raspberry Pi
# Description:  The program allows the Raspberry Pi to run the CNN model in full compatibility, and allows the model to predict sky 
#               conditions
# Date Edited:  28-11-2023

##################################################################################################################################

# Imports
import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image
import os

##################################################################################################################################

# Classes
class RaspiPredictor:
    """ A class for loading a TensorFlow Lite model and performing image predictions """

    def __init__(self, model_path):
        """
        Contructor: Initializes the predictor with the TensorFlow Lite model path.
        Arguments:  self
                    model_path (str): Path to the TensorFlow Lite model file.

        """

        # Load TFLite model and allocate tensors
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        # Get input and output tensor details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def load_image(self, img_path, target_size=(64, 64)):
        """
        Method:     Load and process an image from a given path.
        Arguments:  self
                    img_path (str): Path to the image file.
                    target_size (tuple): Target size to resize the image.
        Returns:    numpy.ndarray: Processed image array.

        """

        img = Image.open(img_path)
        img = img.resize(target_size)
        img = np.array(img)
        # Convert grayscale images to 3 channels
        if img.ndim == 2:
            img = np.stack((img,)*3, axis=-1)
        return img

    def predict_image(self, img_path):
        """
        Method:     Predict the class of an image using the loaded TensorFlow Lite model.
        Arguments:  self
                    img_path (str): Path to the image file.
        Returns:    str: Predicted category of the image.

        """

        test_image = self.load_image(img_path)
        test_image = np.expand_dims(test_image, axis=0)
        test_image = test_image.astype('float32') / 255.0

        # Set the input tensor and invoke the interpreter
        self.interpreter.set_tensor(self.input_details[0]['index'], test_image)
        self.interpreter.invoke()

        # Get the prediction results
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        prediction_index = np.argmax(output_data[0])

        # Map the prediction index to the corresponding class
        categories = ["Clear", "Cloudy", "Rainy"]
        return categories[prediction_index]

    def predict_images_in_directory(self, directory_path):
        """
        Method:     Predict the classes of all images in a specified directory.

        Arguments:  self
                    directory_path (str): Path to the directory containing images.

        """
        for img in os.listdir(directory_path):
            prediction = self.predict_image(os.path.join(directory_path, img))
            print(f'{img} = {prediction}')

##################################################################################################################################

# Usage
model_path = '/home/Pi/Desktop/cloud_image_model.tflite'
predictor = RaspiPredictor(model_path)

# Predicting images in a directory
path = '/home/Pi/Pictures/data_for_pi/prediction'
predictor.predict_images_in_directory(path)

##################################################################################################################################
######################################################## End of code #############################################################