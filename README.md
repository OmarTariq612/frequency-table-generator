
# Frequency Table Generator
Program that constructs the frequency table for a given data set.
## Create a virtual environment

```
python -m venv env
```

for *nix systems:
```
source ./env/bin/activate
```

for windows systems:

- powershell:
  ```
  .\env\Scripts\Activate.ps1
  ```
- command prompt:
  ```
  .\env\Scripts\activate.bat
  ```
## Install the dependencies

```
pip install -r requirements.txt
```
```
python freqgen.py --help
```

```
usage: freqgen.py [-h] [-v] [-n N] [-o output_file] input_file

This program constructs the frequency table for a given data set.

positional arguments:
  input_file            the input file, eg: filename.csv or filename.xlsx

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -n N, --classes N     the number of classes required in the frequancy table (default: Sturge's rule)
  -o output_file, --output-file output_file
                        the output file, eg: filename.csv or filename.xlsx (default: stdout)
```


## Examples
- using the default number of classes (`Sturge's rule`) and direct the result to `stdout`:
```
python freqgen.py input/input.csv
```
```
    age  frequency
21 - 28         20
29 - 36         29
37 - 44         17
45 - 52          4
53 - 60          2
61 - 68          2
69 - 76          1
77 - 84          1
```
- specify a number of classes and output the result to `stdout`:
```
python freqgen.py input/input.csv -n 6
```
```
    age  frequency
21 - 30         28
31 - 40         30
41 - 50         12
51 - 60          2
61 - 70          2
71 - 80          2
```
* direct the result to a csv file
```
python freqgen.py input/input.csv -n 6 -o output/output.csv
```
* direct the result to an xlsx file:
```
python freqgen.py input/input.xlsx -n 6 -o output/output.xlsx
```