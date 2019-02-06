from db_module import db_main, db_config
tables = db_config.tables()

class item:
    def __init__(self, id):
        table = db_main.Table(tables.names_dict["items"])
        data = table.select("*", "id", id)[0]
        table.close()
        self.name = data[1]
        description
        photo_id
        category_id
        ", "
        position
        ", "
        price
        ", "
        code
        "

