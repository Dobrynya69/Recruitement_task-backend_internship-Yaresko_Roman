import os
import sqlite3
import pandas
import xmltodict
import xml.etree.ElementTree as ET
import json
import re
from components import management

class CommandsExecuter:
    def __init__(self, command, arguments, *args, **kwargs):
        self.command = command
        self.arguments = arguments

    def call_command(self):
        if list(self.arguments.keys()) == self._get_arguments_list():
            if self.command == "print-all-accounts":
                pass
            elif self.command == "print-oldest-account":
                pass
            elif self.command == "group-by-age":
                pass
            elif self.command == "print-children":
                pass
            elif self.command == "find-similar-children-by-age":
                pass
            elif self.command == "create-database":
                self._create_database()
            elif self.command == "test":
                pass
            else:
                raise SystemExit("This command is not allowed")
        else:
           raise SystemExit(f"You entered not valid arguments for this particular command.\
                            The right arguments is: '{self._get_arguments_list()}'\
                            Your arguments is: '{self.arguments.keys()}'") 


    def _get_arguments_list(self):
        try:
            return management.ALLOWED_COMMANDS[self.command]
        except IndexError:
            raise SystemExit("This command is not allowed")


    def _create_database(self):
        if not os.path.exists(f"{management.BASE_DIR}/database/database.db"):
            connection = sqlite3.connect(f"{management.BASE_DIR}/database/database.db")
            cursor = connection.cursor()
            self._create_database_tables(cursor)
            parser = DataParser(cursor)
            parser.parse()
            print("Database has been created")
        else:
            print("Database is already exists")


    def _create_database_tables(self, cursor: sqlite3.Cursor):
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS
                       parents(
                           firstname CHAR(255),
                           phone_number INTEGER UNIQUE,
                           email VARCHAR(255) PRIMARY KEY,
                           password VARCHAR(255),
                           role CHAR(255),
                           created_at DATETIME
                        );""")
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS
                       children(
                           child_id INTEGER PRIMARY KEY,
                           age INTEGER,
                           name CHAR(255),
                           parent_email VARCHAR(255),
                           FOREIGN KEY(parent_email) REFERENCES parents(email)
                        );""")


class DataParser:
    def __init__(self, cursor: sqlite3.Cursor, *args, **kwargs):
        self.cursor = cursor

    def parse(self):
        dictionary_data = self._get_dictionary_data()
        self._insert_db(dictionary_data["parents"])
        self._insert_db(dictionary_data["children"])


    def _get_dictionary_data(self):
        dictionary_data = []
        dictionary_data += self._parse_csv(f"{management.BASE_DIR}/data/users_1.csv")
        dictionary_data += self._parse_csv(f"{management.BASE_DIR}/data/users_2.csv")
        dictionary_data += self._parse_xml(f"{management.BASE_DIR}/data/users_1.xml")
        dictionary_data += self._parse_xml(f"{management.BASE_DIR}/data/users_2.xml")
        dictionary_data += self._parse_json(f"{management.BASE_DIR}/data/users.json")
        print(dictionary_data)


    def _parse_csv(self, path):
        csv_df = pandas.read_csv(path, sep=";")
        csv_data = csv_df.to_dict(orient='records')
        for user in csv_data:
            if type(user["children"]) is str:
                children = []
                print(user["children"])
                for child in user["children"].split(","):
                    child_split = child.split(" ")
                    child = {"name": child_split[0], "age": re.sub("[()]", "", child_split[1])}
                    children.append(child)
                user["children"] = children
        return csv_data


    def _parse_xml(self, path):
        tree = ET.parse(open(path, "r"))
        xml_tree = tree.getroot()
        xmlstr = ET.tostring(xml_tree, encoding='utf-8', method='xml')
        xml_dict = dict(xmltodict.parse(xmlstr))
        xml_data = []
        for user in dict(xml_dict["users"])["user"]:
            if user["children"]:
                user["children"] = dict(dict(user["children"])["child"])
            xml_data.append(dict(user))
        return xml_data


    def _parse_json(self, path):
        return json.load(open(path, "r"))


    def _insert_db(self, dictionary_data):
        pass

