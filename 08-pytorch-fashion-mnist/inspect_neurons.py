import torch
from torchvision import datasets, transforms

train_data = datasets.FashionMNIST(
    "data", train=True, download=True, transform=transforms.ToTensor()
)
weights = torch.load("fashion_model.pt")
W, b = weights["1.weight"], weights["1.bias"]

images = torch.stack([image for image, label in train_data]).view(-1, 784)
hidden = images @ W.T + b
active = (hidden > 0).float().mean(dim=0)

dead = (active == 0).nonzero().flatten().tolist()
print("hidden neurons:", len(active))
print("never active:", len(dead))
print("dead neurons:", dead)
