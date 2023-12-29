import pickle
import umap

import pandas as pd
import streamlit as st

from sklearn.manifold import MDS
from sklearn.decomposition import PCA
from openTSNE import TSNE


def embed_by_model(x, n_components=2, model_name="", save=False):
    if model_name == "PCA":
        model = _embed_by_pca(n_components)
    elif model_name == "TSNE":
        _model = _embed_by_tsne(n_components)
    elif model_name == "UMAP":
        model = _embed_by_umap(n_components)
    else:
        model = _embed_by_mds(n_components)

    if model_name == "TSNE":
        model = _model.fit(x)
        x_embed = model.transform(x)
    else:
        x_embed = model.fit_transform(x)
    st.info(x_embed.shape)
    if save:
        filepath = f"model/{model_name}_model_{n_components}.pkl"
        with open(filepath, "wb") as f:
            pickle.dump(model, f)
        st.success(f"Success to save {filepath}")

    return pd.DataFrame(
        x_embed,
        columns=[f"dim{i+1}" for i in range(n_components)],
    )


def _embed_by_pca(n_components=2, random_state=0):
    return PCA(n_components=n_components, random_state=random_state)


def _embed_by_tsne(n_components=2, random_state=0):
    return TSNE(n_components=n_components, random_state=random_state)


def _embed_by_umap(n_components=2, random_state=0, densmap=False, dens_lambda=1):
    return umap.UMAP(
        n_components=n_components,
        random_state=random_state,
        densmap=densmap,
        dens_lambda=dens_lambda,
    )


def _embed_by_mds(n_components=2, random_state=0):
    return MDS(n_components=n_components, random_state=random_state)
