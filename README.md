# name and surname: Roman Yaresko
#### To run the script you need to install 'pandas' and 'xmltodict'. All commands must be entered inside the src folder.
##### You can run unit tests by typing
>python -m unittest tests/test_command.py
##### Before running any command in order to create the database and parse the data, you also have to type
>python script.py create-database
##### The rest of the commands should be done like this (if you wish, you can swipe the “login” and “password”):
>python script.py <command> --login "<user_login>" --password "<user_password>"
##### For testing you can use these two accounts: ADMIN - login: 762084369; password: #_ILaeXdj0 | CASUAL USER - login: 203818382; password: gk2VM$qk@S
##### Here is the list of commands:
- print-all-accounts (only admin)
- print-oldest-account (only admin)
- group-by-age (only admin)
- print-children
- find-similar-children-by-age
