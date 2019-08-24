# Code Analyzer

## Description
>  Get most common words from code in cli.

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
usage: code_analyzer [-p PATH] [-g GITHUB_PATH] [-l {v,w,a}] [-pr PROJECTS]
                     [-s TOP_SIZE] [-n NUMBER_FILENAMES] [-o {json,txt,csv}]
                     [-h] [-v]

Get most common words from code.

optional arguments:
  -p PATH, --path PATH  Path to the directory with code to analyse, default
                        current directory
  -g GITHUB_PATH, --github_path GITHUB_PATH
                        The URL to github repository with code to analyse,
                        default None
  -l {v,w,a}, --lookup {v,w,a}
                        Type of analyzing, default "v". "v" - ..., "a" - ...,
                        "w" - ...
  -pr PROJECTS, --projects PROJECTS
                        Dirnames with projects with code to analyse, default
                        current directory
  -s TOP_SIZE, --top_size TOP_SIZE
                        Top amount of words to report, default 10
  -n NUMBER_FILENAMES, --number_filenames NUMBER_FILENAMES
                        Max numbers of filenames to analyse, default 100
  -o {json,txt,csv}, --output_format {json,txt,csv}
                        Output report file format to current directory,
                        default output to cli
  -h, --help            Help
  -v, --version         Version
```
---
running tests:
```$ python setup.py test```
