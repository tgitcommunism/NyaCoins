import json

f = open("users.json", "r")
users = json.loads(f.read())
f.close()

sum = round(sum([x["money"] for x in users]), 2)
n = len([x["user"] for x in users])

print("всего NyaCoin'ов:", sum)
print("кол-во юзеров:", n)
print("кол-во NyaCoin'ов на человека:", round(sum / n, 2))
