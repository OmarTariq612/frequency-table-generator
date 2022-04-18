"""
Assignment
==============
- Problem Statement:
    Write a program that constructs the frequency table for a given data set
Professor: Dr. Abdallah
Department: Computers And Systems Engineering
"""

import pandas as pd
import argparse
from math import ceil, floor, log2
from bisect import bisect_right
import enum
import os, os.path

# the supported extension for reading
class Readers(enum.Enum):
    CSV = enum.auto()
    XLSX = enum.auto()

class Reader:
    def __init__(self, filename: str):
        self.filename = filename
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        if ext == ".csv":
            self.type = Readers.CSV
        elif ext == ".xlsx":
            self.type = Readers.XLSX
        else:
            raise TypeError(f"({ext}) extension is not supported")

# the supported extension for writing
class Writers(enum.Enum):
    CSV = enum.auto()
    XLSX = enum.auto()
    STDOUT = enum.auto()

class Writer:
    def __init__(self, filename: str):
        self.filename = filename
        if filename is None:
            self.type = Writers.STDOUT
        else:
            _, ext = os.path.splitext(filename)
            ext = ext.lower()
            if ext == ".csv":
                self.type = Writers.CSV
            elif ext == ".xlsx":
                self.type = Writers.XLSX
            else:
                raise TypeError(f"({ext}) extension is not supported")

def generate_freq_table(reader: Reader, writer: Writer, n_classes: int = None) -> None:
    if reader.type == Readers.XLSX:
        dataframe = pd.read_excel(reader.filename)
    elif reader.type == Readers.CSV:
        dataframe = pd.read_csv(reader.filename)

    column_name = dataframe.columns[0] # read the name of the first column
    arr = dataframe.values.flatten()
    arr.sort()
    min_value, max_value = floor(arr.min()), ceil(arr.max())

    if n_classes is None:
        n_classes = ceil(1 + log2(arr.size)) # apply Sturge's rule
    class_width = ceil((max_value - min_value) / n_classes)
    start = min_value
    index = 0
    slices = [""] * n_classes
    freqs = [0] * n_classes
    data = {column_name: slices, "frequency": freqs}

    for i in range(n_classes - 1):
        curr_index = bisect_right(arr, start + class_width - 1, index)
        freq = curr_index - index
        index = curr_index
        slices[i] = f"{start} - {start + class_width - 1}"
        freqs[i] = freq
        start += class_width
    
    max_value = max(max_value, start + class_width - 1)
    freq = bisect_right(arr, max_value, index) - index
    slices[-1] = f"{start} - {max_value}"
    freqs[-1] = freq

    df = pd.DataFrame(data=data)

    if writer.type == Writers.XLSX:
        with pd.ExcelWriter(writer.filename) as excel_writer:
                df.to_excel(excel_writer, index=False, sheet_name="freq table")
    elif writer.type == Writers.CSV:
        df.to_csv(writer.filename, index=False)
    elif writer.type == Writers.STDOUT:
        print(df.to_string(index=False))

def main() -> None:
    parser = argparse.ArgumentParser(description="This program constructs the frequency table for a given data set.")
    parser.add_argument("input_file", help="the input file, eg: filename.csv or filename.xlsx")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s version: 0.1")
    parser.add_argument("-n", "--classes", metavar="N", type=int, help="the number of classes required in the frequancy table (default: Sturge's rule)")
    parser.add_argument("-o", "--output-file", metavar="output_file", type=str, help="the output file, eg: filename.csv or filename.xlsx (default: stdout)")
    args = parser.parse_args()

    # assert that the input_file is a valid file
    if not os.path.isfile(args.input_file):
        raise argparse.ArgumentTypeError(f"input_file: \"{args.input_file}\" is not found")

    reader = Reader(args.input_file)
    writer = Writer(args.output_file)

    # assert that the input_file is not the same as the output_file
    if (writer.type != Writers.STDOUT) and (os.path.isfile(args.output_file)):
        if os.path.samefile(args.input_file, args.output_file):
            raise argparse.ArgumentTypeError(f"input_file and output_file must not be the same file")

    generate_freq_table(reader, writer, args.classes)

if __name__ == "__main__":
    main()