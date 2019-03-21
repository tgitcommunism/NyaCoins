import json
import time

while 1:

    t = int(time.time())

    if t % 3600 == 0:
    
        f = open("users.json", "r")
        users = json.loads(f.read())
        f.close()

        f = open("stats.json", "r")
        stats = json.loads(f.read())
        f.close()

        sm = round(sum([x["money"] for x in users]), 2)
        n = len([x["user"] for x in users])
        NyaPerPerson = round(sm / n, 3)

        print("всего NyaCoin'ов:", sm)
        print("кол-во юзеров:", n)
        print("кол-во NyaCoin'ов на человека:", NyaPerPerson)

        stats.append({"sum":sm, "n":n, "NyaPerPerson":NyaPerPerson, "time":t})

        f = open("stats.json", "w")
        f.write(json.dumps(stats))
        f.close()

        time.sleep(60)
