from db_module import db_main, db_config

if __name__ == "__main__":
    # -----
    catalog = db_main.Table(db_config.tables.catalog)
    catalog.create(
        ["id", "name"],
        ["INT(5) PRIMARY KEY AUTO_INCREMENT", "VARCHAR(128)"]
    )
    catalog.insert("name", "Обувь")
    catalog.insert("name", "Одежда")
    catalog.insert("name", "Шапки")
    catalog.close()

    # -----
    items = db_main.Table(db_config.tables.items)
    items.create(
        ["id", "name", "description", "photos_id", "catalog_id", "position"],
        ["INT(8) PRIMARY KEY AUTO_INCREMENT", "VARCHAR(128)", "VARCHAR(1024)", "INT(8)", "INT(5)", "INT(8)"]
    )
    items.close()

    # -----
    texts = db_main.Table(db_config.tables.texts)
    texts.create(
        ["title", "text"],
        ["VARCHAR(256) PRIMARY KEY", "VARCHAR(1024)"]
    )
    texts.insert(["title", "text"], ["hello", "привет, ты попал в бота, который находится в разработке"])
    texts.close()