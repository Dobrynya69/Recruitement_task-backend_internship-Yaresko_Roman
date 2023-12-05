import os
from components.commands import CommandsExecuter
from pathlib import Path

ALLOWED_COMMANDS = {"print-all-accounts": ["login", "password"],
                    "print-oldest-account": ["login", "password"],
                    "group-by-age": ["login", "password"],
                    "print-children": ["login", "password"],
                    "find-similar-children-by-age": ["login", "password"],
                    "create-database": []}

BASE_DIR = Path(__file__).resolve().parent.parent

class CommandsManager:
    
    def __init__(self, argv, *args, **kwargs):
        try:
            if argv[1] in ALLOWED_COMMANDS.keys():
                self.command = argv[1]
            else:
                raise SystemExit("This command is not allowed")
        except IndexError:
            raise SystemExit("Please enter your command")
        self.arguments = self._get_arguments(argv)
        if self.command != "create-database" and not os.path.exists(f"{BASE_DIR}/database/database.sqlite"):
            raise SystemExit("First create the database by calling the create-database command.")


    def _get_arguments(self, argv):
        arguments = {}
        for index in range(1, len(argv)):
            if "--" in argv[index]:
                try:
                    if "--" not in argv[index + 1]:
                        arguments[argv[index][2:]] = argv[index + 1]
                    else:
                        raise SystemExit("Argument wasn`t added in the right way")
                except IndexError:
                    raise SystemExit("Argument wasn`t added in the right way")
        return arguments


    def execute(self):
        executer = CommandsExecuter(self.command, self.arguments, "database.sqlite")
        executer.call_command()
