import re
import string


def post_process_token_list(token_list):
    """
        Post process a token list after tokenization
        Parameter : token_list [str]
        return  processed token list
    """
    out = []
    for token in token_list:
        if is_punc(token):
            continue
        elif is_number(token):
            out.append("xxnum")
        else:
            out.append(token.strip().lower())
    return out



def is_punc(text: str) -> bool:
    """check whether the text is a punctuation"""
    return all(map(lambda ch: (ch in string.punctuation+ " "), text))


def is_number(text: str) -> bool:
    """check whether the text is a number"""

    return all(
        map(
            lambda ch: (ch in "0123456789๐๑๒๓๔๕๖๗๘๙"),
            filter(lambda ch: not (ch in string.punctuation), text)
        )
    )

