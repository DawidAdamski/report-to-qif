import argparse
import os
import sys
import chardet
import pandas as pd

def detect_encoding(file_path):
    detector = chardet.UniversalDetector()
    
    with open(file_path, 'rb') as file:
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    
    return detector.result['encoding']

def find_header_start(file_path, encoding):
    target_header = "#Data księgowania;#Data operacji;#Opis operacji;#Tytuł;#Nadawca/Odbiorca;#Numer konta;#Kwota;#Saldo po operacji;"
    header_line = None
    line_count = 0

    # Read the file line by line to find the header
    with open(file_path, 'r', encoding="cp1250") as file:
        for line in file:
            line_count += 1
            if target_header in line:
                header_line = line_count
                break
    
    if header_line is None:
        print("Header not found.")
        sys.exit(1)
    
    return header_line

def csv_to_qif(input_file, output_file, bank):

    # Detect file encoding
    encoding = detect_encoding(input_file)
    print(f"Detected encoding: {encoding}")
    
    if encoding is None:
        print("Could not detect encoding.")
        sys.exit(1)

    # Check if the bank is implemented
    if bank == 'mbank':
        print(f"Processing for: {bank}")
        
        header_start_line = find_header_start(input_file, encoding)
        print(f"Data starts at line: {header_start_line}")

        # Read the CSV using pandas with the detected encoding
        try:
            data = pd.read_csv(input_file, encoding="cp1250", sep=";", engine='python', index_col=False, skiprows=header_start_line-1)
            print(f"Successfully read the CSV file with {len(data)} rows.")
            
            # Remove empty rows
            data.dropna(how='all', inplace=True)

            # Remove rows containing 'Saldo końcowe' or legal information
            data = data[~data.apply(lambda row: row.astype(str).str.contains('Saldo końcowe').any(), axis=1)]
            data = data[~data.apply(lambda row: row.astype(str).str.contains('Niniejszy dokument').any(), axis=1)]

            # Drop the last unnamed column if it exists
            data = data.iloc[: , :-1]

            # Clean all spaces from specific columns
            for col in ['#Saldo po operacji', '#Kwota']:
                if col in data.columns:
                    data[col] = data[col].str.replace(" ", "").str.replace("\u00A0", "")

            # Clean redundant spaces from specific columns
            for col in ['#Tytuł', '#Nadawca/Odbiorca', '#Opis operacji']:
                if col in data.columns:
                    # Remove leading/trailing spaces and collapse multiple spaces
                    data[col] = data[col].str.replace(r'\s+', ' ', regex=True).str.strip()

            print(f"Data after cleaning:")
            print(data.head())  # Display the first few rows of the cleaned data


        except Exception as e:
            print(f"Error reading the CSV file: {e}")
            sys.exit(1)

        # Write the QIF output
        with open(output_file, 'w', encoding='utf-8') as qif_file:
            qif_file.write('!Type:Bank\n')

            # Iterate through each row and write to QIF format
            for index, row in data.iterrows():
                date = row['#Data operacji']
                amount = row['#Kwota']
                payee = row['#Nadawca/Odbiorca']
                memo = f"{row['#Opis operacji']} | {row['#Tytuł']}"
                
                qif_file.write(f"D{date}\n")
                qif_file.write(f"T{amount}\n")
                qif_file.write(f"P{payee}\n")
                qif_file.write(f"M{memo}\n")
                qif_file.write("^\n")  # '^' is the end-of-entry marker in QIF

        print(f"QIF file written to: {output_file}")
    else:
        print(f"Bank '{bank}' is not yet implemented.")
        sys.exit(1)  # Exit the script if the bank is not implemented

def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Convert CSV files with bank reports to QIF format.")
    
    # Group 1: Script-related arguments (for input/output file paths)
    script_group = parser.add_argument_group('Script Operations', 'Arguments for handling input/output files')
    script_group.add_argument('-i', '--in', dest='input_file', required=True, help="Path to the input CSV file.")
    script_group.add_argument('-o', '--out', dest='output_file', required=False, help="Path to the output QIF file (optional).")
    
    # Group 2: Bank-related arguments (specific to banks)
    bank_group = parser.add_argument_group('Bank Options', 'Arguments related to bank configuration')
    bank_group.add_argument('-b', '--bank', choices=['mbank', 'mbank-credit','alior', 'santander'], required=True, 
                            help="Specify the bank identifier.\n"
                                 "'mbank' is implemented.\n"
                                 "'mbank-credit' is implemented.\n"
                                 "'alior' and 'santander' are not yet implemented.")
    
    # Parse arguments
    args = parser.parse_args()
    
    if args.output_file is None:
        base_name = os.path.splitext(args.input_file)[0]  # Remove the .csv extension
        args.output_file = f"{base_name}.qif"

    # Call the conversion function
    csv_to_qif(args.input_file, args.output_file, args.bank)
    
if __name__ == "__main__":
    main()
