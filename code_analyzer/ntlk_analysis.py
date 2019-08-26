import logging

from nltk import download as download_nltk_data, pos_tag


def _is_verb(word):
    """
    Returns the boolean value of whether the word is a verb.
    :param word: word
    :return: boolean - True or False
    """
    if not word:
        return False
    try:
        pos_info = pos_tag([word])
        return pos_info[0][1] == 'VB'
    except LookupError:
        logging.warning("Download nltk data.")
        download_nltk_data('averaged_perceptron_tagger')
        pos_info = pos_tag([word])
        return pos_info[0][1] == 'VB'


def _is_nouns(word):
    """
    Returns the boolean value of whether the word is a nouns.
    :param word: word
    :return: boolean - True or False
    """
    if not word:
        return False
    try:
        pos_info = pos_tag([word])
        return pos_info[0][1] == 'NN'
    except LookupError:
        logging.warning("Download nltk data.")
        download_nltk_data('averaged_perceptron_tagger')
        pos_info = pos_tag([word])
        return pos_info[0][1] == 'NN'


def _get_verbs_from_function_name(function_name):
    """
    Returns list with verb.
    :param function_name: function name
    :return: lists with verb
    """
    return [word for word in function_name.split('_')
            if _is_verb(word)]


def _get_nouns_from_function_name(function_name):
    """
    Returns list with nouns.
    :param function_name: function name
    :return: lists with nouns
    """
    return [word for word in function_name.split('_')
            if _is_nouns(word)]
