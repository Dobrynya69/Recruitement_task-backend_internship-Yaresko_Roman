import unittest
import sqlite3
import os
from components import management
from components import commands

class TestCommands(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(f"{management.BASE_DIR}/database/testing_database.sqlite")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
                       CREATE TABLE IF NOT EXISTS
                       parents(
                           firstname CHAR(255),
                           phone_number CHAR(9) PRIMARY KEY,
                           email VARCHAR(255) UNIQUE,
                           password VARCHAR(255),
                           role CHAR(255),
                           created_at DATETIME
                        );""")
        self.cursor.execute("""
                       CREATE TABLE IF NOT EXISTS
                       children(
                           child_id INTEGER PRIMARY KEY,
                           age INTEGER,
                           name CHAR(255),
                           parent_number CHAR(9),
                           FOREIGN KEY(parent_number) REFERENCES parents(phone_number)
                        );""")
        dictionary_data = {
            "parents": [{"firstname": "name1",
                         "telephone_number": "000000001",
                         "email": "name1@gmail.com",
                         "password": "password1",
                         "role": "user",
                         "created_at": "2023-05-04 10:09:14"},
                        {"firstname": "name2",
                         "telephone_number": "000000002",
                         "email": "name2@gmail.com",
                         "password": "password2",
                         "role": "admin",
                         "created_at": "2023-05-05 10:09:14"}],
            "children": [{"name": "child1",
                          "age": "5",
                          "parent_number": "000000001"},
                         {"name": "child2",
                          "age": "8",
                          "parent_number": "000000001"},
                         {"name": "child3",
                          "age": "5",
                          "parent_number": "000000002"},
                         {"name": "child4",
                          "age": "2",
                          "parent_number": "000000002"},]
        }
        for parent in dictionary_data["parents"]:
            self.cursor.execute(f"""
                                INSERT INTO parents
                                VALUES(
                                    '{parent["firstname"]}',
                                    '{parent["telephone_number"]}',
                                    '{parent["email"]}',
                                    '{parent["password"]}',
                                    '{parent["role"]}',
                                    '{parent["created_at"]}'
                                );""")
        self.connection.commit()
        for child in dictionary_data["children"]:
            self.cursor.execute(f"""
                                INSERT INTO children (name, age, parent_number)
                                VALUES(
                                    '{child["name"]}',
                                    {child["age"]},
                                    '{child["parent_number"]}'
                                );""")
        self.connection.commit()
        self.executer = commands.CommandsExecuter("test", {"login": "000000002", "password": "password2"}, "testing_database.sqlite")


    def tearDown(self):
        os.remove(f"{management.BASE_DIR}/database/testing_database.sqlite")


    def test_print_all_accounts(self):
        self.assertEqual(self.executer.print_all_accounts(), "2\n")


    def test_print_oldest_account(self):
        right_string = "name: name1\nemail_address: name1@gmail.com\ncreated_at: 2023-05-04 10:09:14\n"
        self.assertEqual(self.executer.print_oldest_account(), right_string)


    def test_group_by_age(self):
        right_string = "age: 2, count: 1\nage: 5, count: 2\nage: 8, count: 1\n"
        self.assertEqual(self.executer.group_by_age(), right_string)


    def test_print_children(self):
        right_string = "child3, 5\nchild4, 2\n"
        self.assertEqual(self.executer.print_children(), right_string)


    def test_find_similar_children_by_age(self):
        right_string = "name1, 000000001: child1, 5\n"
        self.assertEqual(self.executer.find_similar_children_by_age(), right_string)


if __name__ == '__main__':
    unittest.main()
