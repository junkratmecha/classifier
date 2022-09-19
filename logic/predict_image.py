from PIL import Image
import torchvision.transforms as transforms
from models.net import Net
import torch
import torch.nn as nn
import torch.nn.functional as F

img_size = 32
n_result = 3  # 上位3つの結果を表示
labels = [
    'apple', 'aquarium_fish', 'baby', 'bear', 'beaver', 'bed', 'bee', 'beetle',
    'bicycle', 'bottle', 'bowl', 'boy', 'bridge', 'bus', 'butterfly', 'camel',
    'can', 'castle', 'caterpillar', 'cattle', 'chair', 'chimpanzee', 'clock',
    'cloud', 'cockroach', 'couch', 'crab', 'crocodile', 'cup', 'dinosaur',
    'dolphin', 'elephant', 'flatfish', 'forest', 'fox', 'girl', 'hamster',
    'house', 'kangaroo', 'keyboard', 'lamp', 'lawn_mower', 'leopard', 'lion',
    'lizard', 'lobster', 'man', 'maple_tree', 'motorcycle', 'mountain', 'mouse',
    'mushroom', 'oak_tree', 'orange', 'orchid', 'otter', 'palm_tree', 'pear',
    'pickup_truck', 'pine_tree', 'plain', 'plate', 'poppy', 'porcupine',
    'possum', 'rabbit', 'raccoon', 'ray', 'road', 'rocket', 'rose',
    'sea', 'seal', 'shark', 'shrew', 'skunk', 'skyscraper', 'snail', 'snake',
    'spider', 'squirrel', 'streetcar', 'sunflower', 'sweet_pepper', 'table',
    'tank', 'telephone', 'television', 'tiger', 'tractor', 'train', 'trout',
    'tulip', 'turtle', 'wardrobe', 'whale', 'willow_tree', 'wolf', 'woman',
    'worm'
    ]
n_class = len(labels)

def predict_image(filepath):
  image = Image.open(filepath)
  image = image.convert("RGB")
  image = image.resize((img_size, img_size))

  normalize = transforms.Normalize(
      (0.0, 0.0, 0.0), (1.0, 1.0, 1.0))  # 平均値を0、標準偏差を1に
  to_tensor = transforms.ToTensor()
  transform = transforms.Compose([to_tensor, normalize])

  x = transform(image)
  x = x.reshape(1, 3, img_size, img_size)

  # 予測
  net = Net()
  net.load_state_dict(torch.load(
      "ai/model_cnn100.pth", map_location=torch.device("cpu")))
  net.eval()  # 評価モード

  y = net(x)
  y = F.softmax(y, dim=1)[0]
  sorted_idx = torch.argsort(-y)  # 降順でソート
  result = ""
  for i in range(n_result):
      idx = sorted_idx[i].item()
      ratio = y[idx].item()
      label = labels[idx]
      result += "<p>" + str(round(ratio*100, 1)) + \
          "%の確率で" + label + "です。</p>"
  return result