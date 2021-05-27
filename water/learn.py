import os

import cv2
import numpy as np
import tensorflow as tf

from tensorflow.keras import layers, models, datasets
import matplotlib.pyplot as plt

images = []
labels = []
for root, dirs, files in os.walk(r"make"):
    for f in files:
        d = root + '\\' + f
        img = cv2.imdecode(np.fromfile(d, dtype=np.uint8), -1) / 255
        img = img.reshape((img.shape[0], img.shape[1], 1))
        # print(img)
        images.append(img)
        labels.append(float(f.split("_")[0]))

images = np.array(images)
labels = np.array(labels)

model = models.Sequential()
model.add(layers.Conv2D(8, (3, 3), activation='relu', input_shape=(150, 10, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(8, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(1))

model.summary()

model.compile(loss="mean_squared_error", optimizer="adam", metrics=["mean_squared_error"])

history = model.fit(images, labels, batch_size=3, epochs=1000, verbose=1, validation_split=0.2)

model.save(r"model/model")

# plt.plot(history.history['accuracy'], label='accuracy')
# plt.plot(history.history['val_accuracy'], label='val_accuracy')
# plt.xlabel('Epoch')
# plt.ylabel('Accuracy')
# plt.ylim([0.5, 1])
# plt.legend(loc='lower right')
# plt.show()

test_loss = model.evaluate(images, labels, batch_size=3, verbose=1)

print(test_loss)
