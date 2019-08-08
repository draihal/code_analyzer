# Description

>  Get most common function name from path to your code.

## Usage
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
example.py:
```
from func_name_parser.core import FuncNameParser


path = 'D:\\py\\otus'
my_projects = (  # default .\
    'django',
    'flask',
    'pyramid',
    'reddit',
    'requests',
    'sqlalchemy',
)
my_top_size = 15  # default 10
stats = FuncNameParser(path, projects=my_projects, top_size=my_top_size)
```
---
running tests:
```$ python setup.py test```
