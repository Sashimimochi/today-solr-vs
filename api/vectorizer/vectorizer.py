from vectorizer.clip_vectorizer import Vectorizer as cv
from vectorizer.w2v_vectorizer import Vectorizer as wv
from vectorizer.densenet_vectorizer import Vectorizer as dv
from vectorizer.sentence_bert_vectorizer import Vectorizer as sv


class Vectorizer:
    def __init__(self) -> None:
        self.clip = cv()
        self.w2v = wv()
        self.densenet = dv()
        self.sentence_bert = sv()

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
