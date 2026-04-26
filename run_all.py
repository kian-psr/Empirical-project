import subprocess
from pathlib import Path

scripts = [
    "src/01_get_data.py",
    "src/02_clean_data.py",
    "src/03_daily_return_data.py",
    "src/04_analysis.py",
    "src/05_market_beta_regression.py",
]

for script in scripts:
    print(f"Running {script}")
    subprocess.run(["python3", script], check=True)

print("Pipeline completed successfully.")