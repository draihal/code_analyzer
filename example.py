from func_name_parser.core import FuncNameParser


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


FuncNameParser(path, lookup=my_lookup, projects=my_projects, top_size=my_top_size)
