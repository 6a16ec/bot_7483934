class tables:
    def __init__(self):
        self.names = []
        self.names_dict = {}
        self.fields = []
        self.types = []

        # # # # #
        self.names.append("permissions")
        self.fields.append(["tid", "owner", "admin", "manager", "moderator"])
        self.types.append(["INT(12) PRIMARY KEY", "INT(1) DEFAULT 0", "INT(1) DEFAULT 0", "INT(1) DEFAULT 0", "INT(1) DEFAULT 0"])

        # # # # #
        self.names.append("managers_admins")
        self.fields.append(["manager_tid", "admin_tid"])
        self.types.append(["INT(12) PRIMARY KEY", "INT(12)"])

        # # # # #
        self.names.append("categories")
        self.fields.append(["id", "photo_id"])
        self.types.append(["TINYINT PRIMARY KEY AUTO_INCREMENT", "INT(12)"])

        for name in self.names:
            self.names_dict[name] = name
        self.init_default_data()

    def init_default_data(self):
        self.default_data = []