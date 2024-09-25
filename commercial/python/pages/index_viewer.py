import glob
import json

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import plotly.express as px

from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

from reductor.init_reductor import embed_by_model

if "fields" not in st.session_state:
    st.session_state.fields = []


def plot_with_image(df, filepaths, width=100):
    def imscatter(x, y, filepaths, ax=None, zoom=1):
        artists = []
        for x0, y0, filepath in zip(x, y, filepaths):
            img = Image.open(filepath)
            w, h = img.size
            mag = width / w
            height = int(h * mag)
            img = img.resize((width, height))
            im = OffsetImage(img, zoom=zoom)

            ab = AnnotationBbox(im, (x0, y0), xycoords="data", frameon=False)
            artists.append(ax.add_artist(ab))

    fig, ax = plt.subplots()
    imscatter(df.dim1, df.dim2, filepaths, ax=ax, zoom=0.25)
    ax.scatter(df.dim1, df.dim2)

    st.pyplot(fig, theme="streamlit", use_container_width=True)


def dump_only(field, method, embed_dim):
    st.write(f"Embedding to {embed_dim}-dimensions")
    X = np.array([d.get(field) for d in st.session_state.data])
    st.metric(label="Index Size", value=f"{len(X)}")
    embed_by_model(X, n_components=embed_dim, model_name=method, save=True)


def visualize(field, method):
    st.subheader("Embedding to 2-dimensions")
    X = np.array([d.get(field) for d in st.session_state.data])
    df = embed_by_model(X, model_name=method)
    st.metric(label="Index Size", value=f"{len(df)}")
    if "filepath" in st.session_state.fields:
        plot_with_image(df, [d.get("filepath") for d in st.session_state.data])
    else:
        fig = px.scatter(
            df,
            x=f"dim1",
            y=f"dim2",
        )

        tab1, tab2 = st.tabs(["Streamlit theme", "Plotly native theme"])
        with tab1:
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        with tab2:
            st.plotly_chart(fig, theme=None, use_container_width=True)


def load_index(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return data


def main():
    st.title("Index Viewer")

    filepaths = glob.glob(f"index/*.json")
    filepath = st.selectbox("choice index file", filepaths)
    if st.button("load index data"):
        st.session_state.data = load_index(filepath)
        st.session_state.fields = list(st.session_state.data[0].keys())

    field = st.selectbox("select vector field", [None] + st.session_state.fields)
    method = st.selectbox(
        "select dimension reduction method", ["MDS", "UMAP", "PCA", "TSNE"]
    )

    if field and "data" in st.session_state:
        max_value = len(st.session_state.data[0].get(field))
        max_value = max_value if max_value < 1024 else 1024
        if method == "TSNE":
            max_value = 2

        embed_dim = st.number_input(
            "input embedding dimension",
            value=256 if 256 < max_value else max_value,
            min_value=2,
            max_value=max_value,
            step=1,
        )
        if st.button("dumping only"):
            dump_only(field, method, embed_dim)

    if st.button("visualize"):
        visualize(field, method)


if __name__ == "__main__":
    main()
