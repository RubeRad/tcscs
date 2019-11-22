#! /usr/bin/env python3

import random
import os
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

def plot_image(i, predictions_array, true_label, img):
  predictions_array, true_label, img = predictions_array, true_label[i], img[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])

  plt.imshow(img, cmap=plt.cm.binary)

  predicted_label = np.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'

  plt.xlabel("test {} {:2.0f}% ({})".format(i,
                                100*np.max(predictions_array),
                                class_names[true_label]),
                                color=color)

def plot_value_array(i, predictions_array, true_label):
  predictions_array, true_label = predictions_array, true_label[i]
  plt.grid(False)
  plt.xticks(range(10))
  plt.yticks([])
  thisplot = plt.bar(range(10), predictions_array, color="#777777")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)

  thisplot[predicted_label].set_color('red')
  thisplot[true_label].set_color('blue')




print('tensorflow version is', tf.__version__)

# the module gives easy access to the test data
# first run this will download to a local file
# subsequent runs it will be much quicker
fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

#number_mnist = keras.datasets.mnist
#(train_images, train_labels), (test_images, test_labels) =  number_mnist.load_data()
#class_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# see what the data looks like
show_data = False
if show_data:
   plt.figure(figsize=(10,10))
   for i in range(25):
       plt.subplot(5,5,i+1)
       plt.xticks([])
       plt.yticks([])
       plt.grid(False)
       plt.imshow(train_images[i], cmap=plt.cm.binary)
       plt.xlabel(class_names[train_labels[i]])
   plt.show()

train_images = train_images / 255.0
test_images  = test_images  / 255.0

if os.path.exists('model.json') and os.path.exists('model.h5'):
   with open('model.json') as file:
      json = file.read()
   model = keras.models.model_from_json(json)
   model.load_weights('model.h5')
   print('loaded model from disk')

   model.compile(optimizer='adam',
                 loss='sparse_categorical_crossentropy',
                 metrics=['accuracy'])
else:
   model = keras.Sequential([
       keras.layers.Flatten(input_shape=(28, 28)),
       keras.layers.Dense(128, activation='relu'),
       keras.layers.Dense(10, activation='softmax')
   ])

   model.compile(optimizer='adam',
                 loss='sparse_categorical_crossentropy',
                 metrics=['accuracy'])

   # this is the training step that takes all the time
   model.fit(train_images, train_labels, epochs=10)

   with open('model.json', 'w') as file:
      file.write(model.to_json())
   model.save_weights('model.h5')
   print('saved model to files model.json and model.h5')

# either way now we have a model with weights


test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
print('\nTest loss:    ', test_loss)
print('Test accuracy:', test_acc)


# this applies the model to all the test images
predictions = model.predict(test_images)


num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for ii in range(num_images):
  i = random.randint(0,len(test_images))
  plt.subplot(num_rows, 2*num_cols, 2*ii+1)
  plot_image(i, predictions[i], test_labels, test_images)
  plt.subplot(num_rows, 2*num_cols, 2*ii+2)
  plot_value_array(i, predictions[i], test_labels)
plt.tight_layout()
plt.show()





