import glob
import gc

import streamlit as st

from reductor.index_reductor import reduct_index, load_index

if "fields" not in st.session_state:
    st.session_state.fields = []


def main():
    st.title("Index reductor")
    model_name = st.selectbox(
        "select dimension reduction method", ["UMAP", "PCA", "TSNE"]
    )
    dim = st.number_input(
        "input reducted dimension",
        min_value=2,
        max_value=1024,
        value=256,
        step=1,
        help="input reduction model dimension that exists.",
    )
    filepaths = glob.glob(f"index/*.json")
    filepath = st.selectbox("choice index file", filepaths)
    if st.button("load index data"):
        data = load_index(filepath)
        st.session_state.fields = list(data[0].keys())
        del data
        gc.collect()

    field = st.selectbox("select vector field", [None] + st.session_state.fields)
    if st.button("reduct index"):
        reduct_index(model_name, dim, filepath, field)


if __name__ == "__main__":
    main()
