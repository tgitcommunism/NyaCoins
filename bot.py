#####################
# mysmah_NyaCoinBot #
#####################

from telepot.loop import MessageLoop
import telepot
import logging
import random
import time
import json
import sys

def search(arr, user):
    for i in arr:
        if i["user"] == user:
            return i

def getID(arr, user):
    for i in arr:
        if i["user"] == user:
            return i["id"]

def chckConfirmUser(arr, user):
    for i in arr:
        if i["user"] == user:
            return i["confirm"]

def searchID(arr, user):
    for i in range(len(arr)):
        if arr[i]["user"] == user:
            return i

f = open("json/users.json", "r")
users = json.loads(f.read())
f.close()
f = open("json/Nya.json", "r")
Nya = json.loads(f.read())
f.close()
f = open("json/debts.json", "r")
debts = json.loads(f.read())
f.close()

c = [Nya['NyaMine'], 60, 60, 0]

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    un = msg["from"]["username"]
    i = searchID(users, un)
    try:
        if un not in [x["user"] for x in users]:
            users.append({"money":10, "user":un, "id":msg["from"]["id"], "confirm":False})
    except:
        pass
    try:
        getID(users, un)
        chckConfirmUser(users, un)
    except:
        users[i] = {"money":users[i]["money"], "user":un, "id":msg["from"]["id"], "confirm":False}
    if not chckConfirmUser(users, un):
        if msg["from"]["username"] == msg["chat"]["username"]:
            users[i] = {"money":users[i]["money"], "user":un, "id":msg["from"]["id"], "confirm":True}
        else:
            tb.sendMessage(msg["chat"]["id"], "Возникла ошибка\nДля исправления напишите боту в лс")
            return 0

    if content_type == 'text':

        if msg['text'][0] == '/':

            try:
                l = [int(time.time()), msg["from"]["username"],  msg["chat"]["username"], msg["text"]]
                print(*l, sep="; ")
                #tb.sendMessage(466011918, json.dumps(l))
            except:
                try:
                    l = [int(time.time()), msg["from"]["username"], msg["text"]]
                    print(*l, "Some Error!", sep="; ")
                except:
                    print("ERROR!")

            if '/ruser' == msg['text'][:6]:
                tb.sendMessage(msg["chat"]["id"], users[random.randint(0, len(users) - 1)])
                f = open("json/users.json", "w")
                f.write(json.dumps(users))
                f.close()

            if '/all' == msg['text'][:4]:
                tb.sendMessage(msg["chat"]["id"], "\n".join([x["user"] + ": " + str(x["money"]) + (" *" if x["confirm"] else "") for x in users]))
                f = open("json/users.json", "w")
                f.write(json.dumps(users))
                f.close()

            if '/top' == msg['text'][:4]:
                arr = [[x["user"] + ": " + str(x["money"]) + (" *" if x["confirm"] else "") for x in users], [x["money"] for x in users]]
                for i in range(len(arr[0])):
                    for i in range(len(arr[0]) - 1):
                        if arr[1][i] < arr[1][i + 1]:
                            arr[1][i], arr[1][i + 1] = arr[1][i + 1], arr[1][i]
                            arr[0][i], arr[0][i + 1] = arr[0][i + 1], arr[0][i]
                tb.sendMessage(msg["chat"]["id"], "\n".join(arr[0]))
                f = open("json/users.json", "w")
                f.write(json.dumps(users))
                f.close()

            if '/confall' == msg['text'][:8]:
                tb.sendMessage(msg["chat"]["id"], "\n".join([x["user"] + ": " + str(x["money"]) for x in users if x["confirm"]]))
                f = open("json/users.json", "w")
                f.write(json.dumps(users))
                f.close()

            if "/mymoney" == msg['text'][:8]:
                try:
                    tb.sendMessage(msg["chat"]["id"], search(users, un)["money"])
                except:
                    pass
                f = open("json/users.json", "w")
                f.write(json.dumps(users))
                f.close()

            if '/send' == msg['text'][:5]:
                mesg = msg['text'][5:].split()[0:]
                if len(mesg) != 2: return 0
                mesg[0] = mesg[0][1:]
                uid = getID(users, mesg[0])
                coins = round(float(mesg[1]), 2)
                if coins <= 0: return 0
                if mesg[0] not in [x["user"] for x in users]:
                    users.append({"money":10, "user":mesg[0]})
                can = search(users, un)['money'] >= coins
                if can:
                    users[searchID(users, un)]['money'] -= coins
                    users[searchID(users, mesg[0])]['money'] += coins
                    users[searchID(users, un)]['money'] = round(users[searchID(users, un)]['money'], 2)
                    users[searchID(users, mesg[0])]['money'] = round(users[searchID(users, mesg[0])]['money'], 2)
                    tb.sendMessage(msg["chat"]["id"], "успешно послано " + str(coins) + " NyaCoin юзеру @" + mesg[0])
                    tb.sendMessage(uid, "@" + un + " отправил тебе " + str(coins) + " НяКоинов")
                else:
                    tb.sendMessage(msg["chat"]["id"], "Ошибка: недостаточно денег")
                f = open("json/users.json", "w")
                f.write(json.dumps(users))
                f.close()

            if '/mine' == msg['text'][:5]:
                try:
                    if msg["from"]["username"] == msg["chat"]["username"]:
                        if int(time.time()) - c[3] >= c[2]:
                            c[0] += 1
                            c[3] = int(time.time())
                            users[searchID(users, un)]['money'] += 0.01
                            users[searchID(users, un)]['money'] = round(users[searchID(users, un)]['money'], 2)
                            print(c[0])
                            if c[0] >= c[1]:
                                users[searchID(users, un)]['money'] += 0.99
                                users[searchID(users, un)]['money'] = round(users[searchID(users, un)]['money'], 2)
                                tb.sendMessage(msg["chat"]["id"], "+1 NyaCoin")
                                print()
                                print(un, "получил 1 NyaCoin!")
                                print()
                                c[0] = 0
                            else:
                                tb.sendMessage(msg["chat"]["id"], "осталось намайнить " + str(c[1] - c[0]) + " NyaMine")
                        else:
                            tb.sendMessage(msg["chat"]["id"], "подожди " + str(c[2] - (int(time.time()) - c[3])) + " секунд")
                        Nya['NyaMine'] = c[0]
                        f = open("json/users.json", "w")
                        f.write(json.dumps(users))
                        f.close()
                        f = open("json/Nya.json", "w")
                        f.write(json.dumps(Nya))
                        f.close()
                    else:
                        tb.sendMessage(msg["chat"]["id"], "Ошибка: Не майнь в чатах")
                except:
                    tb.sendMessage(msg["chat"]["id"], "Ошибка: Не майнь в чатах")

            if "/help" == msg['text'][:5]:
                help  = "- для того чтобы узнать количество своих NyaCoin используйте команду /mymoney\n"
                help += "- для того чтобы попытаться добыть немного NyaCoin используйте команду /mine\n"
                help += "- для того чтобы послать немного NyaCoin используйте команду /send\n"
                help += "(/send [@username которому отправляете] [количество NyaCoin])\n"
                help += "- для того чтобы дать немного NyaCoin взаймы используйте команду /debt\n"
                help += "(/debt [@username которому даёте] [количество NyaCoin] [время в часах] [%])\n"
                help += "для подтверждения отправте /confirmdebt\n"
                help += "для отмены отправте /canceldebt\n"
                help += "- для того чтобы подарить немного NyaCoin используйте команду /gift\n"
                help += "(/gift [@username которому дарите] [количество NyaCoin] [сообщение])\n"
                #help += "\n"
                tb.sendMessage(msg["chat"]["id"], help)
                f = open("json/users.json", "w")
                f.write(json.dumps(users))
                f.close()

            if '/debt' == msg['text'][:5]:
                mesg = msg['text'][5:].split()[0:]
                if len(mesg) != 4:
                    print("Error: invalid debt")
                    return 0
                mesg[0] = mesg[0][1:]
                uid = getID(users, mesg[0])
                coins = round(float(mesg[1]), 2)
                t = int(mesg[2])
                percent = int(mesg[3])
                if percent >= 100 or percent <= -100:
                    print("Error: invalid %")
                    return 0
                if coins <= 0:
                    print("Error: Nya <= 0")
                    return 0
                if un == mesg[0]:
                    print("Error: un == mesg[0]")
                    return 0
                if mesg[0] not in [x["user"] for x in users]:
                    users.append({"money":10, "user":mesg[0]})
                can = search(users, un)['money'] >= coins and not UncDebtChck(mesg[0]) and search(users, mesg[0])['money'] >= 0
                if can:
                    debts.append({"from":un, "to":mesg[0], "coins":coins, "%":percent, "time":int(time.time()), "+time":t * 3600, "confirm":False})
                    tb.sendMessage(msg["chat"]["id"], "жди подтверждения")
                    tb.sendMessage(uid, "@" + str(un) + " хочет дать тебе " + str(coins) + " НяКоинов в долг на " + str(t) + " часов под " + str(percent) + "%")
                elif UncDebtChck(mesg[0]):
                    tb.sendMessage(msg["chat"]["id"], "Ошибка: у @" + mesg[0] + " есть неподтвержденный долг")
                elif search(users, un)['money'] < coins or search(users, mesg[0])['money'] < 0:
                    tb.sendMessage(msg["chat"]["id"], "Ошибка: недостаточно NyaCoin")
                f = open("json/users.json", "w")
                f.write(json.dumps(users))
                f.close()
                f = open("json/debts.json", "w")
                f.write(json.dumps(debts))
                f.close()

            if '/confirmdebt' == msg['text'][:12]:
                if UncDebtChck(un):
                    id = UncDebtSrch(un)
                    uid = users[searchID(users, debts[id]["from"])]['id']
                    debts[id]["confirm"] = True
                    coins = debts[id]["coins"]
                    users[searchID(users, debts[id]["to"])]['money'] += coins
                    users[searchID(users, debts[id]["from"])]['money'] -= coins
                    users[searchID(users, debts[id]["to"])]['money'] = round(users[searchID(users, debts[id]["to"])]['money'], 2)
                    users[searchID(users, debts[id]["from"])]['money'] = round(users[searchID(users, debts[id]["from"])]['money'], 2)
                    tb.sendMessage(msg["chat"]["id"], "успешно подтверждено")
                    tb.sendMessage(uid, "@" + str(un) + " подтвердил debt")
                    print("успешно подтверждено")
                f = open("json/users.json", "w")
                f.write(json.dumps(users))
                f.close()
                f = open("json/debts.json", "w")
                f.write(json.dumps(debts))
                f.close()

            if '/canceldebt' == msg['text'][:11]:
                if UncDebtChck(un):
                    id = UncDebtSrch(un)
                    uid = users[searchID(users, debts[id]["from"])]['id']
                    debts.pop(id)
                    tb.sendMessage(msg["chat"]["id"], "успешно отменено")
                    tb.sendMessage(uid, "@" + str(un) + " отмененил debt")
                    print("успешно отменено")
                    f = open("json/debts.json", "w")
                    f.write(json.dumps(debts))
                    f.close()
            
            if '/gift' == msg['text'][:5]:
                mesg = msg['text'][5:].split()
                message = " ".join(mesg[2:])
                if len(mesg) < 3: return 0
                mesg[0] = mesg[0][1:]
                uid = getID(users, mesg[0])
                coins = round(float(mesg[1]), 2)
                if coins <= 0: return 0
                if mesg[0] not in [x["user"] for x in users]:
                    users.append({"money":10, "user":mesg[0]})
                can = search(users, un)['money'] >= coins
                if can:
                    users[searchID(users, un)]['money'] -= coins
                    users[searchID(users, mesg[0])]['money'] += coins
                    users[searchID(users, un)]['money'] = round(users[searchID(users, un)]['money'], 2)
                    users[searchID(users, mesg[0])]['money'] = round(users[searchID(users, mesg[0])]['money'], 2)
                    tb.sendMessage(msg["chat"]["id"], "успешно подарено " + str(coins) + " NyaCoin юзеру @" + mesg[0])
                    tb.sendMessage(uid, "@" + un + " подарил тебе " + str(coins) + " НяКоинов!")
                    tb.sendMessage(uid, message)
                else:
                    tb.sendMessage(msg["chat"]["id"], "Ошибка: недостаточно денег")
                f = open("json/users.json", "w")
                f.write(json.dumps(users))
                f.close()
            
            if '/stats' == msg['text'][:6]:
                sm = round(sum([x["money"] for x in users]), 2)
                num = len([x["user"] for x in users])
                tb.sendMessage(msg["chat"]["id"], "всего NyaCoin'ов: " + str(sm) + "\nкол-во юзеров: " + str(num) + "\nкол-во NyaCoin'ов на человека: " + str(round(sm / num, 3)))
                f = open("json/users.json", "w")
                f.write(json.dumps(users))
                f.close()

def UncDebtSrch(to):
    for i in range(len(debts)):
        if debts[i]["to"] == to:
            return i

def UncDebtChck(to):
    for i in range(len(debts)):
        if debts[i]["to"] == to:
            return True
    return False

def debtCheck():
    for i in range(len(debts)):
        if time.time() > debts[i]["time"] + debts[i]["+time"] and debts[i]["confirm"]:
            coins = debts[i]["coins"]
            coins += coins * (debts[i]["%"] / 100)
            users[searchID(users, debts[i]["to"])]['money'] -= coins
            users[searchID(users, debts[i]["from"])]['money'] += coins
            users[searchID(users, debts[i]["to"])]['money'] = round(users[searchID(users, debts[i]["to"])]['money'], 2)
            users[searchID(users, debts[i]["from"])]['money'] = round(users[searchID(users, debts[i]["from"])]['money'], 2)
            debts.pop(i)
            f = open("json/debts.json", "w")
            f.write(json.dumps(debts))
            f.close()
            break

token = '755622415:AAHQZlEYSm3tVRWkVNKmXv8tmEbx5TiY1ro'
tb = telepot.Bot(token)

MessageLoop(tb, handle).run_as_thread()

while 1:
    time.sleep(0.1)
    debtCheck()
