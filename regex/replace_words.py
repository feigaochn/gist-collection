def replace_words(text, word_dic):
    """
    replace words in text via a dictionary

    >>> text = 'A Colorful day in city Center.'
    >>> word_dic = {'Color': 'color', 'Center': 'sub'}
    >>> replace_words(text, word_dic)
    'A colorful day in city sub.'
    """
    import re
    yo = re.compile('|'.join(map(re.escape, word_dic)))

    def translate(mat):
        return word_dic[mat.group(0)]
    return yo.sub(translate, text)
