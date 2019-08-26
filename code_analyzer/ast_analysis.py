import ast
import logging


def _get_all_names(tree):
    """
    Returns list of all words.
    :param tree: _ast.Module object
    :return: list with words
    """
    return [node.id for node in ast.walk(tree)
            if isinstance(node, ast.Name)]


def _get_all_func_names(tree):
    """
    Returns list of all words.
    :param tree: _ast.Module object
    :return: list with words
    """
    return [node.name.lower() for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)]


def _generate_trees(filename, with_filenames=False, with_file_content=False):
    """
    Generated trees.
    :param filename: filename
    :param with_filenames: boolean
    :param with_file_content: boolean
    :return: list of ast object
    """
    trees = []
    with open(filename, 'r', encoding='utf-8') as attempt_handler:
        main_file_content = attempt_handler.read()
    try:
        tree = ast.parse(main_file_content)
    except SyntaxError as e:
        logging.exception("Exception occurred.")
        tree = None
    if with_filenames:
        if with_file_content:
            trees.append((filename, main_file_content, tree))
        else:
            trees.append((filename, tree))
    else:
        trees.append(tree)
    return trees
