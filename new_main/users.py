import database
import database_config
tables = database_config.tables().names_dict

class access:
    def __init__(self):
        self.permissions = {}
        self.get_privileged_users()
        self.get_managers_admins()

    def get_privileged_users(self):

        table = database.Table(tables["permissions"])
        users = table.select_all(["tid", "owner", "admin", "manager", "moderator"], to_dict=True)
        table.close()

        self.privileged_users = [user["tid"] for user in users]
        self.owners = [user["tid"] for user in users if user["owner"]]
        self.admins = [user["tid"] for user in users if user["admin"]]
        self.managers = [user["tid"] for user in users if user["manager"]]
        self.moderators = [user["tid"] for user in users if user["moderator"]]

    def get_managers_admins(self):

        table = database.Table(tables["managers_admins"])
        pairs = table.select_all(["manager_tid", "admin_tid"], to_dict=True)
        table.close()

        self.managers_admins = {}
        for pair in pairs:
            self.managers_admins[pair["manager_tid"]] = pair["admin_tid"]
        print (self.managers_admins)

    def set_employee(self, employee_tid, employee):
        table = database.Table(tables["permissions"])
        if table.exist("tid", employee_tid):
            table.update("tid", employee_tid, employee, 1)
        else:
            table.insert(["tid", employee], [employee_tid, 1])
        table.close()

        if employee_tid not in self.privileged_users:
            self.privileged_users.append(employee_tid)

    def set_manager_admin(self, manager_tid, admin_tid):
        table = database.Table(tables["managers_admins"])
        if table.exist("manager_tid", manager_tid):
            table.update("manager_tid", manager_tid, "admin_tid", admin_tid)
        else:
            table.insert(["manager_tid", "admin_tid"], [manager_tid, admin_tid])
        table.close()

    def set_owner(self, owner_tid):
        self.set_employee(owner_tid, "owner")
        if owner_tid not in self.owners:
            self.owners.append(owner_tid)
        print (self.owners, self.admins, self.managers, self.moderators, self.managers_admins)

    def set_admin(self, admin_tid):
        self.set_employee(admin_tid, "admin")
        if admin_tid not in self.admins:
            self.admins.append(admin_tid)
        print (self.owners, self.admins, self.managers, self.moderators, self.managers_admins)

    def set_manager(self, manager_tid, admin_tid):
        self.set_employee(manager_tid, "manager")
        if manager_tid not in self.managers:
            self.managers.append(manager_tid)
        self.set_manager_admin(manager_tid, admin_tid)
        self.managers_admins[manager_tid] = admin_tid
        print (self.owners, self.admins, self.managers, self.moderators, self.managers_admins)

    def set_moderator(self, moderator_tid):
        self.set_employee(moderator_tid, "moderator")
        if moderator_tid not in self.moderators:
            self.moderators.append(moderator_tid)
        print (self.owners, self.admins, self.managers, self.moderators, self.managers_admins)

    def user(self, telegram_id):
        self.default_permissions()
        if telegram_id in self.owners:
            self.owner_permissions()
        if telegram_id in self.admins:
            self.admin_permissions()
        if telegram_id in self.managers:
            self.manager_permissions()
        if telegram_id in self.moderators:
            self.moderator_permissions()
        return self.permissions

    def default_permissions(self):
        pemissions = [
            "add_category", "add_subcategory", "add_item",
            "add_employee", "add_admin", "add_manager", "add_moderator"
        ]

        for pemission in pemissions:
            self.permissions[pemission] = False

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
        pemissions = [
            "add_category", "add_subcategory", "add_item",
            "add_employee", "add_admin", "add_manager", "add_moderator"
        ]
        for pemission in pemissions:
            self.permissions[pemission] = True

    def admin_permissions(self):

        pemissions = [
            "add_category", "add_subcategory", "add_item",
            "add_employee", "add_manager"
        ]

        for pemission in pemissions:
            self.permissions[pemission] = True

    def manager_permissions(self):
        pemissions = [
            "add_item"
        ]

        for pemission in pemissions:
            self.permissions[pemission] = True


    def moderator_permissions(self):
        pass
