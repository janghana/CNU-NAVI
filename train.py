import torch.optim as optim
import torch
from torch import nn

transform = transforms.Compose([
    transforms.Resize((32, 128)),
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
])

dataset = TimetableDataset(annotations_file='/path/to/timetable_ground_truth.csv',
                           img_dir='/path/to/datasets',
                           transform=transform)

dataloader = DataLoader(dataset, batch_size=4, shuffle=True, num_workers=4)

model = CRNN(num_classes=100)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(num_epochs):
    for images, labels in dataloader:
        outputs = model(images)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {loss.item():.4f}')


torch.save(model.state_dict(), 'model_path.pth')

model = CRNN(num_classes=100)
model.load_state_dict(torch.load('model_path.pth'))
model.eval()
