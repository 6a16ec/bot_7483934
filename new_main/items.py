class items:
    def __init__(self):
        table = database.Table(tables["user_permissions"])
        users = table.select_all(["tid", "owner", "admin", "manager", "moderator"], to_dict=True)
        table.close()