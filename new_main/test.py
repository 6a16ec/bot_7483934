import database

table = database.Table(database.tables["user_permissions"], logging=True)
print (table.exist("telegram_id", 385778185))
table.close()


