# coding=utf-8
import mysql.connector as mariadb

from config import username, password, database_name
import database_config
tables = database_config.tables().names_dict


class Table:

    def __init__(self, name, logging=False):
        self.mariadb_connection = mariadb.connect(user=username, password=password, database=database_name)
        self.cursor = self.mariadb_connection.cursor(buffered=True)

        self.table_name = name
        self.logging = logging
        # self.send_query("SET collation_connection = 'utf8_general_ci';")

    def brackets(self, string):
        string = """ """ + """`""" + string + """`"""
        return string

    def toArray(self, *objs):
        objects = []
        for obj in objs:
            if type(obj) is list:
                objects.append(obj)
            else:
                objects.append([obj])
        if len(objects) == 1:
            objects = objects[0]
        return objects

    def create(self, fields, types):

        fields, types = self.toArray(fields, types)
        fields_with_types = [fields[i] + " " + type_ for i, type_ in enumerate(types)]

        query = "CREATE TABLE IF NOT EXISTS {table_name} ({fields_with_types})".format(
            table_name=self.brackets(self.table_name),
            fields_with_types=", ".join(fields_with_types)
        )

        # print (query)

        self.send_query(query)


    def insert(self, fields, values):

        fields, values = self.toArray(fields, values)

        values = ["'{value}'".format(value=value) for value in values]
        # while values.find('None') != -1:
        #     values[values.find('None')] = "NULL"

        query = "INSERT INTO {table_name} ({parameters}) VALUES ({values})".format(
            table_name=self.brackets(self.table_name),
            parameters=", ".join(fields),
            values=", ".join(values).replace("'None'", "NULL") ### ))))
        )

        self.send_query(query)

    def update(self, key_fields, key_values, upd_fields, upd_values):

        key_fields, key_values, upd_fields, upd_values = self.toArray(key_fields, key_values, upd_fields, upd_values)

        # keys = [field + " = " + "'" + str(key_values[i]) + "'" for i, field in enumerate(key_fields)]
        keys = ["{field} = '{value}'".format(
            field=field,
            value=key_values[i]
        ) for i, field in enumerate(key_fields)]

        updates = ["{field} = '{value}'".format(
            field=field,
            value=upd_values[i]
        ) for i, field in enumerate(upd_fields)]

        query = "UPDATE {table_name} SET {changes} WHERE {keys}".format(
            table_name=self.brackets(self.table_name),
            changes=", ".join(updates),
            keys=" and ".join(keys)
        )

        self.send_query(query)

    def turple_to_array(self, object):
        for i, tuple in enumerate(object):
            object[i] = list(tuple)
        return object

    def exist(self, key_fields, key_values):

        # SELECT EXISTS(SELECT id FROM table WHERE id = 1)

        key_fields, key_values = self.toArray(key_fields, key_values)

        keys = ["{field} = '{value}'".format(
            field=field,
            value=key_values[i]
        ) for i, field in enumerate(key_fields)]

        query = "SELECT EXISTS(SELECT {field} FROM {table_name} WHERE {keys})".format(
            field=key_fields[0],
            table_name=self.brackets(self.table_name),
            keys=" and ".join(keys)
        )
        return self.send_query(query, True)[0][0]

    def to_dict(self, fields, objects_data):
        oblects = []

        for object_data in objects_data:
            oblect = {}
            for i, field in enumerate(fields):
                oblect[field] = object_data[i]
            oblects.append(oblect)

        return oblects

    def select(self, fields, key_fields, key_values, to_dict = False):

        fields, key_fields, key_values = self.toArray(fields, key_fields, key_values)

        keys = ["{field} = '{value}'".format(
            field=field,
            value=key_values[i]
        ) for i, field in enumerate(key_fields)]

        query = "SELECT {fields} FROM {table_name} WHERE {keys}".format(
            fields=", ".join(fields),
            table_name=self.brackets(self.table_name),
            keys=" and ".join(keys)
        )
        data = self.send_query(query, True)
        if to_dict:
            return self.to_dict(fields, data)
        else:
            return self.turple_to_array(data)

    def select_many_key(self, fields, key_field, key_values):

        fields, key_field, key_values = self.toArray(fields, key_field, key_values)

        keys = ["{field} = '{value}'".format(
            field=key_field[0],
            value=value
        ) for value in key_values]

        query = "SELECT {fields} FROM {table_name} WHERE {keys}".format(
            fields=", ".join(fields),
            table_name=self.brackets(self.table_name),
            keys=" or ".join(keys)
        )
        return self.turple_to_array(self.send_query(query, True))

    def select_by_max(self, fields, key_field):

        fields = self.toArray(fields)

        query = "SELECT {fields} FROM {table_name} ORDER BY {key_field} DESC LIMIT 1".format(
            fields=", ".join(fields),
            table_name=self.brackets(self.table_name),
            key_field=self.brackets(key_field)
        )
        return self.turple_to_array(self.send_query(query, True))

    def select_all(self, fields="*", to_dict = False):

        fields = self.toArray(fields)

        query = "SELECT {fields} FROM {table_name}".format(
            fields=", ".join(fields),
            table_name=self.brackets(self.table_name)
        )
        data = self.send_query(query, True)
        if to_dict:
            return self.to_dict(fields, data)
        else:
            return self.turple_to_array(data)

    def delete(self, key_fields, key_values):

        key_fields, key_values = self.toArray(key_fields, key_values)

        keys = ["{field} = '{value}'".format(
            field=field,
            value=key_values[i]
        ) for i, field in enumerate(key_fields)]

        query = "DELETE FROM {table_name} WHERE {keys}".format(
            table_name=self.brackets(self.table_name),
            keys=" and ".join(keys)
        )

        self.send_query(query)

    def delete_table(self, sure = "?"):

        if sure.lower() == "yes":
            query = "DROP TABLE IF EXISTS {table_name}".format(
                table_name=self.brackets(self.table_name)
            )
            self.send_query(query)
        else:
            print("Please, be careful...You tried to remove a table {table_name}".format(table_name=self.brackets(self.table_name)))

    def send_query(self, query, answer=False):

        if self.logging:
            print(query)
        self.cursor.execute(query)
        self.mariadb_connection.commit()
        if answer == True:
            return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.mariadb_connection.close()