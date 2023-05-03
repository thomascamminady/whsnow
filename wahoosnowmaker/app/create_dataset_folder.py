from datetime import datetime
from pathlib import Path


def create_dataset_folder() -> str:
    # dataset_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=20))
    dataset_name = datetime.now().isoformat()
    dataset_folder = f"data/{dataset_name}/"
    Path(dataset_folder).mkdir(parents=True, exist_ok=True)
    return dataset_folder
