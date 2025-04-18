import torch
import streamlit as st

from transformers import BertJapaneseTokenizer, BertModel


class Vectorizer:
    def __init__(self) -> None:
        self.model, self.tokenizer, self.device = self.load_model()

    @st.cache_resource
    def load_model(_self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model_name = "sonoisa/sentence-bert-base-ja-mean-tokens-v2"
        model = BertModel.from_pretrained(model_name)
        tokenizer = BertJapaneseTokenizer.from_pretrained(model_name)
        model.eval()

        device = torch.device(device)
        model.to(device)
        return model, tokenizer, device

    def _mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[
            0
        ]  # First element of model_output contains all token embeddings
        input_mask_expanded = (
            attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        )
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
            input_mask_expanded.sum(1), min=1e-9
        )

    @torch.no_grad()
    def encode(self, sentences, batch_size=8):
        all_embeddings = []
        iterator = range(0, len(sentences), batch_size)
        for batch_idx in iterator:
            batch = sentences[batch_idx : batch_idx + batch_size]

            encoded_input = self.tokenizer.batch_encode_plus(
                batch, padding="longest", truncation=True, return_tensors="pt"
            ).to(self.device)
            model_output = self.model(**encoded_input)
            sentence_embeddings = self._mean_pooling(
                model_output, encoded_input["attention_mask"]
            ).to("cpu")

            all_embeddings.extend(sentence_embeddings)

        return torch.stack(all_embeddings)

    def text_vectorize(self, text):
        return self.encode(text, batch_size=4)
