# Code Analyzer

## Description
>  Get most common words from your code in cli.

## Installation

clone the repo:
```
git clone https://github.com/draihal/code_analyzer
cd code_analyzer
```
create virtual environment and install package in it:
```
python -m venv venv
source venv/bin/activate or venv\Scripts\activate (on Win)
python setup.py install
```
or install package global:
```
python setup.py install
```
to uninstall:
```
pip uninstall code_analyzer
```

## Usage example
Type in cli:
```
code_analizer -h
```
```
usage: code_analyzer [-p PATH] [-l {v,w,a}] [-pr PROJECTS] [-s TOP_SIZE]
                     [-lf LEN_FILENAMES] [--help] [--version]

Get most common words from your code.

optional arguments:
  -p PATH, --path PATH  Path to the code directory
  -l {v,w,a}, --lookup {v,w,a}
  -pr PROJECTS, --projects PROJECTS
  -s TOP_SIZE, --top_size TOP_SIZE
  -lf LEN_FILENAMES, --len_filenames LEN_FILENAMES
  --help, -h            Help
  --version             Version
```
---
running tests:
```$ python setup.py test```
