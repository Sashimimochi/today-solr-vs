import pickle


class Reductor:
    def __init__(self) -> None:
        pass

    def reduct_vector(self, model_name, dim, X):
        model_filepath = f"model/{model_name}_model_{dim}.pkl"
        model = self._load_model(model_filepath)
        return self._reduct_vector(model, X)

    def _load_model(self, filepath):
        with open(filepath, "rb") as f:
            return pickle.load(f)

    def _reduct_vector(self, model, X):
        return model.transform(X).tolist()
