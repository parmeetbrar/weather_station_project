#*********************************************************************************************************************************
# Project: Weather Station Project
# 
# Author: Priyanshu Bhateja
# Date Edited: 20-11-2023
# File Name: cloud_image_processor.py
# 
# Purpose: A Convolutional Neural Network Model built as a machine learning model to identify sky conditions. 
# Description: The model uses CNN machine learning method to determine whether the sky is clear, cloudy or rainy.
#*********************************************************************************************************************************
#*********************************************************************************************************************************
"""
Importing external libraries

"""
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
from keras.preprocessing import image
import os

#*********************************************************************************************************************************

class CloudImageClassifier:
    """ 
    Class Definition: Cloud Image Classifier
    A class which handles processing and classifying of cloud images.

    """    
    def __init__(self, train_dir, test_dir, prediction_dir, model_save_path):
        """
        Contructor (__init__) : Initializes the classifier model with directory paths and model save paths
        Arguments: self, train_dir, test_dir, prediction_dir, model_save_path
        Access: Public      
        """    
        self.train_dir = train_dir
        self.test_dir = test_dir
        self.prediction_dir = prediction_dir
        self.model_save_path = model_save_path
        self.model = None

    def preprocess_data(self):
        """
        Method: preprocess_data
        Method to upload the data into training and testing sets with augmentation and splitting
        Arguments: self
        Access: Public

        """
        # Data augmentation and split for training and validation sets
        train_datagen = ImageDataGenerator(rescale=1./255,
                                           shear_range=0.2,
                                           zoom_range=0.2,
                                           horizontal_flip=True,
                                           validation_split=0.2)
        self.training_set = train_datagen.flow_from_directory(
            self.train_dir,
            target_size=(64, 64),
            batch_size=32,
            class_mode='categorical',
            subset='training')
        self.validation_set = train_datagen.flow_from_directory(
            self.train_dir,
            target_size=(64, 64),
            batch_size=32,
            class_mode='categorical',
            subset='validation')
        # Preparing test data with rescaling
        test_datagen = ImageDataGenerator(rescale=1./255)
        self.test_set = test_datagen.flow_from_directory(
            self.test_dir,
            target_size=(64, 64),
            batch_size=32,
            class_mode='categorical')
        
        
    def cnn_model(self):
        """
        Method: cnn_model
        Method to create and compile the CNN model for sky conditions classification
        Arguments: self
        Access: Public
        """
        # Initialising
        cloud_image_model = tf.keras.models.Sequential()
        # Adding input, convolutional, pooling anf dense layers
        cloud_image_model.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu', input_shape=[64, 64, 3]))
        cloud_image_model.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=1))
        cloud_image_model.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu'))
        cloud_image_model.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=1))
        cloud_image_model.add(tf.keras.layers.Flatten())
        cloud_image_model.add(tf.keras.layers.Dense(units=32, activation='relu'))
        cloud_image_model.add(tf.keras.layers.Dense(units=3, activation='softmax'))
        # Compiling the model with loss function, optimizer, and metrics
        cloud_image_model.compile(loss='categorical_crossentropy', optimizer='nadam',metrics=['accuracy'])

    def train_model(self, epochs=15):
        """
        Method: train_model
        Method to train the CNN model with specified number of epochs)
        Arguments: self, epochs=15
        epochs=15: Number of times the model will run and train itself
        Access: Public
        """
        self.model.fit(x=self.training_set, validation_data=self.validation_set, epochs=epochs)

    def evaluate_model(self):
        """
        Method: evaluate_model
        Method to evaluate and display model performance based on the test set
        Arguments: self
        Access: Public
        """
        test_accuracy = self.model.evaluate(self.test_set)
        print(f'Test Accuracy: {test_accuracy[1]}')


    def predict(self):
        """
        Method: predict
        Method to predict sky conditions using new images
        Arguments: self
        Access: Public
        """
        for img in os.listdir(self.prediction_dir):
            # Load and preprocess the image
            test_image = image.load_img(os.path.join(self.prediction_dir, img), target_size=(64, 64))
            test_image = image.img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis=0)
            # Making a prediction
            predict = self.model.predict(test_image)
            prediction_index = np.argmax(predict, axis=1)
            # Mapping prediction index to category
            categories = ["Clear", "Cloudy", "Rainy"]
            prediction = categories[prediction_index[0]]
            print(f'{img} = {prediction}')

    def save_model(self):
        """
        Method: save_model
        Saves the trained model to a specified path in .h5 format
        Arguments: self
        Access: Public
        """        
        self.model.save(self.model_save_path)

#*********************************************************************************************************************************

# Using the class
classifier = CloudImageClassifier(
    train_dir=r'D:\UBC Term 1\MECH 524\Assignments\weather_station_files\cloud_dataset\cloud_training_set',
    test_dir=r'D:\UBC Term 1\MECH 524\Assignments\weather_station_files\cloud_dataset\cloud_test_set',
    prediction_dir=r'D:\UBC Term 1\MECH 524\Assignments\weather_station_files\cloud_dataset\prediction',
    model_save_path=r'C:\Users\ASUS\Desktop\cloud_image_model.h5'
)
classifier.preprocess_data()
classifier.create_model()
classifier.train_model()
classifier.evaluate_model()
classifier.predict()
classifier.save_model()

#*********************************************************************************************************************************