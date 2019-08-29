import collections


def _is_dunder(name):
    """
    Return boolean if a name is a dunder method.
    Like this: __name__.

    :param name: name
    :return: boolean - True or False
    """
    return name.startswith("__") and name.endswith("__")


def _convert_tpls_to_lst(list_of_tuple):
    """
    Convert list of tuples to list.
    [(1,2), (3,4)] -> [1, 2, 3, 4]

    :param list_of_tuple: list of tuple
    :return: list
    """
    return (item for tuple_ in list_of_tuple for item in tuple_)


def _get_count_most_common(list_words, top_size):
    """
    Return a list of tuples with words and his counts.

    :param list_words: list of words
    :param top_size: number of top words
    :return: list of tuples with words and his counts
    """
    return collections.Counter(list_words).most_common(top_size)


def _get_converted_names(trees, func):
    """
    Return a list of words.

    :param trees: list of _ast.Module object
    :param func: function
    :return: list with words
    """
    return (word
            for word in _convert_tpls_to_lst((func(tree) for tree in trees))
            if not _is_dunder(word))
