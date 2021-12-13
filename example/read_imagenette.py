import subprocess
from io import BytesIO
from pathlib import Path
from typing import Any, Callable, List, Tuple

from mmzipfile import MmZipFile
from PIL import Image
from torch import Tensor
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms as T
from torchvision.datasets.utils import download_and_extract_archive
from tqdm import tqdm


class Imagenette160px(Dataset):

    url = "https://s3.amazonaws.com/fast-ai-imageclas/imagenette2-160.tgz"

    def __init__(
        self,
        root: str,
        transform: Callable[[Any], Tensor] = None,
        train: bool = True,
        download: bool = False,
        read_method: str = "open",
    ) -> None:
        super().__init__()

        root_dir = Path(root)

        if download:
            self.download(root_dir)

        mm_zip_file = MmZipFile(root)
        split = "train" if train else "val"
        samples = parse_files(mm_zip_file.namelist(), split)

        self.samples = samples
        self.mm_zip_file = mm_zip_file
        self.transform = transform
        self.read_method = read_method

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index: int):
        file_path, label = self.samples[index]

        # 两种读取接口
        if self.read_method == "open":
            with self.mm_zip_file.open(file_path) as f:
                image = Image.open(f).convert("RGB")
                image_tensor = self.transform(image)
        elif self.read_method == "read":
            fp = BytesIO(self.mm_zip_file.read(file_path))
            image = Image.open(fp).convert("RGB")
            image_tensor = self.transform(image)
        else:
            raise Exception

        return image_tensor, label

    def download(self, root_dir: Path):
        if root_dir.exists():
            return

        root_dir.parent.mkdir(parents=True, exist_ok=True)
        download_and_extract_archive(self.url, str(root_dir.parent))
        subprocess.check_call(
            ["zip", "-r", "-0", str(root_dir), str(root_dir.parent / "imagenette2-160")]
        )


def TrainTransform():
    return T.Compose(
        [
            T.RandomResizedCrop(128),
            T.RandomHorizontalFlip(),
            T.ToTensor(),
            T.Normalize([0.5] * 3, [0.5] * 3),
        ]
    )


def ValTransform():
    return T.Compose(
        [
            T.Resize(144),
            T.CenterCrop(128),
            T.ToTensor(),
            T.Normalize([0.5] * 3, [0.5] * 3),
        ]
    )


def DummyTransform():
    return T.Compose(
        [
            T.CenterCrop(128),
            T.ToTensor(),
        ]
    )


def parse_files(file_list: List[str], split: str) -> List[Tuple[str, int]]:
    # imagenette2-160/val/n03028079/n03028079_15392.JPEG

    def get_label(file_path: str) -> str:
        return file_path.split("/")[-2]

    labels = sorted(set(map(get_label, file_list)))
    label_dict = {x: i for i, x in enumerate(labels)}
    print(label_dict)

    subset = filter(lambda p: split in p and ".JPEG" in p, file_list)

    def get_label_id(file_path: str) -> int:
        label = get_label(file_path)
        return label_dict[label]

    samples = list(map(lambda p: (p, get_label_id(p)), subset))
    print(samples[0])

    return samples


def main():

    batch_size = 256
    num_workers = 8

    dataset = Imagenette160px(
        "example/data/imagenette/imagenette2-160.zip",
        transform=DummyTransform(),
        download=True,
    )

    image, label = dataset[0]
    print(image.shape)
    print(label)

    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        shuffle=True,
    )

    with tqdm(unit="img", total=len(dataset)) as pbar:
        for image, label in loader:
            pbar.update(n=image.size(0))


if __name__ == "__main__":
    main()
