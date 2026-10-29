import torch
from torch import nn
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

torch.manual_seed(0)

full_train = datasets.FashionMNIST(
    "data", train=True, download=True, transform=transforms.ToTensor()
)
train_data, val_data = random_split(full_train, [50000, 10000])
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
val_loader = DataLoader(val_data, batch_size=256)

model = nn.Sequential(
    nn.Flatten(),
    nn.Linear(784, 128),
    nn.ReLU(),
    nn.Linear(128, 10),
)
print("parameters:", sum(p.numel() for p in model.parameters()))

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

def accuracy(loader):
    model.eval()
    correct = 0
    with torch.no_grad():
        for images, labels in loader:
            preds = model(images).argmax(dim=1)
            correct += (preds == labels).sum().item()
    return correct / len(loader.dataset)

print(f"before training: val accuracy {accuracy(val_loader):.2%}")

for epoch in range(10):
    model.train()
    total_loss = 0
    for images, labels in train_loader:
        logits = model(images)
        loss = loss_fn(logits, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    avg_loss = total_loss / len(train_loader)
    val_acc = accuracy(val_loader)
    print(f"epoch {epoch + 1:2d}  loss {avg_loss:.4f}  val accuracy {val_acc:.2%}")

torch.save(model.state_dict(), "fashion_model.pt")
print("saved fashion_model.pt")
