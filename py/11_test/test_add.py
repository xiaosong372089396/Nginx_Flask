
import sys

if __name__ == '__main__':
    if len(sys.argv) <= 1: 
        sys.exit(1)
    total = 0
    for i in sys.argv[1:]:
        total += int(i)
    print total
