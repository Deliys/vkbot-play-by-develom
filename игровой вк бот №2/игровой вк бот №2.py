import vk_api
import random
import time
import datetime
#если вы не знаете что вообще за токен то посмотрите мой первый ролик на эту тему https://www.youtube.com/watch?v=n-b6HJ5R1c4&feature=youtu.be
token = "vk1.a.PXX04uQnwoyhB_bee_uXzLxYWLK0puNO13gt-3jtjVPR7ceYzff2n7K8LZZV-oX_dLLaek2C06qGObyBmbFuegjjxQwj1AF3P-Z3IsUwi1HI2JBlKztlv7rzi9Lmq4yLLt66zl_R3s-cvMifA-zU0m9bIzeX3ePVkvrOrINfl4xtKmOu5irWCx_YUA0q_G4S"


vk = vk_api.VkApi(token=token)

vk._auth_token()


now = datetime.datetime.now()
timeA = now.hour




def construct(id,name,money,power):
    p = {}
    p["name"] = name
    p["money"] = money
    p["messegNumb"] = 0
    p["power"] = power

    data[str(id)] = p
    

    return "normal"


def savebd():
    with open("data.txt", "w") as file:
        for  i in data:#проходимся по data и получаем id в нем
            p = str(i) + " " +str(data[i]["name"]) +" " +str(data[i]["money"])+ " " +str(data[i]["messegNumb"])+ " " +str(data[i]["power"])
            
            file.write(p + '\n') #записываем в data.txt построчно пользователей
        
def loadbd():
    file = open("data.txt","r") 
    datas= file.read()
    datas = datas.splitlines()
    file.close()
    data = {}
    for i in datas:
        i = i.split()
        if len(i)>4:#проверка на полноту данных 
            data[str(i[0])] = {}
            data[str(i[0])]["name"] = i[1]
            data[str(i[0])]["money"] = i[2]
            data[str(i[0])]["messegNumb"] = i[3]
            data[str(i[0])]["power"] = i[4]     

    return(data)





data =loadbd()#загружаем в переменную data информацию из функции loadbd и файла data.txt

while True:
    #добавления монет каждый час пользователя
    #часть игровой механики бота
    now = datetime.datetime.now()
    timeB = now.hour
    
    if timeA<timeB:
        timeA = timeB

        for i in data:
            data[i]["money"] = data[i]["money"] + data[i]["power"]
            print(data)
    
    elif (timeA>timeB) and (timeB == 0):
        timeA = 0
        for i in data:
            data[i]["money"] = data[i]["money"] + data[i]["power"]


    messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
    if messages["count"] >= 1:
        id = messages["items"][0]["last_message"]["from_id"]
        body = messages["items"][0]["last_message"]["text"]

        #авторизация пользователя в боте
        n = 0
        for i in data:
            print(i)
            if str(id) == i :
                n = 1
        if n == 0:
            construct(id , id , 0 , 10)
        
        #простые команды   
        if body.lower() == "привет":
    
            vk.method("messages.send", {"peer_id": id, "message": "Привет!", "random_id": random.randint(1, 2147483647)})
        elif body.lower() == "кто я?":
            vk.method("messages.send", {"peer_id": id, "message": "ты хороший человек", "random_id": random.randint(1, 2147483647)})
        elif body.lower() == "профиль":
            smg = "привет " + str(data[str(id)]["name"]) + "\n"
            smg = smg + str(data[str(id)]["money"])+"$"
            smg = smg + "\n" + str(data[str(id)]["power"]) + "доход/в час"
            vk.method("messages.send", {"peer_id": id, "message": smg, "random_id": random.randint(1, 2147483647)})

        else:
            #состовные команды
            bodyone = body.lower().split()
            if (bodyone[0] == "ник") and (len(bodyone)>1):
                data[str(id)]["name"] = bodyone[1] #меняем имя пользователя в боте на новое 
               
                vk.method("messages.send", {"peer_id": id, "message": "ник изменен на " + str(bodyone[1]), "random_id": random.randint(1, 2147483647)})

            else:
                #если бот не нашел команду которую он может выполнить
                vk.method("messages.send", {"peer_id": id, "message": "нет такой команды", "random_id": random.randint(1, 2147483647)})
        savebd()

