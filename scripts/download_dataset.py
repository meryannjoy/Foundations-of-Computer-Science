#!/usr/bin/env python3
"""Minimal script to download and extract the dataset used by the notebook."""

import argparse
import shutil
import zipfile
from pathlib import Path

DATASET_FILE_ID = "1VuI1NnPzYlhHIMBy-2nBegFoQTATbf8K"
ROOT_DIR = Path(__file__).resolve().parent.parent
ZIP_PATH = ROOT_DIR / "youtube_trending_dataset.zip"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download YouTube Trending dataset")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Delete existing videos/ and categories/ before downloading again.",
    )
    return parser.parse_args()


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

    if videos_dir.exists() and categories_dir.exists() and not args.force:
        print("Dataset already present (videos/ and categories/).")
        print("Use --force if you want to download it again.")
        return

    if args.force:
        if videos_dir.exists():
            shutil.rmtree(videos_dir)
        if categories_dir.exists():
            shutil.rmtree(categories_dir)

    url = f"https://drive.google.com/uc?id={DATASET_FILE_ID}"
    print("Downloading dataset...")
    gdown.download(url, str(ZIP_PATH), quiet=False, fuzzy=True)

    print("Extracting dataset...")
    with zipfile.ZipFile(ZIP_PATH, "r") as archive:
        archive.extractall(ROOT_DIR)

    ZIP_PATH.unlink(missing_ok=True)

    if not videos_dir.exists() or not categories_dir.exists():
        raise RuntimeError("Dataset extracted, but videos/ or categories/ was not found.")

    print("Done. Dataset is ready.")


if __name__ == "__main__":
    main()
