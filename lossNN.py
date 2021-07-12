import torch
from torch import nn
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
import matplotlib.pyplot as plt
import pickle5 as pickle
from torch.utils import data
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import train_test_split
import numpy as np

#Data = pack[0-6]
#Predict = pack[7]

file = 'NNdata.pickle'
with open(file, 'rb') as f:
    load = pickle.load(f)

x_raw = []
y_raw= []

print(load[0][0])
print(load[0][1])
#do loss rate for prediction
# holder = []
# for i in range(len(load)):

# for packet in load:
#     x_raw.append(packet[0])
#     y_raw.append(packet[1])

#print(x_raw[:10])
#print(y_raw[:10])

# x_train, x_val, y_train, y_val = train_test_split(x_raw, y_raw, test_size=0.2, stratify=y_raw)
# np.unique(y_train, return_counts=True)
# np.unique(y_val, return_counts=True)
#
# print(len(x_train))
# print(len(y_train))

class ExampleDataset(Dataset):
     def __init__(self, data):
         self.data = data

     def __len__(self):
         return len(self.data)

     def __getitem__(self, idx):
         return self.data[idx][0], self.data[idx][1]

class NumbersDataset(Dataset):
    def __init__(self):
        self.samples = [list(range(1,1001)), list(range(2001,3001))]

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx][0]


#CNN
#convolutoinal on time

# full mixing between attributes. 8 x 3,
# for packet in x_train:
#     for element in packet:
#         if type(element) == str:
#             element = -1
#
batch_size = 1

#data = [x_train, y_train]
#train_data = ExampleDataset(data)
train_data = ExampleDataset(load)

train_dataloader = DataLoader(train_data, batch_size=batch_size)
dataused, prediction = next(iter(train_dataloader))

print(dataused)
print(prediction)

# print(len(train_data[0][0][0]))
# print(train_data[0])
# data = [x_val, y_val]
# test_data = ExampleDataset(data)

#print(train_data[0])
#x_train, x_test, y_train, y_test = train_test_split(x_raw, y_raw, test_size=0.20, shuffle = True)

#train_set, val_set, test_set = data.random_split(master, (n_train, n_val, n_test))

#
# train_data = NumbersDataset()
# # # Create data loaders.
# train_dataloader = DataLoader(train_data, batch_size=batch_size)
# print(next(iter(train_dataloader)))


# test_dataloader = DataLoader(test_data, batch_size=batch_size)
#
# print(next(iter(train_dataloader)))
# # for X, y in test_dataloader:
# #     print("Shape of X [N, C, H, W]: ", X.shape)
# #     print("Shape of y: ", y.shape)
# #     break
#
# from torch.utils.data import Dataset
#
# # Display image and label.
#train_features, train_labels = next(iter(train_dataloader))
# print(train_features)
# print(train_labels)
#
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using {} device".format(device))

# Define model
class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28*28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10),
            nn.ReLU()
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

model = NeuralNetwork().to(device)
print(model)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)

def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)

        # Compute prediction error
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch % 100 == 0:
            loss, current = loss.item(), batch * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

epochs = 5
for t in range(epochs):
    print(f"Epoch {t+1}\n-------------------------------")
    train(train_dataloader, model, loss_fn, optimizer)
    test(test_dataloader, model, loss_fn)
print("Done!")
#
#
# #[[[window, , , , , loss count]]]