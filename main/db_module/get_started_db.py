import db_config, db_main

class tables(db_config.tables):

    def create(self, name):
        table = db_main.Table(name)
        fields, types = self.fields[self.names.index(name)], self.types[self.names.index(name)]
        table.create(fields, types)
        table.send_query("ALTER TABLE {table_name} CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;".format(table_name = name))
        table.close()

    def create_all(self):
        for name in self.names:
            self.create(name)

    def delete(self, name):
        table = db_main.Table(name)
        table.delete_table("yes")
        table.close()

    def delete_all(self):
        for name in self.names:
            self.delete(name)

    def write_default_data(self):
        table_names = []
        for table_name, fields, values in self.default_data:
            if table_name not in table_names:
                table_names.append(table_name)

        for table_name_now in table_names:
            table = db_main.Table(table_name_now)
            for table_name, fields, values in self.default_data:
                if table_name_now == table_name:
                    table.insert(fields, values)
            table.close()


if __name__ == "__main__":
    tables().delete_all()
    tables().create_all()
    tables().write_default_data()