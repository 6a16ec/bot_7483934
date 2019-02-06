try:
    from db_module import db_main
except:
    import db_main

username = "root"
password = "default_password_centos_000"
database_name = "main"

class tables:
    def __init__(self):
        self.names = []
        self.names_dict = {}
        self.fields = []
        self.types = []

        # # # # #
        self.names.append("admins")
        self.fields.append(["id", "telegram_id"])
        self.types.append(["INT(2) PRIMARY KEY AUTO_INCREMENT", "INT(20)"])

        # # # # #
        self.names.append("categories")
        self.fields.append(["id", "name", "count_items"])
        self.types.append(["INT(5) PRIMARY KEY AUTO_INCREMENT", "VARCHAR(128)", "INT(8) DEFAULT 0"])

        # # # # #
        self.names.append("items")
        self.fields.append(["id", "name", "description", "photo_id", "category_id", "position", "price", "code"])
        self.types.append(["INT(8) PRIMARY KEY AUTO_INCREMENT", "VARCHAR(128)", "VARCHAR(256)", "VARCHAR(128)", "INT(5)", "INT(8)", "INT(10)", "INT(32)"])

        # # # # #
        self.names.append("basket")
        self.fields.append(["user_id", "item_code", "item_name", "item_price", "item_count"])
        self.types.append(["INT(12)", "INT(32)", "VARCHAR(128)", "INT(10)", "INT(4)"])

        # # # # #
        self.names.append("orders")
        self.fields.append(["order_code", "item_code", "item_name", "item_price", "item_count"])
        self.types.append(["VARCHAR(10)", "INT(32)", "VARCHAR(128)", "INT(10)", "INT(4)"])

        # # # # #
        self.names.append("user_order")
        self.fields.append(["user_id", "adress_id", "sum"])
        self.types.append(["INT(12) PRIMARY KEY", "INT(2)", "INT(12) DEFAULT 0"])

        # # # # #
        self.names.append("user_orders")
        self.fields.append(["id", "user_id", "order_code", "checked", "delivery_adress"])
        self.types.append(["INT(8) PRIMARY KEY AUTO_INCREMENT", "INT(12)", "VARCHAR(10)", "INT(2) DEFAULT 0", "VARCHAR(512)"])

        # # # # #
        self.names.append("delivery_adress")
        self.fields.append(["id", "delivery_adress"])
        self.types.append(["INT(2) PRIMARY KEY AUTO_INCREMENT", "VARCHAR(512)"])

        # # # # #
        self.names.append("texts")
        self.fields.append(["title", "text"])
        self.types.append(["VARCHAR(128) PRIMARY KEY", "VARCHAR(1024)"])

        for name in self.names:
            self.names_dict[name] = name
        self.init_default_data()

    def init_default_data(self):
        self.default_data = []

        self.default_data.append([self.names_dict["texts"], ["title", "text"], ["hello", "Hello, friend!"]])
        self.default_data.append([self.names_dict["texts"], ["title", "text"], ["menu", "Выберите, пожалуйста, категорию товара, который Вас интересует:"]])
        self.default_data.append([self.names_dict["texts"], ["title", "text"], ["new_category", "Введите название новой категории"]])
        self.default_data.append([self.names_dict["texts"], ["title", "text"], ["new_item_name", "Введите название нового товара"]])
        self.default_data.append([self.names_dict["texts"], ["title", "text"], ["new_item_description", "Введите описание товара"]])
        self.default_data.append([self.names_dict["textsэ"], ["title", "text"], ["new_item_code", "Введите численный код товара"]])
        self.default_data.append([self.names_dict["texts"], ["title", "text"], ["new_item_price", "Введите цену товара"]])
        self.default_data.append([self.names_dict["texts"], ["title", "text"], ["new_item_photo", "Пришлите фотографию товара"]])
        self.default_data.append([self.names_dict["texts"], ["title", "text"], ["new_item_category", "Выберите категорию товара"]])
        self.default_data.append([self.names_dict["texts"], ["title", "text"], ["manager_question", "Опишите свою проблему или задайте вопрос и менеджеры свяжутся с Вами в течении 24 часов."]])
        self.default_data.append([self.names_dict["texts"], ["title", "text"], ["lastTxnId", "0"]])
        self.default_data.append([self.names_dict["texts"], ["title", "text"], ["new_adress", "Введите адрес"]])
        self.default_data.append([self.names_dict["texts"], ["title", "text"], ["number_qiwi", "Введите номер телефона в формате +79998887766"]])
        self.default_data.append([self.names_dict["texts"], ["title", "text"], ["token_qiwi", "Введите token QIWI"]])
        self.default_data.append([self.names_dict["texts"], ["title", "text"], ["number", "+79307082264"]])
        self.default_data.append([self.names_dict["texts"], ["title", "text"], ["qiwi_api_access_token", "896c43427911322d3a5389cc3117cd40"]])

        self.default_data.append([self.names_dict["delivery_adress"], "delivery_adress", "ул. Ботовская 28"])

        self.default_data.append([self.names_dict["items"],
                                  ["name", "description", "photo_id", "category_id", "position", "price", "code"],
                                  ["Собака", "Живая собака, бегает, виляет хвостом, иногда гавкает. Хороший друг.", "AgADAgADxKkxG39y2EmQegeY5TQrXSv89A4ABMMgmZnmPm3ugs4DAAEC", 1, 1, 1, 36278234]])
