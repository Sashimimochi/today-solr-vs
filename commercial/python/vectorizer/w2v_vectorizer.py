from gensim.models import word2vec, KeyedVectors
import MeCab
import numpy as np
import streamlit as st
from config import MODEL


class Vectorizer:
    def __init__(self) -> None:
        self.model, self.mt = self.load_model()

    @st.cache_resource
    def load_model(_self):
        model_path = MODEL.get("model_path")
        binary = MODEL.get("binary")
        model_format = MODEL.get("model_format")
        if model_format == "vector_only":
            model = KeyedVectors.load_word2vec_format(model_path, binary=binary)
        else:
            model = word2vec.Word2Vec.load(model_path)
        path = "/usr/lib/x86_64-linuxgnu/mecab/dic/mecab-ipadic-neologd"
        mt = MeCab.Tagger(path)  # 形態素解析器
        return model, mt

    def _vectorize(self, word) -> None:
        return self.model.wv.get_vector(word)

    def text_vectorize(self, text):
        sum_vec = np.zeros(self.model.vector_size)
        word_count = 0
        node = self.mt.parseToNode(text)
        while node:
            fields = node.feature.split(",")
            word = node.surface
            if fields[0] in ["名詞", "動詞", "形容詞"] and word in self.model.wv.vocab.keys():
                sum_vec += self._vectorize(word)
                word_count += 1
            node = node.next
        word_count = word_count if word_count > 0 else 1
        return sum_vec / word_count
