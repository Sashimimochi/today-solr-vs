import time
import pysolr
from pysolr import SolrError
import PIL
import numpy as np

from config import *
from solr.solr import Searcher
from vectorizer.vectorizer import Vectorizer
from reductor.reductor import Reductor


class BasicSearcher(Searcher):
    def __init__(self) -> None:
        super().__init__()

    def search(self, collection, query):
        solr = pysolr.SolrCloud(
            self.zookeeper,
            collection=collection,
            timeout=30,
            retry_count=5,
            retry_timeout=0.2,
            always_commit=False,
        )
        try:
            solr.ping()
        except SolrError:
            res = [{"status": ":umbrella_with_rain_drops: connection failed"}]
            return res

        try:
            results = solr.search(**query)
        except SolrError as e:
            raise SolrError(f"""クエリに誤りがある可能性があります。確認してください。詳細は以下をご確認ください。{e}""")
        return results


class VectorSearcher(Searcher):
    def __init__(self) -> None:
        super().__init__()
        self.v = Vectorizer()
        self.r = Reductor()

    def search(self, collection, query, reduct_model_name=None, reduct_dim=0):
        if type(query.get("q")) == str:
            return self._text_query(collection, query, reduct_model_name, reduct_dim)
        elif type(query.get("q")) in [
            PIL.JpegImagePlugin.JpegImageFile,
            PIL.PngImagePlugin.PngImageFile,
        ]:
            return self._img_query(collection, query, reduct_model_name, reduct_dim)
        else:
            return self._query(collection, None, reduct_model_name, reduct_dim)

    def _img_query(self, collection, query, reduct_model_name, reduct_dim):
        model = COLLECTION.get(collection).get("embedding_model")
        s_time = time.time()
        _vec = self.v.get_img_vector(model, query.get("q"))
        v_time = time.time() - s_time
        return self._query(collection, _vec, reduct_model_name, reduct_dim), v_time

    def _text_query(self, collection, query, reduct_model_name, reduct_dim):
        model = COLLECTION.get(collection).get("embedding_model")
        s_time = time.time()
        vec = self.v.get_text_vector(model, query.get("q"))
        v_time = time.time() - s_time
        if collection in ["text_short", "wiki"]:
            _vec = vec
        else:
            _vec = vec
        return self._query(collection, _vec, reduct_model_name, reduct_dim), v_time

    def _query(self, collection, vec, reduct_model_name, reduct_dim):
        col_info = COLLECTION.get(collection)
        if reduct_model_name:
            if reduct_model_name == "TSNE":
                vec = np.array([vec])
                vec = self.r.reduct_vector(reduct_model_name, reduct_dim, vec)[0]
            else:
                vec = self.r.reduct_vector(reduct_model_name, reduct_dim, [vec])[0]
        if collection == "mini":
            q = "{!knn f=vector topK=10}[1.0, 2.0, 3.0, 4.0]"
            fl = "id"
        elif col_info.get("result_type") == "image":
            q = "{!knn f=vector topK=10}" + f"{vec}"
            fl = "id filepath score"
        else:
            q = "{!knn f=vector topK=10}" + f"{vec}"
            fl = "id title body score"

        solr = pysolr.SolrCloud(
            self.zookeeper,
            collection=collection,
            timeout=30,
            retry_count=5,
            retry_timeout=0.2,
            always_commit=False,
        )
        try:
            solr.ping()
        except SolrError:
            res = [{"status": ":umbrella_with_rain_drops: connection failed"}]
            return res

        results = solr.search(q=q, fl=fl)
        return results
