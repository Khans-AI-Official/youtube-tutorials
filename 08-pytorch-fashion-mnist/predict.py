import torch
from torch import nn
from torchvision import datasets, transforms

test_data = datasets.FashionMNIST(
    "data", train=False, download=True, transform=transforms.ToTensor()
)
classes = test_data.classes

model = nn.Sequential(
    nn.Flatten(), nn.Linear(784, 128), nn.ReLU(), nn.Linear(128, 10)
)
model.load_state_dict(torch.load("fashion_model.pt"))
model.eval()

for i in [0, 1, 2, 4, 6, 9, 12, 40]:
    image, label = test_data[i]
    with torch.no_grad():
        scores = model(image.unsqueeze(0))
    probs = torch.softmax(scores, dim=1)[0]
    conf, pred = probs.max(dim=0)
    mark = "ok" if pred == label else "WRONG"
    guess, true = classes[pred], classes[label]
    print(f"image {i:2d}: {guess:12s} {conf:4.0%}   true: {true:12s} {mark}")
