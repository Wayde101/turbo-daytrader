# client.py
import srcinfo

if __name__ == '__main__':
    try:
    # Whatever.
        raise Exception, "hello"
    except Exception, x:
        print ('warning: %s: %d: %s' %
            (srcinfo.file(), srcinfo.line(), x))
