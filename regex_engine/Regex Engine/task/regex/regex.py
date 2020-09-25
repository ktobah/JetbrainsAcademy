# write your code here
from typing import Union


def handle_question_symbol(regex: str, input_str: str) -> Union[bool, str]:
    """
    check if the provided regex, which has a ? symbol, matches any part of the input string.

    :param regex: regex pattern
    :param input_str: input string
    :return: either there is a match or not
    """
    if regex[regex.index("?") - 1] not in input_str:
        return check_regex(regex[regex.index("?") + 1:], input_str)
    else:
        char_frequency = input_str.count(regex[regex.index("?") - 1])
        if char_frequency == 1:
            return check_regex(regex[regex.index("?") + 1:], input_str[1:]) if regex[regex.index("?") - 1] == input_str[
                0] else False
        else:
            return "Twice"


def handle_plus_symbol(regex: str, input_str: str) -> bool:
    """
    check if the provided regex, which has a + symbol, matches any part of the input string.

    :param regex: regex pattern
    :param input_str: input string
    :return: either there is a match or not
    """
    if regex[regex.index("+") - 1] in input_str:
        char_frequency = input_str.count(regex[regex.index("+") - 1])
        if char_frequency == 1:
            return check_regex(regex[regex.index("+") + 1:], input_str[1:]) if regex[regex.index("+") - 1] == input_str[
                0] else False
        else:
            return check_regex(regex, input_str[1:]) if regex[regex.index("+") - 1] == input_str[0] else False
    elif regex[regex.index("+") - 1] == ".":
        if regex[regex.index("+") + 1] in input_str[regex.index("+") + 1:]:
            index = input_str[regex.index("+") + 1:].index(regex[regex.index("+") + 1]) + regex.index("+") + 1
            input_str = input_str[index:]
            regex = regex[regex.index("+") + 1:]
            return check_regex(regex, input_str) if len(regex) == len(input_str) else False
        else:
            return False


def handle_asterisk_symbol(regex: str, input_str: str) -> bool:
    """
    check if the provided regex, which has a * symbol, matches any part of the input string.

    :param regex: regex pattern
    :param input_str: input string
    :return: either there is a match or not
    """
    if regex[regex.index("*") - 1] not in input_str:
        return check_regex(regex[regex.index("*") + 1:], input_str)
    return check_regex(regex, input_str[1:]) if regex[regex.index("*") - 1] == input_str[0] else False


def check_regex(regex: str, input_str: str, back_slash: bool = False) -> bool:
    """
    check if the provided regex matches any part of the input string.

    :param regex: regex pattern
    :param input_str: input string
    :param back_slash: whether a backslash is present
    :return: either there is a match or not
    """
    if regex == "":
        return True
    elif input_str == "":
        return False
    elif not back_slash:
        if regex[0] == ".":
            return True
        elif "?" in regex and regex[regex.index("?") - 1] != "\\":
            return handle_question_symbol(regex, input_str)
        elif "*" in regex and regex[regex.index("*") - 1] != "\\":
            return handle_asterisk_symbol(regex, input_str)
        elif "+" in regex and regex[regex.index("+") - 1] != "\\":
            return handle_plus_symbol(regex, input_str)
    # handle the case of \
    if "\\" in regex and "\\" not in input_str:
        regex = regex.replace("\\", "")
    if regex[0] != input_str[0]:
        return False
    else:
        return check_regex(regex[1:], input_str[1:], back_slash)


def launcher(regex: str, inp_str: str) -> bool:
    """
    Acts as the entry point of the program.

    :param regex: regex pattern
    :param inp_str: input string
    :return: either there is a match or not
    """
    back_slash = False
    if regex == "":
        return True
    elif inp_str == "":
        return False
    elif "\\" in regex:
        back_slash = True
        if "\\" in inp_str:
            inp_str = inp_str.replace('\\', '\\\\')
    for i in range(len(inp_str)):
        if regex[0] == "^" and regex[-1] == "$":
            if " " not in inp_str:
                regex = regex[1:-1]
            else:
                return False
        if regex[0] == "^" and ("*" not in regex and "." not in regex and "+" not in regex):
            return check_regex(regex[1:], inp_str, back_slash)
        if regex[0] == "^":
            regex = regex[1:]
        if regex[-1] == "$":
            return check_regex(regex[:-1][::-1], inp_str[::-1], back_slash)

        result = check_regex(regex, inp_str, back_slash)
        if result == "Twice":
            return False
        elif result:
            return True
        else:
            inp_str = inp_str[1:]
    return False


# read the input
regex, input_string = input().split('|')
print(launcher(regex, input_string))
