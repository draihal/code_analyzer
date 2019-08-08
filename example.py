from func_name_parser.core import FuncNameParser


path = 'D:\\py\\otus\\pyweb\\01\\'
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
