import mysql.connector as mariadb
import config


class Table:
    def __init__(self, name, logging=False):
        self.mariadb_connection = mariadb.connect(user=config.username, password=config.password,
                                                  database=config.database_name)
        self.cursor = self.mariadb_connection.cursor(buffered=True)

        self.table_name = name
        self.logging = logging

    def brackets(self, name):
        name = """ """ + """`""" + name + """`"""
        return name

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

    def select(self, fields, key_fields, key_values):

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
        return self.send_query(query, True)

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
        return self.send_query(query, True)

    def select_by_max(self, fields, key_field):

        fields = self.toArray(fields)

        query = "SELECT {fields} FROM {table_name} ORDER BY {key_field} DESC LIMIT 1".format(
            fields=", ".join(fields),
            table_name=self.brackets(self.table_name),
            key_field=self.brackets(key_field)
        )
        return self.send_query(query, True)

    def select_all(self, fields="*"):

        fields = self.toArray(fields)

        query = "SELECT {fields} FROM {table_name}".format(
            fields=", ".join(fields),
            table_name=self.brackets(self.table_name)
        )
        return self.send_query(query, True)

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


def example():
    test = Table("test", True)
    test.create(["id", "id_vk", "name", "message"],
                ["int(5) PRIMARY KEY AUTO_INCREMENT", "INT(15)", "VARCHAR(100)", "VARCHAR(4096)"])

    test.insert("id_vk", 12345)
    test.insert(["id_vk", "name", "message"], [777777, "Nikita", "Hi, how are you"])
    print(test.select("*", "id", 1))
    print(test.select("*", "id", 2))

    test.update("id", "1", "name", "Nikita")
    test.insert(["id_vk", "name"], [123234, "Nikita"])
    print(test.select("*", "name", "Nikita"))

    test.delete("id", 1)
    print(test.select("*", "name", "Nikita"))


    print(test.select_all("id"))

    test.insert("name", None)

    print("Max ID: ", test.select_by_max(["id", "id_vk", "name"], "id"))

    # test.delete_table("yes")

    test.close()


if (__name__ == "__main__"): example()