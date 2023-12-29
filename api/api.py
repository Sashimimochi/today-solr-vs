import time
from fastapi import FastAPI
import uvicorn
from solr.request import VectorSearcher
from typing import Union

app = FastAPI()
searcher = VectorSearcher()


def text_search(collection, reductor, reduct_dim, text):
    s_time = time.time()
    resp, v_time = searcher.search(
        collection,
        query={"q": text},
        reduct_model_name=reductor,
        reduct_dim=reduct_dim,
    )
    e_time = time.time()
    print(
        {
            "Search Time": f"{(e_time - s_time)*1000}[ms]",
            "Vectorized Time": f"{(v_time)*1000}[ms]",
        }
    )
    res = ",".join([r.get("filepath") for r in resp.docs]) + "\n"
    with open(f"output/{collection}_{reductor}_{reduct_dim}.csv", "a") as f:
        f.write(res)
    return resp.docs


@app.get("/")
def index():
    return {"msg": "endpoint"}


@app.get("/search/")
def search(
    text: str = "",
    reductor: Union[str, None] = None,
    reduct_dim: Union[int, None] = None,
    collection: Union[str, None] = None,
):
    return text_search(collection, reductor, reduct_dim, text)


if __name__ == "__main__":
    uvicorn.run(app)
