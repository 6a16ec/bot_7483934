from db_module import db_main, db_config

if __name__ == "__main__":
    # # -----
    # table = db_main.Table("random")
    # table.send_query("ALTER DATABASE {database_name} CHARACTER SET utf8 COLLATE utf8_general_ci;".format(database_name = db_config.database_name))

    # # -----
    # admins = db_main.Table(db_config.tables.admins)
    # admins.create(
    #     ["id", "telegram_id"],
    #     ["INT(2) PRIMARY KEY AUTO_INCREMENT", "INT(20)"]
    # )
    # admins.send_query("ALTER TABLE {table_name} CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;".format(table_name = db_config.tables.admins))
    # admins.close()

    # # -----
    # categories = db_main.Table(db_config.tables.categories)
    # categories.create(
    #     ["id", "name", "count_items"],
    #     ["INT(5) PRIMARY KEY AUTO_INCREMENT", "VARCHAR(128)", "INT(8) DEFAULT 0"]
    # )
    # categories.send_query("ALTER TABLE {table_name} CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;".format(table_name = db_config.tables.categories))
    # categories.insert(["name", "count_items"], ["Животные", 2])
    # categories.close()
    #
    # # -----
    # items = db_main.Table(db_config.tables.items)
    # items.create(
    #     ["id", "name", "description", "photo_id", "category_id", "position", "price", "code"],
    #     ["INT(8) PRIMARY KEY AUTO_INCREMENT", "VARCHAR(128)", "VARCHAR(256)", "VARCHAR(128)", "INT(5)", "INT(8)", "INT(10)", "INT(32)"]
    # )
    # items.send_query("ALTER TABLE {table_name} CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;".format(table_name = db_config.tables.items))
    # items.insert(
    #     ["name", "description", "photo_id", "category_id", "position", "price", "code"],
    #     ["Собака", "Живая собака, бегает, виляет хвостом, иногда гавкает. Хороший друг.", "AgADAgADxKkxG39y2EmQegeY5TQrXSv89A4ABMMgmZnmPm3ugs4DAAEC", 1, 1, 1, 36278234]
    # )
    # items.insert(
    #     ["name", "description", "photo_id", "category_id", "position", "price", "code"],
    #     ["Кошка", "Кошка обыкновенная, пьет молочко и мурлычит, когда ее гладят, мяукает как сука весной.", "AgADAgADXKoxG1OayEnRmdpY9FjRroFVXw8ABGrWYXKuOqcD17oAAgI", 1, 2, 1, 4732833]
    # )
    #
    # items.close()


    #
    # # -----
    # user_order = db_main.Table(db_config.tables.user_order)
    # user_order.create(
    #     ["user_id", "adress_id", "sum"],
    #     ["INT(12) PRIMARY KEY", "INT(2)", "INT(12) DEFAULT 0"]
    # )
    # user_order.send_query("ALTER TABLE {table_name} CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;".format(table_name = db_config.tables.user_order))
    # user_order.close()

    # # -----
    # user_orders = db_main.Table(db_config.tables.user_orders)
    # user_orders.create(
    #     ["id", "user_id", "order_code", "checked", "delivery_adress"],
    #     ["INT(8) PRIMARY KEY AUTO_INCREMENT", "INT(12)", "VARCHAR(10)", "INT(2) DEFAULT 0", "VARCHAR(512)"]
    # )
    # user_orders.send_query("ALTER TABLE {table_name} CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;".format(table_name = db_config.tables.user_orders))
    # user_orders.close()

    # # -----
    # delivery_adress = db_main.Table(db_config.tables.delivery_adress)
    # delivery_adress.create(
    #     ["id", "delivery_adress"],
    #     ["INT(2) PRIMARY KEY AUTO_INCREMENT", "VARCHAR(512)"]
    # )
    # delivery_adress.send_query("ALTER TABLE {table_name} CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;".format(table_name = db_config.tables.delivery_adress))
    # delivery_adress.insert("delivery_adress", "ул. Ботовская 28")
    # delivery_adress.close()

    # # -----
    # texts = db_main.Table(db_config.tables.texts)
    # texts.create(
    #     ["title", "text"],
    #     ["VARCHAR(128) PRIMARY KEY", "VARCHAR(1024)"]
    # )
    # texts.send_query("ALTER TABLE {table_name} CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;".format(table_name = db_config.tables.texts))
    # texts.insert(["title", "text"], ["hello", "Hello, friend!"])
    # texts.insert(["title", "text"], ["menu", "Выберите, пожалуйста, категорию товара, который Вас интересует:"])
    # texts.insert(["title", "text"], ["new_category", "Введите название новой категории"])
    # texts.insert(["title", "text"], ["new_item_name", "Введите название нового товара"])
    # texts.insert(["title", "text"], ["new_item_description", "Введите описание товара"])
    # texts.insert(["title", "text"], ["new_item_code", "Введите численный код товара"])
    # texts.insert(["title", "text"], ["new_item_price", "Введите цену товара"])
    # texts.insert(["title", "text"], ["new_item_photo", "Пришлите фотографию товара"])
    # texts.insert(["title", "text"], ["new_item_category", "Выберите категорию товара"])
    # texts.insert(["title", "text"], ["manager_question", "Опишите свою проблему или задайте вопрос и менеджеры свяжутся с Вами в течении 24 часов."])
    # texts.insert(["title", "text"], ["lastTxnId", "0"])
    # texts.insert(["title", "text"], ["new_adress", "Введите адрес"])
    # texts.insert(["title", "text"], ["number_qiwi", "Введите номер телефона в формате +79998887766"])
    # texts.insert(["title", "text"], ["token_qiwi", "Введите token QIWI"])
    # texts.insert(["title", "text"], ["number", "+79307082264"])
    # texts.insert(["title", "text"], ["qiwi_api_access_token", "896c43427911322d3a5389cc3117cd40"])
    #
    #
    # texts.close()