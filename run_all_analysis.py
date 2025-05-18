"""
To run all of our Python stock analysis scripts (data_extract_dsebdorg.py, data_extract_stocknow.py, heikinAshi.py, 
volumeBasedDecision.py, heikinAshiStrongBuyFilter.py, and fundamentalAnalysis.py) with a single command or click, 
we can create a master script like this:

python run_all_analysis.py

"""

import subprocess

# List of Python scripts to run in order
scripts = [
    "data_extract_dsebdorg.py",
    "data_extract_stocknow.py",
    "heikinAshi.py",
    "volumeBasedDecision.py",
    "heikinAshiStrongBuyFilter.py",
    "fundamentalAnalysis.py"
]

for script in scripts:
    print(f"\n🔄 Running: {script}")
    result = subprocess.run(["python", script], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error in {script}:\n{result.stderr}")
