import database
import database_config
tables = database_config.tables().names_dict

class get_access:
    def __init__(self, telegram_id):
        self.user_status(telegram_id)
        self.permissions()

    def user_status(self, telegram_id):
        table = database.Table(tables["user_permissions"])
        permissions = table.select(["owner", "admin", "manager", "modeartor"], "telegram_id", telegram_id)[0]
        table.close()

        self.owner = permissions[0]
        self.admin = permissions[1]
        self.manager = permissions[2]
        self.moderator = permissions[3]

    def permissions(self):
        self.default_permissions()
        if self.owner:
            self.owner_permissions()
        if self.admin:
            self.admin_permissions()
        if self.manager:
            self.manager_permissions()
        if self.moderator:
            self.moderator_permissions()

    def default_permissions(self):
        self.add_category = False
        self.add_subcategory = False
        self.add_item = False

        self.add_admin = False
        self.add_manager = False
        self.add_moderator = False

        # self.change_texts = False
        # self.add_category = False
        # self.add_subcategory = False
        # self.add_item = False
        # self.moderate = False
        # self.add_qiwi = False
        # self.add_parent_qiwi = False
        # self.add_admin = False
        # self.add_manager = False
        # self.add_moderator = False
        # self.see_unmoderated_goods = False
        pass
        # about items ...

    def owner_permissions(self):
        self.add_admin = True
        self.add_moderator = True

    def admin_permissions(self):
        self.add_category = True
        self.add_subcategory = True
        self.add_item = True
        self.add_manager = True

    def manager_permissions(self):
        self.add_item = True

    def moderator_permissions(self):
        pass.





class set_access:
    def __init__(self, telegram_id):
        self.telegram_id = telegram_id
    def owner(self):
        self.permissions("owner")
    def admin(self):
        self.permissions("admin")
    def manager(self):
        self.permissions("manager")
    def moderator(self):
        self.permissions("moderator")

    def permissions(self, permission):
        table = database.Table(tables["user_permissions"])
        if table.exist("telegram_id", self.telegram_id):
            table.update("telegram_id", self.telegram_id, permission, 1)
        else:
            table.insert(["telegram_id", permission], [self.telegram_id, 1])
        table.close()




def privileged():
    fields = ["telegram_id", "owner", "admin"]
    users = []

    table = database.Table(tables["user_permissions"])
    users_data = table.select_all(fields)
    table.close()

    for user_data in users_data:
        user = {}
        for i, field in enumerate(fields):
            user[field] = user_data[i]
        users.append(user)

    all = [user["telegram_id"] for user in users]
    owner_and_admins = [user["telegram_id"] for user in users if user["owner"] or user["admin"]]
    return all, owner_and_admins
