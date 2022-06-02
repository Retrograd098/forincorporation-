GAME = False
a=b=answ = None

from BotAmino import *
import os, time, random, json
import logging


###################################
e="IOI9nQNF4a9djM15@wwjmp.com"
p="leasanna963"
d="423ae9aef48008707155ba8ca2d258e5a90475821e2e59298731de68e29a4cf40aaaced538db3ee5fd"
prefix = "/"
proxy= None
###################################


bot = BotAmino(email=e,password=p,deviceId=d)
bot.prefix = prefix
print(bot.prefix)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
fmt = logging.Formatter(fmt="%(levelname)s: %(message)s")
handler.setFormatter(fmt)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

def dataBase(uid=None,times=None,coins=None):
    dataFile= "data.json"
    base={"times":0,"coins":0}
    try:
        with open(dataFile) as F:
            data = json.load(F)
            F.close()
    except Exception as exc:
        print("dataBaseError:",exc); data = {}
    if uid:
        try: usr= data[uid]
        except: data[uid] = base
        if times:data[uid]["times"] += 1
        if coins: data[uid]["coins"] += coins
    with open(dataFile, "w") as F:
        F.write(json.dumps(data, indent=4))
    return data[uid] if uid else data

@bot.command("монет")
def _монет(data: Parameters):
    logger.info("Command: монет")
    authorId = data.authorId
    userData = dataBase(authorId)
    data.subClient.send_message(data.chatId,"Всего: {}.".format(userData['coins']))
    #except: data.subClient.send_message(data.chatId"У Вас еще нет учетной записи.\n    Для получения решите пример.")

@bot.command("кулон")
def _кулон(data: Parameters):
	_1_1 = author[1][1]
	if int(time.time()) - _1_1 >= 2*3600:
	       _1_1 = int(time.time())
	       rew  = int(random.randint(10,20))
	       dataBase(authorId, times=True,coins=rew)
	       data.subClient.send_message(data.chatId, "Начислено: {rev}")
	else:
		delta = 2*3600 - ( int(time.time()) - _1_1 )
		textMsg = "Слишком быстро!\nПодождите еще: {}ч. {}м. {}с.".format( int( delta / 3600 ),
		int( ( delta % 3600 ) / 60 ), delta % 60 )
		data.subClient.send_message( data.chatId,
            message = textMsg )

@bot.command("link")
def _link(data: Parameters):
    coins=  data.subClient.client.get_wallet_info()
    logger.info("Command: link | coins: {}".format(coins.totalCoins))
    if data.message != "":
        authorId = data.authorId
        userData = dataBase(authorId)
        _send = 500 if userData["coins"] >=500 else userData["coins"]
        _info =  data.subClient.get_from_code(data.message)
        if _send != 0:
            if _info.objectType == 1: #Blog&Quiz
                data.subClient.pay(_send, blogId=_info.objectId)
            elif _info.objectType == 2: #Wiki
                data.subClient.pay(_send, objectId=_info.objectId)
            elif _info.objectType == 12: #Chat
                data.subClient.pay(_send, chatId=_info.objectId)
            g=dataBase(authorId, coins= -_send)
            data.subClient.send_message(data.chatId, "*Монеты отправлены*.")
        else: data.subClient.send_message(data.chatId, "Всего: {}.".format(userData['coins']))
        
@bot.command("топ")
def _топ(data: Parameters):
    logger.info("Command: топ")
    users = []
    db = dataBase()
    for user in db:
        link=data.subClient.client.get_user_info(user)
        try:db[user]["link"]=link.nickname
        except: db[user]["link"]=" "
        users.append(db[user])   
    top = sorted(users, key = lambda k: k["times"], reverse = True)
    res = ""
    for user, x in zip(top, range(len(top))):
        res += "{}. {}: {}.\n".format(str(x+1), user["link"], user["times"])
    data.subClient.send_message(data.chatId, res)

@bot.on_message()
def _on_message(data: Parameters):
    bot.show_online(data.comId)
    if bot.is_it_bot(data.authorId) is False:
        print("[{}]: {}".format(data.author, data.message))
        authorId = data.authorId
        userData = dataBase(authorId)
        global GAME, a, b, answ
        if GAME is True and data.message != None:
            action = True
            for letter in data.message:
                if letter not in "0987654321":
                    action=False; break
            if action == True:
                if answ == data.message:
                    dataBase(authorId, times=True,coins=5)
                    data.subClient.send_message(data.chatId, "Верно!\nПобедитель: >> {} <<.\nКоличество побед: {}.\n{} + {} = {}.".format(data.author, userData["times"], a, b, answ))
                    GAME = False
                    a=b=answ = None
                else: data.subClient.send_message("Не верно!")
        while GAME is False and random.randint(0, 100) > 10:
            GAME = True
            a = random.randint(0, 10)
            b = random.randint(0, 10)
            answ = str(a + b)
            data.subClient.send_message(data.chatId, "Новый пример: {} + {} = ?.".format(a, b))


#com_id = 41384370
#bot.single_launch(com_id,True) #One Community
bot.launch(True) #All Communities
print("ready")
