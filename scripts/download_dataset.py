import argparse
import shutil
import zipfile
from pathlib import Path

DATASET_FILE_ID = "1VuI1NnPzYlhHIMBy-2nBegFoQTATbf8K"
ROOT_DIR = Path(__file__).resolve().parent.parent
ZIP_PATH = ROOT_DIR / "youtube_trending_dataset.zip"
EXTRACTED_ALT_DIR = ROOT_DIR / "trendingYT"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download YouTube Trending dataset")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Delete existing videos/ and categories/ before downloading again.",
    )
    return parser.parse_args()


def dataset_ready(videos_dir: Path, categories_dir: Path) -> bool:
    if not videos_dir.exists() or not categories_dir.exists():
        return False
    has_csv = any(videos_dir.glob("*.csv"))
    has_json = any(categories_dir.glob("*.json"))
    return has_csv and has_json


def decompress_zst_to_csv(zst_path: Path, csv_path: Path) -> None:
    try:
        import zstandard as zstd
    except ImportError as exc:
        raise RuntimeError(
            "zstandard is required to extract .zst video files. "
            "Run: pip install -r requirements.txt"
        ) from exc

    with zst_path.open("rb") as source, csv_path.open("wb") as target:
        dctx = zstd.ZstdDecompressor()
        with dctx.stream_reader(source) as reader:
            shutil.copyfileobj(reader, target)


def normalize_dataset_layout(root_dir: Path, videos_dir: Path, categories_dir: Path) -> None:
    videos_dir.mkdir(parents=True, exist_ok=True)
    categories_dir.mkdir(parents=True, exist_ok=True)
    extracted_alt_dir = root_dir / "trendingYT"

    if extracted_alt_dir.exists():
        category_files = list(extracted_alt_dir.rglob("*_category_id.json"))
        csv_files = list(extracted_alt_dir.rglob("*videos.csv"))
        zst_files = list(extracted_alt_dir.rglob("*videos.csv.zst"))

        for src in category_files:
            shutil.copy2(src, categories_dir / src.name)

        for src in csv_files:
            shutil.copy2(src, videos_dir / src.name)

        for src in zst_files:
            target_name = src.name.removesuffix(".zst")
            decompress_zst_to_csv(src, videos_dir / target_name)

    if extracted_alt_dir.exists():
        shutil.rmtree(extracted_alt_dir)


def main() -> None:
    args = parse_args()
    videos_dir = ROOT_DIR / "videos"
    categories_dir = ROOT_DIR / "categories"

    try:
        import gdown
    except ImportError as exc:
        raise RuntimeError(
            "gdown is not installed. Run: pip install -r requirements.txt"
        ) from exc

    if dataset_ready(videos_dir, categories_dir) and not args.force:
        print("Dataset already present (videos/ and categories/).")
        print("Use --force if you want to download it again.")
        return

    if args.force:
        if videos_dir.exists():
            shutil.rmtree(videos_dir)
        if categories_dir.exists():
            shutil.rmtree(categories_dir)
        if EXTRACTED_ALT_DIR.exists():
            shutil.rmtree(EXTRACTED_ALT_DIR)

    url = f"https://drive.google.com/uc?id={DATASET_FILE_ID}"
    print("Downloading dataset...")
    gdown.download(url, str(ZIP_PATH), quiet=False, fuzzy=True)

    print("Extracting dataset...")
    with zipfile.ZipFile(ZIP_PATH, "r") as archive:
        archive.extractall(ROOT_DIR)

    print("Normalizing dataset layout...")
    normalize_dataset_layout(ROOT_DIR, videos_dir, categories_dir)

    ZIP_PATH.unlink(missing_ok=True)

    if not dataset_ready(videos_dir, categories_dir):
        raise RuntimeError("Dataset extracted, but videos/ or categories/ was not found.")

    print("Done. Dataset is ready.")


if __name__ == "__main__":
    main()
