COLLECTION = {
    "basic": {
        "result_type": "text",
        "embedding_model": None,
        "max_index_size": 100,
    },
    "mini": {
        "result_type": "text",
        "embedding_model": None,
        "max_index_size": 100,
    },
    "mini_dual": {
        "result_type": "text",
        "embedding_model": None,
        "max_index_size": 100,
    },
    "text_short": {
        "result_type": "text",
        "embedding_model": "w2v",
        "max_index_size": 90000,
    },
    "food": {
        "result_type": "image",
        "embedding_model": "clip",
        "max_index_size": 5000,
    },
    "food_002": {
        "result_type": "image",
        "embedding_model": "clip",
        "max_index_size": 5000,
    },
    "food_128": {
        "result_type": "image",
        "embedding_model": "clip",
        "max_index_size": 5000,
    },
    "food_256": {
        "result_type": "image",
        "embedding_model": "clip",
        "max_index_size": 5000,
    },
    "food_400": {
        "result_type": "image",
        "embedding_model": "clip",
        "max_index_size": 5000,
    },
    "food2": {
        "result_type": "image",
        "embedding_model": "clip",
        "max_index_size": 5000,
    },
    "wiki": {
        "result_type": "text",
        "embedding_model": "w2v",
        "max_index_size": 1200000,
    },
    "text": {
        "result_type": "text",
        "embedding_model": "clip",
        "max_index_size": 200000,
    },
    "text_large": {
        "result_type": "text",
        "embedding_model": "sentence_bert",
        "max_index_size": 50,
    },
    "wiki_org": {
        "result_type": "text",
        "embedding_model": None,
        "max_index_size": 120000,
    },
    "illust": {
        "result_type": "image",
        "embedding_model": "inception",
        "max_index_size": 1,
    },
}

TABLES = ["lcc", "knbc", "kwdlc"]

MODEL = {
    "model_path": "model/entity_vector/entity_vector.model.bin",
    "model_format": "vector_only",
    "binary": True,
}
