import logging
import streamlit as st
import torch
import japanese_clip as ja_clip


class Vectorizer:
    def __init__(self) -> None:
        logging.info(f"init clip model...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess, self.tokenizer = self.load_model()

    @st.cache_resource
    def load_model(_self):
        model, preprocess = ja_clip.load(
            "rinna/japanese-cloob-vit-b-16", device=_self.device
        )
        tokenizer = ja_clip.load_tokenizer()
        logging.info(f"finish loading clip model")
        return model, preprocess, tokenizer

    def text_vectorize(self, text):
        if type(text) == str:
            texts = [text]
        elif type(text) == list:
            texts = text
        else:
            raise TypeError(f"Invalid type {type(text)}")

        encodings = ja_clip.tokenize(
            texts=texts, max_seq_len=77, device=self.device, tokenizer=self.tokenizer
        )
        with torch.no_grad():
            text_features = self.model.get_text_features(**encodings)
        return text_features

    def img_vectorize(self, img):
        image = self.preprocess(img).unsqueeze(0).to(self.device)
        with torch.no_grad():
            image_features = self.model.get_image_features(image)
        return image_features
