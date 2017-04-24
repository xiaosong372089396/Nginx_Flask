#encoding: utf-8
import os
import hashlib

def md5_str(s):
    md5 = hashlib.md5()
    md5.update(s)
    return md5.hexdigest()

def md5_file(path):
    if not os.path.exists(path):
        raise BaseException('file not found') 
    h = open(path, 'r')
    md5 = hashlib.md5()

    while 1:
        k = h.read(1024)
        if k == '':
            break
        md5.update(k)

    h.close()
    return md5.hexdigest()


if __name__ == '__main__':
    usage = '''
    python utils.py str xxxx
    python utils.pyt file xxxxx
'''
    import sys
    if len(sys.argv) >= 3:
        if sys.argv[1] == 'str':
           print md5_str(sys.argv[2]) 
        elif sys.argv[1] == 'file':
           print md5_file(sys.argv[2])
        else:
           print usage
    else:
        print usage
    
