import tempfile


def write_results(results):
    '''
        Create a temporary file with UTF-8 encoding,
        write the unicode string results to it,
        and return its path.
    '''
    tmp_file = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False)
    tmp_file.write(results)
    return tmp_file