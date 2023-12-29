import requests
from tqdm.auto import tqdm

BASE_URL = "http://localhost:5000/search"
REDUCTOR = "UMAP"
REDUCT_DIM = "128"


def request(filepath):
    with open(filepath) as f:
        queries = f.readlines()

    for q in tqdm(queries):
        # requests.get(f"{BASE_URL}?text={q}&collection=food")
        requests.get(
            f"{BASE_URL}?text={q}&collection=food_{REDUCT_DIM}&reductor={REDUCTOR}&reduct_dim={REDUCT_DIM}"
        )


def main():
    # request("query/queries_1.txt")
    # request("query/queries_2.txt")
    # request("query/queries_3.txt")
    request("query/queries_4.txt")
    request("query/queries_5.txt")
    request("query/queries_6.txt")


if __name__ == "__main__":
    main()
