import re


def pre_process_text(text: str) -> str:
    """
        Preprocess the given thai text
        before feeding in Anything

        :param str text: text to preprocess
        :return: str
    """
    functions = [
        rm_crlf,
        rm_repeated_consonants,
        standardize_vowels_order,
        add_space_between_delimiters,
        rm_repeated_spaces,
        rm_repeated_newlines,
        rm_brackets,
        replace_url,
    ]
    for function in functions:
        text = function(text)
    return text


def rm_crlf(text: str) -> str:
    """Change CRLF to LF"""
    return re.sub(r"\r\n", "\n", text)


def replace_url(text: str) -> str:
    """Replace url in `text` with xxurl """
    URL_PATTERN = r"""http(s?):[^ \n\r\t]*"""
    return re.sub(URL_PATTERN, "xxurl", text)


def add_space_between_delimiters(text: str) -> str:
    """Add spaces around / and # in `t`."""
    return re.sub(r"([/#\n])", r" \1 ", text)


def rm_repeated_consonants(text: str) -> str:
    """
    Replace repetitions at the character level in `text` after the repetition.

    :Example:
        >>> text = "กาาาาาาา"
        >>> replace_rep_after(text)
        'กา'
    """

    def _replace_rep(m):
        c, cc = m.groups()
        return f"{c} "
    re_rep = re.compile(r"(\S)(\1{3,})")
    return re_rep.sub(_replace_rep, text)

    "Remove CRLF to LF"
    return re.sub(r"\r\n", "\n", text)


def rm_repeated_newlines(text: str) -> str:
    "Remove multiple newlines in `text`."
    return re.sub(r"[\n]{2,}", " ", text)


def rm_repeated_spaces(text: str) -> str:
    """Remove multiple spaces in `text`. (code from `fastai`)"""
    return re.sub(" {2,}", " ", text)


def rm_brackets(text: str) -> str:
    "Remove all empty brackets from `text`."
    text = re.sub(r"\(\)", "", text)
    text = re.sub(r"\{\}", "", text)
    text = re.sub(r"\[\]", "", text)
    return text


def standardize_vowels_order(text: str) -> str:
    """
    Standardizing vowel sequence like เ + เ => แ
    :Example:
    ::

        from pythainlp.util import normalize

        normalize('สระะน้ำ')
        # output: สระน้ำ

        normalize('เเปลก')
        # output: แปลก

        normalize('นานาาา')
        # output: นานา
    """
    THAI_VOWELS = [
        "ะ", "ั", "็", "า", "ิ", "ี", "ึ", "่", "ํ", "ุ", "ู",
        "ใ", "ไ", "โ", "ื", "่", "้", "๋", "๊", "ึ", "์", "๋", "ำ",
    ]
    NORMALIZE_RULES = [
        ("เเ", "แ"),  # เ เ -> แ
        ("ํ(t)า", "\\1ำ"),
        ("ํา(t)", "\\1ำ"),
        ("([่-๋])([ัิ-ื])", "\\2\\1"),
        ("([่-๋])([ูุ])", "\\2\\1"),
        ("ำ([่-๋])", "\\1ำ"),
        ("(์)([ัิ-ู])", "\\2\\1"),
    ]
    for pattern, sub in NORMALIZE_RULES:
        text = re.sub(pattern.replace("t", "[่้๊๋]"), sub, text)
    for vowel in THAI_VOWELS:
        # get rid of double vowels again
        text = re.sub(vowel + "+", vowel, text)
    return text
