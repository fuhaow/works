import torch
from torch.autograd import Variable
import torch.nn as nn
import random
# [coffee, time of doing sports (hours), awake time (hours), playing with cellphone before sleep(hours)]

x = torch.tensor([
    [1.0, 0.5, 15.0, 2.0],
    [1.0, 0.2, 15.0, 0.5],
    [0, 0.2, 12.0, 0.5]
])
y = torch.tensor([
    [10.0],
    [10.0],
    [8.0]
])


class Mynet(nn.Module):
    def __init__(self):
        super(Mynet, self).__init__()
        self.fc = nn.Sequential(

            nn.Linear(4, 100),
            nn.ReLU(),
            nn.Linear(100, 50),
            nn.ReLU(),
            nn.Linear(50, 60),
            nn.ReLU(),
            nn.Linear(60, 1)

        )
        self.opt = torch.optim.Adam(self.parameters())
        self.mls = torch.nn.MSELoss()
    def forward(self, imput):
        return self.fc(imput)

    def training_model(self, x, y):
        out = self.forward(x)
        loss = self.mls(out, y)
        print(loss)
        self.opt.zero_grad()
        loss.backward()
        self.opt.step()


    def test(self, x):
        return self.forward(x)
net = Mynet()
for i in range(1000):
    net.training_model(x, y)
out = net.test(torch.Tensor([[0.0, 0.5, 15.0, 0.5]]))
print(out)