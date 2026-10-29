from torchvision import datasets, transforms

to_tensor = transforms.ToTensor()
train_data = datasets.FashionMNIST(
    "data", train=True, download=True, transform=to_tensor
)
test_data = datasets.FashionMNIST(
    "data", train=False, download=True, transform=to_tensor
)

print("training images:", len(train_data))
print("test images:", len(test_data))
print("classes:", train_data.classes)

image, label = train_data[0]
print("image shape:", tuple(image.shape))
print("label:", label, "=", train_data.classes[label])
print("pixels:", image.min().item(), "to", image.max().item())
