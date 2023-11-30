import os

class CommandsManager:
    ALLOWED_COMMANDS = ["command1",
                        "command2",
                        "command3",
                        "create_database"]

    def __init__(self, argv, *args, **kwargs):
        try:
            if argv[1] in CommandsManager.ALLOWED_COMMANDS:
                self.command = argv[1]
            else:
                raise SystemExit("This command is not allowed")
        except IndexError:
            raise SystemExit("Please enter your command")
        self.variables = self._get_variables(argv)
        if self.command != "create_database" and not os.path.exists("database/database.db"):
            raise SystemExit("Please create the database first by calling the 'create_database' command")


    def _get_variables(self, argv):
        variables = {}
        for index in range(1, len(argv)):
            if "--" in argv[index]:
                try:
                    if "--" not in argv[index + 1]:
                        variables[argv[index][2:]] = argv[index + 1]
                    else:
                        raise SystemExit("Variable wasn`t added in the right way")
                except IndexError:
                    raise SystemExit("Variable wasn`t added in the right way")
        return variables


    def execute(self):
        pass