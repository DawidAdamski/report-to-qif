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

## Other

If you want to have other banks in script, just contact me. I need to have example report (remember to anonymyze it!) and can add option.

## How to obtain report?
### mBank

1. Go to your "Finanse" to "Zestawienie operacji"

![Alt text](img/1.png?raw=true "Title")

2. In Zestawienie operacji choose your period and remember to take "CSV" format.

![Alt text](img/2.png?raw=true "Title")

3. Download your financial report. 

Remark! Downloaded reports have names starting with the eight last numbers of the account, underscore, start period, underscore, and end period. If you are not a big wacko who remembers all your account numbers, then it is good to give some meaningful names when saving files. 