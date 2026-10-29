import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

test_data = datasets.FashionMNIST(
    "data", train=False, download=True, transform=transforms.ToTensor()
)
test_loader = DataLoader(test_data, batch_size=256)
classes = test_data.classes

model = nn.Sequential(
    nn.Flatten(), nn.Linear(784, 128), nn.ReLU(), nn.Linear(128, 10)
)
model.load_state_dict(torch.load("fashion_model.pt"))
model.eval()

confusion = torch.zeros(10, 10, dtype=torch.long)
with torch.no_grad():
    for images, labels in test_loader:
        preds = model(images).argmax(dim=1)
        for true, pred in zip(labels, preds):
            confusion[true, pred] += 1

total_right = confusion.trace().item()
print(f"test accuracy: {total_right / len(test_data):.2%}")
print()
for i, name in enumerate(classes):
    print(f"{name:12s} {confusion[i, i] / confusion[i].sum():.1%}")

print()
mistakes = confusion.clone()
mistakes.fill_diagonal_(0)
for _ in range(3):
    true, pred = divmod(mistakes.argmax().item(), 10)
    count = mistakes[true, pred].item()
    print(f"{count} {classes[true]} predicted as {classes[pred]}")
    mistakes[true, pred] = 0
