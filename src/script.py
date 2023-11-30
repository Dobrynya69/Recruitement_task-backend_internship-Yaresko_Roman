import sys
from components.management import CommandsManager

def main(*args, **kwargs):
    manager = CommandsManager(sys.argv)
    manager.execute()
    
if __name__ == '__main__':
    main()
