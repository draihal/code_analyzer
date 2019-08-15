# Description
>  Get most common function name from path to your code.

## Installation

clone the repo:
```
git clone https://github.com/draihal/func_name_parser
cd func_name_parser
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

## Usage example

example.py:
```
from func_name_parser import FuncNameParser


path = 'D:\\py\\otus\\pyweb\\01\\'


# a - get all most common words in any names in path
# v - get most common verbs in function names in path
# w - get most common words in functions names in path
my_lookup = 'v'  # default v


# default .\
my_projects = (
    'django',
    'flask',
    'pyramid',
    'reddit',
    'requests',
    'sqlalchemy',
)


# default 10
my_top_size = 15


# default = 100
my_len_filenames = 100


report = FuncNameParser(
    path,
    lookup=my_lookup,
    projects=my_projects,
    top_size=my_top_size,
    len_filenames=my_len_filenames
).parse()

for word, count in report:
    print(word, count)
# or print all
print(report)
```
---
running tests:
```$ python setup.py test```
