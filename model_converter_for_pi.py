#*********************************************************************************************************************************
# Project: Weather Station Project
# 
# Author: Priyanshu Bhateja
# Date Edited: 20-11-2023
# File Name: model_converter_for_pi.py
# 
# Purpose: A program that converts the machine learning model into .tflite format for compatibility with Raspberry Pi.
# Description: The program converts the CNN model into .tflite format which is used by the Raspberry Pi as the database for 
#              classifying sky conditions into clear, cloudy, and rainy.
#*********************************************************************************************************************************
#*********************************************************************************************************************************
"""
Importing external libraries

"""
import tensorflow as tf


class ModelConverter:
    """
    Class Definition: Cloud Image Classifier
    The class handles the conversion of Keras models to TensorFlow Lite format for Raspberry Pi
    """

    def __init__(self, keras_model_path, tflite_model_path):
        """
        Contructor (__init__) : Initialize the converter with paths for the Keras model and the TFLite model.
        Arguments:
        self
        keras_model_path (str): Path to the Keras model file.
        tflite_model_path (str): Path where the TFLite model will be saved.
        Access: Public
        """
        self.keras_model_path = keras_model_path
        self.tflite_model_path = tflite_model_path

    def load_model(self):
        """
        Method: load_model
        Load a Keras model from the specified path
        Arguments: self
        Access: Public
        """
        self.model = tf.keras.models.load_model(self.keras_model_path)
        print("Keras model loaded successfully.")

    def convert_to_tflite(self):
        """
        Method: convert_to_tflite
        Convert the loaded Keras model to TensorFlow Lite format
        Arguments: self
        Access: Public
        """
        converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
        self.tflite_model = converter.convert()
        print("Model converted to TFLite format.")

    def save_tflite_model(self):
        """
        Method: save_tflite_model
        Save the converted TFLite model to the specified path
        Arguments: self
        Access: Public
        """
        with open(self.tflite_model_path, 'wb') as f:
            f.write(self.tflite_model)
        print(f"TFLite model saved to {self.tflite_model_path}")

# Usage
keras_model_path = r'C:\Users\ASUS\Desktop\cloud_image_model.h5'
tflite_model_path = r'C:\Users\ASUS\Desktop\cloud_image_model.tflite'

converter = ModelConverter(keras_model_path, tflite_model_path)
converter.load_model()
converter.convert_to_tflite()
converter.save_tflite_model()