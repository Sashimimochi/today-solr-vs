import logging
import timm
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform
import torch
import streamlit as st


class Vectorizer:
    def __init__(self) -> None:
        self.model, self.transform = self.load_model()

    @st.cache_resource
    def load_model(_self):
        logging.info(f"init Inception-V3 model...")
        model_name = "inception_v3"  # '2048dim
        model = timm.create_model(model_name, pretrained=True)
        model.eval()
        config = resolve_data_config({}, model=model)
        transform = create_transform(**config)
        logging.info(f"finish loading Inception-V3 model")
        return model, transform

    def img_vectorize(self, img):
        tensor = self.transform(img.convert("RGB")).unsqueeze(
            0
        )  # transform and add batch dimension
        with torch.no_grad():
            self.model.reset_classifier(0)
            out = self.model(tensor)
        return out
