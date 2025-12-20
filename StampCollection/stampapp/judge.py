import torch
from torchvision import models, transforms
from torchvision.models import ResNet50_Weights
from PIL import Image

# 学習済みモデル生成
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V2).to(device)
model.eval()
cos_sim = torch.nn.CosineSimilarity(dim=1, eps=1e-6)

preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
'''前処理関数'''

def get_feature(image):
    '''
    特徴量抽出関数
    
    :param image: 画像データ(ImageFile)
    '''
    image = preprocess(image)
    image = image.unsqueeze(0).to(device)
    with torch.no_grad():
        features = model(image)
    return features

def judge(base_image_path, compare_image, threshold=0.80):
    '''
    判定用関数
    
    :param base_image_path: スタンプに登録されている画像のファイルパス
    :param compare_image: formから取得した画像データ
    :param threshold: 判定閾値(default: 0.80)
    :return: True: similarity >= 0.80 | False: similarity < 0.80
    '''
    base_image = Image.open(base_image_path).convert("RGB")
    compare_image = Image.open(compare_image).convert("RGB")

    base_image_feature = get_feature(base_image)
    compare_image_feature = get_feature(compare_image)

    similarity = cos_sim(base_image_feature, compare_image_feature)
    return similarity >= threshold