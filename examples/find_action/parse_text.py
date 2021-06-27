def _check_main_syntax(plain_text):

    text = plain_text.replace(" ", "")

    idx = text.find("=>")
    if idx != -1:
        function_and_arguments = text[:idx]
        return_values = text[idx + 2:]
    else:
        function_and_arguments = text
        return_values = None

    #print("left:", function_and_arguments)
    #print("right:", return_values)

    if (function_and_arguments.find("(") == -1 or
            function_and_arguments.find(")") == -1):
        raise Exception("Wrong FUNCTION_DEFINITION syntax, missed parenthesis after name")

    if return_values is not None:
        if (return_values.find("(") == -1 or
                return_values.find(")") == -1):
            raise Exception("Wrong RETURN_VALUE syntax, missed parenthesis")
        elif return_values.find("(") == (return_values.find(")") - 1):
            raise Exception("Wrong RETURN_VALUE syntax, any value between parenthesis")

    return text


def _extract_function_name(text):
    return text[:text.find("(")]


def _extract_variable(text):
    idx = text.find(":")
    name = text[:idx]
    type_ = text[idx + 1:]
    return name, type_


def _extract_variables(text):
    args_as_list = text.split(',')
    args = {}
    for arg in args_as_list:
        name, type_ = _extract_variable(arg)
        args[name] = type_
    return args


def _extract_function_arguments(text):

    if text.find("(") == -1 or text.find(")") == -1:
        raise Exception("Wrong ARGUMENTS syntax, missed parenthesis")

    args_as_text = text[text.find("(") + 1: text.find(")")]
    if args_as_text == "":
        return None
    else:
        return _extract_variables(args_as_text)


def _extract_function_return_value(text):

    idx = text.find("=>")
    if idx == -1:
        return None

    args_as_text = text[idx + 2:]
    args_as_text = args_as_text[args_as_text.find("(") + 1: args_as_text.find(")")]
    if args_as_text == "":
        raise Exception("Wrong RETURN_VALUE syntax, missed parenthesis")

    return _extract_variables(args_as_text)


def parse_function(text):

    text = _check_main_syntax(text)
    name = _extract_function_name(text)
    arguments = _extract_function_arguments(text)
    return_value = _extract_function_return_value(text)
    return name, arguments, return_value
