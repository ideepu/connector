import sys

from src.connector import Connector
from src.exception import CoreException

if __name__ == '__main__':
    try:
        Connector().run()
    except CoreException as e:
        print(e)
        sys.exit(1)
