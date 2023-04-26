import dbconfig as db

data = db.getUserProfileInfo('Nextolive HR')
print(data["name"])