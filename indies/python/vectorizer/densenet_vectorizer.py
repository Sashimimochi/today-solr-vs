import timm
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform
import torch

class Vectorizer:
    def __init__(self) -> None:
        model_name = 'densenet121' # 'densenet121' 1024dim # 'resnet18' 512dim
        self.model = timm.create_model(model_name, pretrained=True)
        self.model.eval()
        config = resolve_data_config({}, model=self.model)
        self.transform = create_transform(**config)

    def img_vectorize(self, img):
        tensor = self.transform(img.convert('RGB')).unsqueeze(0) # transform and add batch dimension
        with torch.no_grad():
            self.model.reset_classifier(0)
            out = self.model(tensor)
        return out
