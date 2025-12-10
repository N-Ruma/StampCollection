import torch
from torchvision.models import ResNet50_Weights
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1).to(device)
model.eval()
cos_sim = torch.nn.CosineSimilarity(dim=1, eps=1e-6)

# Define the image preprocessing steps
preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5],
                             std=[0.5, 0.5, 0.5])
])

def getFeature(IMG_PATH):
    image = Image.open(IMG_PATH)
    image = preprocess(image)
    image = image.unsqueeze(0).to(device)
    with torch.no_grad():
        features = model(image)
    return features

def calculate_similarity(img1_path, img2_path):

    f1 = getFeature(img1_path)
    f2 = getFeature(img2_path)

    score = cos_sim(f1, f2).item()
    return score