#!/usr/bin/env python
# coding: utf-8

# In[2]:


import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import numpy as np
from keras.preprocessing import image


# In[3]:


train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True,
                                   validation_split=0.2)
training_set = train_datagen.flow_from_directory('cloud_dataset/cloud_training_set',
                                                 target_size = (64, 64),
                                                 batch_size = 32,
                                                 class_mode = 'categorical',
                                                subset='training')
validation_set = train_datagen.flow_from_directory('cloud_dataset/cloud_training_set',
                                                   target_size=(64, 64),
                                                   batch_size=32,
                                                   class_mode='categorical',
                                                   subset='validation')


# In[4]:


test_datagen = ImageDataGenerator(rescale = 1./255)
test_set = test_datagen.flow_from_directory('cloud_dataset/cloud_test_set',
                                            target_size = (64, 64),
                                            batch_size = 32,
                                            class_mode = 'categorical')


# In[5]:


## Building CNN Model


# In[6]:


cloud_image_model = tf.keras.models.Sequential()


# In[7]:


cloud_image_model.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu', input_shape=[64, 64, 3]))
cloud_image_model.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=1))
cloud_image_model.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu'))
cloud_image_model.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=1))
cloud_image_model.add(tf.keras.layers.Flatten())
cloud_image_model.add(tf.keras.layers.Dense(units=32, activation='relu'))
cloud_image_model.add(tf.keras.layers.Dense(units=3, activation='softmax'))
cloud_image_model.compile(loss='categorical_crossentropy', optimizer='nadam',metrics=['accuracy'])


# In[9]:


cloud_image_processor_model=cloud_image_model.fit(x = training_set, validation_data = validation_set, epochs = 15)


# In[10]:


test_accuracy = cloud_image_model.evaluate(test_set)
print(f'Test Accuracy: {test_accuracy[1]}')


# In[11]:


# Making a prediction


# In[14]:


import numpy as np
import os
from keras.preprocessing import image
path = r'C:\Users\ASUS\Desktop\cloud_dataset\prediction'
for img in os.listdir(path):
    test_image = image.load_img(os.path.join(path, img), target_size = (64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    predict = cloud_image_model.predict(test_image)
    prediction_index = np.argmax(predict, axis=1)
    if prediction_index == 0:
        prediction = "Clear"
    elif prediction_index == 1:
        prediction = "Cloudy"
    elif prediction_index == 2:
        prediction = "Rainy"
    print(img + " = " + prediction)


# In[ ]:




