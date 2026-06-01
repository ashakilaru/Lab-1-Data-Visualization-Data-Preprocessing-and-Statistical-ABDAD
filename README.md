MSCS 634 — Lab 1

Purpose
- Demonstrates data visualization, preprocessing, and statistical analysis on the `tips` dataset and saves artifacts required for submission.

Repository contents (generated/expected)
- `MSCS_634_Lab_1.ipynb` — Jupyter Notebook implementing all lab steps.
- `run_lab.py` — Headless runner that reproduces the notebook steps and saves outputs.
- `data/tips.csv` — Local copy of the dataset (created when the notebook or runner is executed).
- `screenshots/` — Contains generated figures and CSV/text snapshots (examples below):
	- `scatter_totalbill_tip.png`, `hist_total_bill.png`, `boxplot_tip_by_day.png`, `correlation_heatmap.png`
	- `df_head_before.csv`, `df_with_missing_before.csv`, `df_with_missing_after.csv`
	- `outliers_total_bill.csv`, `df_after_outlier_removal.csv`, `df_after_reduction.csv`
	- `describe_all.csv`, `central_tendency.csv`, `dispersion_measures.csv`, `correlation_matrix.csv`

Reproduce locally (recommended)
1. Create a Python virtual environment and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
# or install the minimal packages directly:
pip install pandas seaborn matplotlib scikit-learn
```

3a. Run the headless runner to generate `data/` and `screenshots/`:

```bash
python run_lab.py
```

3b. (Optional) Open and run the notebook interactively in Jupyter/VS Code:

```bash
jupyter notebook MSCS_634_Lab_1.ipynb
```

What to push to GitHub for submission
- `MSCS_634_Lab_1.ipynb`
- `run_lab.py`
- `data/tips.csv` (generated after running)
- `screenshots/` folder with the saved images and CSV/text outputs
- `README.md` (this file)

Suggested git commands

```bash
git add MSCS_634_Lab_1.ipynb run_lab.py data/tips.csv screenshots README.md
git commit -m "Add lab notebook, runner, dataset, and screenshots"
git remote add origin <your-repo-url>
git push -u origin main
```

Notes
- Replace `[Your Name]` in the notebook top cell with your full name before submission.
- If you prefer a different dataset, update the loading cell or `run_lab.py` and commit the dataset CSV to `data/`.