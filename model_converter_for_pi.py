##################################################################################################################################

# Project:      Weather Station Project
# File Name:    model_converter_for_pi.py

# Author:       Priyanshu Bhateja
# Purpose:      A program that converts the machine learning model into .tflite format for compatibility with Raspberry Pi.
# Description:  The program converts the CNN model into .tflite format which is used by the Raspberry Pi as the database for 
#               classifying sky conditions into clear, cloudy, and rainy.
# Date Edited:  2023/11/20

##################################################################################################################################

# Imports
import tensorflow as tf

##################################################################################################################################

# Classes
class ModelConverter:
    """ The class handles the conversion of Keras models to TensorFlow Lite format for Raspberry Pi """

    def __init__(self, keras_model_path, tflite_model_path):
        """
        Contructor method to initializes the converter with paths for the Keras model and the TFLite model.
        Arguments:  self
                    keras_model_path (str): Path to the Keras model file.
                    tflite_model_path (str): Path where the TFLite model will be saved.
        
        """
        self.keras_model_path = keras_model_path
        self.tflite_model_path = tflite_model_path

    def load_model(self):
        """
        Method to load a Keras model from the specified path
        Arguments:  self

        """
        self.model = tf.keras.models.load_model(self.keras_model_path)
        print("Keras model loaded successfully.")

    def convert_to_tflite(self):
        """
        Method to convert the loaded Keras model to TensorFlow Lite format
        Arguments:  self
        
        """
        converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
        self.tflite_model = converter.convert()
        print("Model converted to TFLite format.")

    def save_tflite_model(self):
        """
        Method to save the converted TFLite model to the specified path
        Arguments:  self
        
        """
        with open(self.tflite_model_path, 'wb') as f:
            f.write(self.tflite_model)
        print(f"TFLite model saved to {self.tflite_model_path}")


# Usage
keras_model_path = r'C:\Users\ASUS\Desktop\cloud_image_model.h5'        # Load the path for .h5 model
tflite_model_path = r'C:\Users\ASUS\Desktop\cloud_image_model.tflite'   # Specify path name to save the .tflite model

converter = ModelConverter(keras_model_path, tflite_model_path)
converter.load_model()
converter.convert_to_tflite()
converter.save_tflite_model()


######################################################## End of code #############################################################