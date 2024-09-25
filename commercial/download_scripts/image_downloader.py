import fiftyone.zoo as foz
import fiftyone as fo

OUTPUT_DIR = "./images"

dataset = foz.load_zoo_dataset(
        "open-images-v6",
        split="validation",
        label_types=["detections"],
        classes=[
            "Food",
        ],
        max_samples=2000,
        only_matching=True,
)

dataset.export(
    export_dir=OUTPUT_DIR,
    dataset_type=fo.types.ImageClassificationDirectoryTree
)

from PIL import Image
import os

def delete_small_images(folder_path):
    cnt = 0
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    if width <= 512 or height <= 512:
                        os.remove(file_path)
                        cnt += 1
            except Exception as e:
                print(f"エラー: {file_path} を処理中にエラーが発生しました - {e}")
    print(f"サイズが小さな{cnt}件の画像を削除しました。")

delete_small_images(OUTPUT_DIR)
