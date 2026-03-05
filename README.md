# Foundations of Computer Science - YouTube Trending Analysis

Author: Hernandez Nicole Winy, Ortega Azriel Matthew, Tibayan Meryann Joy

## Project Overview
This project is part of the university course "Foundations of Computer Science".

The analysis is implemented in a Jupyter notebook using the YouTube Trending dataset and covers all required course tasks.

## Repository Structure
- `Youtube Trending Notebook.ipynb`: Main notebook with the full analysis.
- `requirements.txt`: Python dependencies needed to run the notebook and dataset bootstrap.
- `scripts/download_dataset.py`: Script to download and extract the dataset.
- `videos/`: Local CSV files used by the notebook (generated locally, gitignored).
- `categories/`: Local JSON category files used by the notebook (generated locally, gitignored).

## Requirements
- Python 3.10 or newer
- pip

Install dependencies:

```bash
pip install -r requirements.txt
```

## Dataset Setup
Download and extract the dataset in the project root:

```bash
python scripts/download_dataset.py
```

If you need to download everything again:

```bash
python scripts/download_dataset.py --force
```

After extraction, the project uses `videos/` and `categories/` from the repository root.

## How to Run the Code
1. Create a virtual environment:
```bash
python3 -m venv .venv
```
2. Activate it:
```bash
source .venv/bin/activate
```
Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Download and extract the dataset:
```bash
python scripts/download_dataset.py
```
5. Start Jupyter and open `Youtube Trending Notebook.ipynb`:
```bash
jupyter lab
```
