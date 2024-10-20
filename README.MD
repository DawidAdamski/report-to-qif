# Report to QIF

Developed a script to easily convert mBank financial reports in CSV format to QIF for streamlined uploads. This simplifies the process of managing financial data across platforms.

## Install

1. Create your venv.
2. Install dependencies using requirements.txt ```pip install -r requirements.txt```
3. Use it.

## Usage
```
usage: main.py [-h] -i INPUT_FILE [-o OUTPUT_FILE] -b {mbank,mbank-credit,alior,santander}

Convert CSV files with bank reports to QIF format.

options:
  -h, --help            show this help message and exit

Script Operations:
  Arguments for handling input/output files

  -i, --in INPUT_FILE   Path to the input CSV file.
  -o, --out OUTPUT_FILE
                        Path to the output QIF file (optional).

Bank Options:
  Arguments related to bank configuration

  -b, --bank {mbank,mbank-credit,alior,santander}
                        Specify the bank identifier. 'mbank' is implemented. 'mbank-credit' is implemented. 'alior' and 'santander' are not yet implemented.
```                        