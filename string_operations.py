def remove_prefix(prefix, response):
    if response[: len(prefix)] == prefix:
        return response[len(prefix) :]
    else:
        return response


def remove_suffix(suffix, response):
    if response[-len(suffix) :] == suffix:
        return response[: -len(suffix)]
    else:
        return response
