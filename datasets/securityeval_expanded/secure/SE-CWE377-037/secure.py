from tempfile import mkstemp
import os


def write_results(results):
    '''
    Create a temporary file and write the results to it
    '''
    fd, filename = mkstemp()
    try:
        with os.fdopen(fd, "w") as f:
            f.write(results)
        print("Results written to", filename)
    except:
        os.close(fd)
        raise