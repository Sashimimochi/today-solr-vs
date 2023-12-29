import os
import numpy as np


def recall_at_k(y_true, y_pred, k=5):
    return np.mean([1 if y in y_true else 0 for y in y_pred][:k])


def recall_category_at_k(y_true, y_pred, k=5):
    y_true = [y.split("/")[-2] for y in y_true]
    y_pred = [y.split("/")[-2] for y in y_pred]
    return recall_at_k(y_true, y_pred, k)


def recall_order_at_k(y_true, y_pred, k=5):
    return np.mean([1 if y_t == y_p else 0 for y_t, y_p in zip(y_true, y_pred)][:k])


def calc_score(reductor, reduct_dim, k=5):
    basedata = "output/food_None_None.csv"
    targetdata = f"output/food_{reduct_dim}_{reductor}_{reduct_dim}.csv"
    if not os.path.exists(targetdata):
        return ""
    with open(basedata) as f:
        data_true = f.readlines()
    with open(targetdata) as f:
        data_pred = f.readlines()
    score = np.mean(
        [
            recall_category_at_k(data_t.split(","), data_p.split(","), k)
            for data_t, data_p in zip(data_true, data_pred)
        ]
    )
    return score


def main():
    k = 5
    for reductor in ["PCA", "UMAP", "TSNE"]:
        for reduct_dim in ["002", "128", "256", "400"]:
            score = calc_score(reductor, reduct_dim, k)
            if score == "":
                continue
            print(f"Reductor: {reductor}, Reduct_dim: {reduct_dim}, score@{k}: {score}")


if __name__ == "__main__":
    main()
