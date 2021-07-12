from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Conv2D
from keras.layers import Flatten
from keras.layers import Reshape
from keras.layers import MaxPooling2D
from keras.layers import Dropout
from keras.metrics import MeanSquaredError
import pickle5 as pickle
from sklearn.model_selection import train_test_split
import numpy as np

file = 'NNdata.pickle'
with open(file, 'rb') as f:
    load = pickle.load(f)

x_raw = []
y_raw= []

#print(load[0][0])
#print(load[0][1])
print(len(load))
for packet in load:
    x_raw.append(packet[0])
    y_raw.append(packet[1])

#print(x_raw[:10])
#print(y_raw[:10])
#print(len(x_raw[0][0]))

x_train, x_val, y_train, y_val = train_test_split(x_raw, y_raw, test_size=0.2, stratify=y_raw)
#np.unique(y_train, return_counts=True)
#np.unique(y_val, return_counts=True)
print(len(x_val))
print(len(y_val))


print(len(x_train))
print(len(y_train))
print(x_train[0])
#normalize?
#x_train = np.expand_dims(x_train, axis=-1)

batch_size = 64

#[20[8]]
input_shape = (20,9,1)
model = Sequential()
model.add(Reshape(input_shape))
model.add(Dropout(0.2))
model.add(Conv2D(256, (3,9), 1, activation='relu', input_shape=input_shape))
#model.add(MaxPooling2D(pool_size=(2, 1)))
model.add(Conv2D(128, (2,1), 1, activation='relu'))
#model.add(MaxPooling2D(pool_size=(2, 1)))
model.add(Conv2D(64, (2,1),1, activation='relu'))
#model.add(Conv2D(64, (2,1), activation='relu'))
model.add(Conv2D(32, (2,1),1, activation='relu'))
model.add(Flatten())
model.add(Dense(1, activation='softmax'))

#model = Sequential()
#model.add(Dense(12, input_dim=8, activation='relu'))
#model.add(Dense(8, activation='relu'))
#model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy', MeanSquaredError()])

model.fit(x_train, y_train, epochs=10, batch_size=batch_size)
_, accuracy, _ = model.evaluate(x_val, y_val)
print('Accuracy: %.2f' % (accuracy*100))

model.summary()


