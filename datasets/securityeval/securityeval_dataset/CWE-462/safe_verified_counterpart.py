def foo():
    return "./", "file.txt"


def dataSorting():
    '''
    Continuously take (basename,data) key-value pair from foo() function and sort it
    '''
    alist_dict = {}
    basename, data = (True, True)
    while basename and data:
        (basename, data) = foo()
        if basename and data:
            alist_dict[basename] = data
    
    alist = sorted(alist_dict.items())