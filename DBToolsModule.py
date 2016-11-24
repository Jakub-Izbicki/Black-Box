from __future__ import print_function
import sqlite3
import jsonpickle

class DBTools():

    itemsDBName = 'items.db'

    def __init__(self, db_connection_object):
        self.createDBTables(db_connection_object)

    def createDBTables(self, db_connection_object):
        try:
            db_connection_object.execute('CREATE TABLE IF NOT EXISTS Items('
                                            'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
                                            'ItemName TEXT NOT NULL, '
                                            'Path TEXT NOT NULL, '
                                            'ObjectsArray TEXT)')
            db_connection_object.commit()

        except sqlite3.OperationalError:
            print('\n\nERR01: Could not create table \'Items\'\n\n')

    def resetDB(self, db_connection_object):
        try:
            db_connection_object.execute('DROP TABLE IF EXISTS Items')
            db_connection_object.commit()
        except sqlite3.OperationalError:
            print('\n\nERR02: Could not drop table \'Items\'\n\n')

        self.createDBTables(db_connection_object)

    def insertItem(self, db_connection_object, item_name, path, objects_array):

        objects_array_as_str = jsonpickle.encode(objects_array)

        try:
            cursor = db_connection_object.cursor()
            cursor.execute('SELECT * FROM Items WHERE ItemName=\''+item_name+'\'')
            data = cursor.fetchall()

            if len(data) != 0:
                print('\nThe item is already on the list!\n')
                return # TODO: make an appropriate popup for this

            db_connection_object.execute('INSERT INTO Items (ItemName, Path, ObjectsArray)'
                                        'VALUES (\'' + item_name + '\', \'' + path + '\', \'' + objects_array_as_str + '\')')

            db_connection_object.commit()
        except sqlite3.OperationalError:
            print('\n\nERR03: Could not insert item: ' + item_name + '\n\n')

    def printItems(self, db_connection_object):
        cursor = db_connection_object.cursor()

        try:
            query_result = cursor.execute('SELECT id, ItemName, Path, ObjectsArray '
                                          'FROM Items')

            for row in query_result:
                print('id: ' + str(row[0]))
                print('ItemName: ' + row[1])
                print('Path: ' + row[2])
                print('ObjectsArray: ' + row[3])

        except sqlite3.OperationalError:
            print('\n\nERR04: Could not withdraw item\n\n')

    def selectAllItemsDb(self, db_connection_object):
        cursor = db_connection_object.cursor()

        list = []

        try:
            query_result = cursor.execute('SELECT id, ItemName, Path, ObjectsArray '
                                          'FROM Items')



            for row in query_result:
                sublist = []
                sublist.append(row[1])
                sublist.append(row[2])
                sublist.append(row[3])
                list.append(sublist)

        except sqlite3.OperationalError:
            print('\n\nERR05: Could not select all\n\n')

        return list

