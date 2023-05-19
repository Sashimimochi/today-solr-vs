import streamlit as st
from vectorizer.clip_vectorizer import Vectorizer as cv
from vectorizer.w2v_vectorizer import Vectorizer as wv
from vectorizer.densenet_vectorizer import Vectorizer as dv
from vectorizer.sentence_bert_vectorizer import Vectorizer as sv


class Vectorizer:
    def __init__(self) -> None:
        if "clip" not in st.session_state:
            st.session_state.clip = cv()
        self.clip = st.session_state.clip
        if "w2v" not in st.session_state:
            st.session_state.w2v = wv()
        self.w2v = st.session_state.w2v
        if "densenet" not in st.session_state:
            st.session_state.densenet = dv()
        self.densenet = st.session_state.densenet
        if "sentence_bert" not in st.session_state:
            st.session_state.sentence_bert = sv()
        self.sentence_bert = st.session_state.sentence_bert

        self.embedding_dim = {
            "clip": 512,
            "w2v": 200,
            "densenet": 1024,  # 'densenet121'
            "resnet": 512,  # 'resnet18'
            "sentence_bert": 768,
        }

    def get_text_vector(self, model, text):
        if model == "w2v":
            return self.w2v.text_vectorize(text).tolist()
        elif model == "sentence_bert":
            return self.sentence_bert.text_vectorize(text).tolist()[0]
        else:
            return self.clip.text_vectorize(text).tolist()[0]

    def get_img_vector(self, model, img):
        if model == "densenet":
            return self.densenet.img_vectorize(img).tolist()[0]
        else:
            return self.clip.img_vectorize(img).tolist()[0]
