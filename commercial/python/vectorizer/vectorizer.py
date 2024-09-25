from vectorizer.clip_vectorizer import Vectorizer as cv
from vectorizer.w2v_vectorizer import Vectorizer as wv
from vectorizer.densenet_vectorizer import Vectorizer as dv
from vectorizer.sentence_bert_vectorizer import Vectorizer as sv
from vectorizer.mobnetv3_vectorizer import Vectorizer as mv
from vectorizer.inceptionv3_vectorizer import Vectorizer as iv


class Vectorizer:
    def __init__(self) -> None:
        self.clip = cv()
        self.w2v = wv()
        self.densenet = dv()
        self.sentence_bert = sv()
        self.mobnet = mv()
        self.inception = iv()

        self.embedding_dim = {
            "clip": 512,
            "w2v": 200,
            "densenet": 1024,  # 'densenet121'
            "resnet": 512,  # 'resnet18'
            "sentence_bert": 768,
            "mobnet": 1280,
            "inception": 2048,
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
        elif model == "mobnet":
            return self.mobnet.img_vectorize(img).tolist()[0]
        elif model == "inception":
            return self.inception.img_vectorize(img).tolist()[0]
        else:
            return self.clip.img_vectorize(img).tolist()[0]
