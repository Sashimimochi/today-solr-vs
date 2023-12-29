import glob
import json
from logging import getLogger, INFO
import time
import streamlit as st
from PIL import Image
from solr.request import VectorSearcher
from solr.indexer import Indexer
from solr.response import make_response
from config import *
from utils import calc_elapse_time
import gc

logger = getLogger(__name__)
logger.setLevel(INFO)

searcher = VectorSearcher()
indexer = Indexer()


def create_index(collection):
    datasource = st.selectbox("choice datasource", ("db", "file"))
    filepath = None
    col1, col2 = st.columns(2)
    if datasource == "file":
        filepath = st.selectbox("filepath", glob.glob(f"index/*.gz"))
    if st.button(":seedling: Create Index"):
        s_time = time.time()
        i = indexer.create_index(collection, save=True, filepath=filepath)
        e_time = time.time()
        st.info(":100: success")
        col1.metric(label="Index Size", value=f"{i}")
        col2.metric(label="Indexing Time", value=calc_elapse_time(s_time, e_time))


def index_with_file(collection):
    st.subheader("Update index by file")
    st.write("D&D or Select Index File from below list")
    index_data = st.file_uploader(label="index data", type="json")
    filepath = st.selectbox("select index file", glob.glob(f"index/*.gz"))
    data = None
    if st.button(label=":blue_book: Index with File"):
        if index_data:
            data = json.load(index_data)
        try:
            st.info(indexer.add(collection, data, filepath))
        except Exception as e:
            st.error(e)


def index_from_db(collection):
    st.subheader("Update index from Database")
    if st.button(label=":green_book: Full Index Update"):
        try:
            st.info(indexer.add(collection))
        except Exception as e:
            st.error(e)


def text_search(collection):
    reductor = st.selectbox("select reductor", [None, "PCA", "TSNE", "UMAP"])
    reduct_dim = st.number_input(
        "input reducted dimension",
        min_value=2,
        max_value=1024,
        value=256,
        step=1,
        help="input reduction model dimension that exists.",
    )
    text = st.text_input(label="query keyword", placeholder="input query text here")
    if st.button(label=":mag: Search"):
        s_time = time.time()
        resp, v_time = searcher.search(
            collection,
            query={"q": text},
            reduct_model_name=reductor,
            reduct_dim=reduct_dim,
        )
        e_time = time.time()
        st.write(
            {
                "Search Time": f"{(e_time - s_time)*1000}[ms]",
                "Vectorized Time": f"{(v_time)*1000}[ms]",
            }
        )
        make_response(collection, resp)


def img_search(collection):
    img = st.file_uploader(label="image", type=["jpg", "png"])
    if img:
        st.image(img)
        if st.button(label=":mag: Search by Image"):
            image = Image.open(img)
            s_time = time.time()
            resp, v_time = searcher.search(collection, query={"q": image})
            e_time = time.time()
            st.write(
                {
                    "Search Time": f"{(e_time - s_time)*1000}[ms]",
                    "Vectorized Time": f"{(v_time)*1000}[ms]",
                }
            )
            make_response(collection, resp)
            gc.collect()


def main():
    st.title("Vector Search Engine")

    st.header("Select Collection")
    collection = st.selectbox("Select Collection", COLLECTION.keys())

    tab1, tab2 = st.tabs(["Create Index", "Update Index"])
    with tab1:
        st.header("Create Index")
        create_index(collection)
    with tab2:
        st.header("Update Index")
        index_with_file(collection)
        index_from_db(collection)

    tab3, tab4 = st.tabs(["Search by Text", "Search by Image"])
    with tab3:
        st.header("Search by text")
        text_search(collection)
    with tab4:
        st.header("Search by image")
        img_search(collection)


if __name__ == "__main__":
    main()
