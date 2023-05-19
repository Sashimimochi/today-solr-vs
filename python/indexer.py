import datetime
import glob
import gzip
import itertools
import json
import logging
import random
import time
import subprocess

import streamlit as st

from PIL import Image
import pysolr
from pysolr import SolrError
from tqdm.auto import tqdm

from mysql import MySQLClient

client = MySQLClient()

from solr import SolrClient
from config import *
from utils import elapse_time
from vectorizer.vectorizer import Vectorizer


class Indexer(SolrClient):
    def __init__(self):
        super().__init__()
        self.v = Vectorizer()
        self.limit_index_size = 1200000
        self.post = 0

    def _progress(self, datasets, progress_text, max_index_size=0):
        s_time = time.time()
        total = (
            max_index_size
            if max_index_size < len(datasets) and max_index_size > 0
            else len(datasets)
        )
        bar = st.progress(0, text=progress_text)
        for i, data in enumerate(datasets, start=1):
            now = time.time()
            progress_percent = (i / total) * 100 if (i / total) * 100 <= 100 else 100
            left_percent = 100 - progress_percent
            pass_time = now - s_time
            left_time = pass_time / progress_percent * left_percent
            bar.progress(
                int(progress_percent),
                text=progress_text
                + f"[{i}/{total}={int(progress_percent)}%] pass time: {elapse_time(pass_time)}, left time: {elapse_time(left_time)}",
            )
            yield i, data

    def _progress_large_index(self, s_time, i, total, bar, progress_text):
        now = time.time()
        progress_percent = (i / total) * 100 if (i / total) * 100 <= 100 else 100
        left_percent = 100 - progress_percent
        pass_time = now - s_time
        left_time = pass_time / progress_percent * left_percent
        bar.progress(
            progress_percent,
            text=progress_text
            + f"[{i}/{total}={progress_percent}%] pass time: {elapse_time(pass_time)}, left time: {elapse_time(left_time)}",
        )

    def _load_large_data(self, filepath, max_index_size):
        with gzip.open(filepath) as f:
            for line in tqdm(f, total=max_index_size, desc="parse wiki documents"):
                yield json.loads(line)

    def map_media(self, k) -> int:
        medias = {
            "dokujo-tsushin": 1,
            "it-life-hack": 2,
            "kaden-channel": 3,
            "livedoor-homme": 4,
            "movie-enter": 5,
            "peachy": 6,
            "smax": 7,
            "sports-watch": 8,
            "topic-news": 9,
        }
        return medias.get(k)

    def save_index(self, data, collection):
        with open(
            f'index/index.{collection}.{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.json',
            "w",
        ) as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def create_index(self, collection, save: bool = True, filepath: str = None):
        col_info = COLLECTION.get(collection)
        result_type = col_info.get("result_type")
        model_name = col_info.get("embedding_model")
        embed_dim = self.v.embedding_dim.get(model_name)
        if collection == "wiki":
            return self.create_wiki_index(collection, filepath=filepath)
        elif result_type == "text" and embed_dim < 500:
            return self.create_text_index(collection, save)
        elif result_type == "text" and embed_dim >= 500:
            return self.create_large_text_index(collection)
        elif result_type == "image":
            return self.create_img_index(collection, save)
        else:
            raise Exception("Invalid Collection")

    def create_text_index(self, collection, save: bool = True):
        rows = client.select()
        model = COLLECTION.get(collection).get("embedding_model")
        logging.info(f"vectorize {len(rows)} texts")
        data = [
            {
                "id": i,
                "media": self.map_media(row.get("media")),
                "url": row.get("url"),
                "title": row.get("title"),
                "body": row.get("body"),
                "vector": self.v.get_text_vector(model, row.get("body")),
            }
            for i, row in self._progress(rows, progress_text="creating index...")
        ]
        logging.info(f"finish vectorize {len(rows)} texts")

        if save:
            self.save_index(data, collection)

        return len(data)

    def create_img_index(self, collection, save: bool = True):
        ext = ["jpg", "png", "JPG", "PNG", "jfif"]
        model = COLLECTION.get(collection).get("embedding_model")
        max_index_size = COLLECTION.get(collection).get("max_index_size")
        max_index_size = (
            max_index_size
            if max_index_size or max_index_size > self.limit_index_size
            else self.limit_index_size
        )
        filepaths = list(
            itertools.chain.from_iterable(
                [glob.glob(f"img/{collection}/**/*.{e}", recursive=True) for e in ext]
            )
        )
        if len(filepaths) > max_index_size:
            filepaths = random.sample(filepaths, max_index_size)
        data = [
            {
                "id": i,
                "filepath": filepath,
                "vector": self.v.get_img_vector(model, Image.open(filepath)),
            }
            for i, filepath in self._progress(
                filepaths, progress_text="creating index..."
            )
        ]

        if save:
            self.save_index(data, collection)

        return len(data)

    def create_large_text_index(self, collection, save: bool = True):
        logging.info(f"vectorize {collection} texts")
        rows = client.select()
        logging.info(f"vectorize {len(rows)} texts")
        model = COLLECTION.get(collection).get("embedding_model")
        max_index_size = COLLECTION.get(collection).get("max_index_size")

        if save:
            filepath = f'index/index.{collection}.{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.json'
            with open(
                filepath,
                "w",
            ) as f:
                for i, row in self._progress(
                    rows,
                    progress_text="creating index...",
                    max_index_size=max_index_size,
                ):
                    if i >= max_index_size:
                        break
                    data = {
                        "id": i,
                        "media": self.map_media(row.get("media")),
                        "url": row.get("url"),
                        "title": row.get("title"),
                        "body": row.get("body"),
                        "vector": self.v.get_text_vector(model, row.get("body")),
                    }
                    json.dump(data, f, ensure_ascii=False)
                    f.write("\n")
                    if i % 1000 == 0:
                        logging.info(f"{i} docs vectorized")
            subprocess.call(["gzip", filepath])

        logging.info(f"finish vectorize {collection} texts")
        return (
            max_index_size
            if max_index_size > 0 and max_index_size < len(rows)
            else len(rows)
        )

    def create_wiki_index(self, collection, filepath, save: bool = True):
        logging.info(f"vectorize {collection} texts")
        model = COLLECTION.get(collection).get("embedding_model")
        max_index_size = COLLECTION.get(collection).get("max_index_size")
        max_index_size = (
            max_index_size
            if max_index_size or max_index_size > self.limit_index_size
            else self.limit_index_size
        )

        if save:
            filepath = f'index/index.{collection}.{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.json'
            with open(
                filepath,
                "w",
            ) as f:
                for i, row in enumerate(
                    self._load_large_data(filepath, max_index_size)
                ):
                    if "index" not in row:
                        data = {
                            "id": i,
                            "media": row.get("media"),
                            "url": row.get("url"),
                            "title": row.get("title"),
                            "body": row.get("text"),
                            "vector": self.v.get_text_vector(model, row.get("text")),
                        }
                        json.dump(data, f, ensure_ascii=False)
                        f.write("\n")
                    if i % 10000 == 0:
                        logging.info(f"{i} docs vectorized")
            subprocess.call(["gzip", filepath])
        logging.info(f"finish vectorize {collection} texts")
        return i

    def _add(self, collection: str, data: list, commit: bool = True, max_post=60000):
        solr = pysolr.SolrCloud(
            self.zookeeper,
            collection=collection,
            timeout=30,
            retry_count=5,
            retry_timeout=0.2,
            always_commit=commit,
        )
        solr.ping()

        # 大きすぎるとタイムアウトするので max_post 件ずつ送る
        for i in range(0, len(data), max_post):
            solr.add(data[i : i + max_post])
            time.sleep(2)

    def _add_large_index(
        self, collection, filepath, max_index_size, max_load_size=1000
    ):
        self.post = 0
        data = []
        s_time = time.time()
        progress_text = "adding index..."
        bar = st.progress(0, text=progress_text)
        for i, row in enumerate(
            self._load_large_data(filepath, max_index_size), start=1
        ):
            data += [row]
            if i % max_load_size == 0:  # 一度に全件は Memory に載り切らないので分割して読み込み& post する
                self._add(collection, data, False)
                self.post += 1
                data = []
                self._progress_large_index(
                    s_time, i, max_index_size, bar, progress_text
                )
                if i >= max_index_size:
                    break  # リソースの都合上これ以上はSolrにインデックスできない
        if self.post == 0:  # 総ドキュメント数が max_index_size を下回った場合
            self._add(collection, data, False)

        solr = pysolr.SolrCloud(
            self.zookeeper,
            collection=collection,
            timeout=30,
            retry_count=5,
            retry_timeout=0.2,
            always_commit=False,
        )
        solr.ping()
        solr.commit()

    def _add_wiki_org(self, collection, filepath):
        max_index_size = COLLECTION.get(collection).get("max_index_size")
        max_index_size = (
            max_index_size
            if max_index_size or max_index_size > self.limit_index_size
            else self.limit_index_size
        )
        data = []
        for i, row in enumerate(self._load_large_data(filepath, max_index_size)):
            data += [
                {
                    "id": row.get("id"),
                    "media": row.get("media"),
                    "url": row.get("url"),
                    "title": row.get("title"),
                    "body": row.get("body"),
                }
            ]
            if i % 30000 == 0:
                self._add(collection, data, False)
                data = []
                if i >= max_index_size:
                    break  # リソースの都合上これ以上はSolrにインデックスできない

        solr = pysolr.SolrCloud(
            self.zookeeper,
            collection=collection,
            timeout=30,
            retry_count=5,
            retry_timeout=0.2,
            always_commit=False,
        )
        solr.ping()
        solr.commit()

    def add(self, collection, data: list = None, filepath: str = None):
        max_index_size = COLLECTION.get(collection).get("max_index_size")
        model_name = COLLECTION.get(collection).get("embedding_model")
        embed_dim = self.v.embedding_dim.get(model_name)
        index_size = "large" if max_index_size > 100000 or embed_dim >= 500 else "small"
        try:
            if data:
                self._add(collection, data)
            elif index_size == "large":
                self._add_large_index(
                    collection, filepath=filepath, max_index_size=max_index_size
                )
            else:
                self._add(collection, self.create_index(collection))
        except SolrError as e:
            raise Exception(f":umbrella_with_rain_drops: failed!\n[ERROR]\n{e}")

        return ":100: success"
