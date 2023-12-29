import os
import json

import streamlit as st
import numpy as np

from reductor.reductor import Reductor


def load_index(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return data


def reduct_index(model_name, dim, index_filepath, field):
    reductor = Reductor()

    index_data = load_index(index_filepath)
    X = [d.get(field) for d in index_data]
    if model_name == "TSNE":
        X = np.array(X)
    X_embed = reductor.reduct_vector(model_name, dim, X)
    index_data_new = []
    for i, d in enumerate(index_data):
        d[field] = X_embed[i]
        index_data_new.append(d)

    fp, _ = os.path.splitext(index_filepath)
    o_filepath = f"{fp}.{model_name}_{dim}.json"
    with open(o_filepath, "w") as f:
        json.dump(index_data_new, f, indent=4, ensure_ascii=False)

    st.success(f"success vector reduction to {o_filepath}")
