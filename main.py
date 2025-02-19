# coding=utf-8
""""
---Main file---

By BlockMaster
"""

import telebot as tb
from logic import calculate, find_match, NoCloseMatchException
from db_manager import DB
from bot_token import TOKEN

bot = tb.TeleBot(TOKEN)

status = ""
data = []
db = DB()


@bot.message_handler(commands=["start", "help"])
def start(msg):
    bot.send_message(msg.chat.id, """Привет! 👋
Это бот для расчёта загрязнения воздуха!

🤖 Команды:

/start - показать это сообщение ещё раз
/calculate - начать расчёт
/normal - получить среднее значение загрязнения в своей стране
/info - что такое глобальное потепление""")


@bot.message_handler(commands=["calculate"])
def calculate_(msg):
    global status
    bot.send_message(msg.chat.id, "Напишите количество километров, которые вы проехали на личном транспорте")
    status = "private_transport"


@bot.message_handler(commands=["info"])
def info(msg):
    bot.send_message(msg.chat.id, """🌍 Что такое глобальное потепление?

Глобальное потепление — это процесс повышения средней температуры Земли, обусловленный увеличением концентрации парниковых газов в атмосфере из-за человеческой деятельности.

💡 Основные причины глобального потепления включают:

    Сжигание ископаемых топлив: Добыча и использование угля, нефти и газа выделяют большие объемы углекислого газа (CO₂), что приводит к усилению парникового эффекта.

    Вырубка лесов: Леса играют ключевую роль в поглощении CO₂. Уничтожение зеленых насаждений уменьшает эту способность и, таким образом, увеличивает уровень углекислого газа в атмосфере.

    Сельское хозяйство: Некоторые методы ведения сельского хозяйства, такие как использование удобрений и метан, выделяемый скотом, также способствуют выбросам парниковых газов.

🚨 Почему это важно?

    Глобальное потепление приводит к ряду серьезных последствий, включая:

    Изменение климата (больше экстремальных погодных явлений, таких как ураганы, засухи и наводнения)

    Повышение уровня океанов (в результате таяния ледников и расширения воды при нагревании)

    Уничтожение экосистем и угрозы для биоразнообразия (многие виды животных и растений могут не адаптироваться к изменениям среды)

🌱 Что мы можем сделать?

    Каждый из нас может внести свой вклад в борьбу с глобальным потеплением:

    Сократите использование ископаемых топлив (например, переходите на общественный транспорт или электромобили).

    Поддержите проекты по озеленению и сохранению лесов.

    Используйте энергоэффективные технологии и экономьте электроэнергию.

    Поддерживайте устойчивые сельскохозяйственные практики и избегайте избытка потребления мяса.
    
Давайте вместе заботиться о нашей планете! 🌏💚""")


@bot.message_handler(commands=["normal"])
def normal(msg):
    global status
    bot.send_message(msg.chat.id, "Введите страну проживания на английском")
    status = "country"


@bot.message_handler(func=lambda msg: True)
def input_(msg):
    global status, data
    match status:
        case "private_transport":
            try:
                data.append(int(msg.text))
            except ValueError:
                bot.send_message(msg.chat.id, "Вы ввели не число! Напишите количество километров, которые вы проехали на личном транспорте")
                return
            status = "social_transport"
            bot.send_message(msg.chat.id, "Напишите количество километров, которые вы проехали на общественном транспорте")
            return
        
        case "social_transport":
            try:
                data.append(int(msg.text))
            except ValueError:
                bot.send_message(msg.chat.id, "Вы ввели не число! Напишите количество километров, которые вы проехали на общественном транспорте")
                return
            status = "food_type"
            bot.send_message(msg.chat.id, "Напишите тип вашей диеты. Варианты - Вегетарианская/Обычная")
            return
        
        case "food_type":
            if not msg.text in ["Вегетарианская", "Обычная"]:
                bot.send_message(msg.chat.id, "Такого варианта не существует! Напишите тип вашей диеты. Варианты - Вегетарианская/Обычная")
                return
            if msg.text == "Вегетарианская":
                data.append(True)
            else:
                data.append(False)
            status = "at_home"
            bot.send_message(msg.chat.id, "Напишите количество приёмов пищи дома")
            return
        
        case "at_home":
            try:
                data.append(int(msg.text))
            except ValueError:
                bot.send_message(msg.chat.id, "Вы ввели не число! Напишите количество приёмов пищи дома")
                return
            status = "at_restaurant"
            bot.send_message(msg.chat.id, "Напишите количество приёмов пищи в кафе/ресторане")
            return
        
        case "at_restaurant":
            try:
                data.append(int(msg.text))
            except ValueError:
                bot.send_message(msg.chat.id, "Вы ввели не число! Напишите количество приёмов пищи в кафе/ресторане")
                return
            status = "kwats"
            bot.send_message(msg.chat.id, "Напишите количество киловаттов, которые вы израсходовали")
            return
        
        case "kwats":
            try:
                data.append(int(msg.text))
            except ValueError:
                bot.send_message(msg.chat.id, "Вы ввели не число! Напишите количество киловаттов, которые вы израсходовали")
                return
            status = ""
            result = calculate(data[0], data[1], data[2], data[3], data[4], data[5])
            data.clear()
            bot.send_message(msg.chat.id, f"""Результаты:
            
Личный транспорт: {result["private_km"]}г, {round(result["private_km_per"])}% от всего
Общественный транспорт: {result["community_km"]}г, {round(result["community_km_per"])}% от всего
Еда дома: {result["at_home"]}г, {round(result["at_home_per"])}% от всего
Еда в ресторане/кафе: {result["at_restaurant"]}г, {round(result["at_restaurant_per"])}% от всего
Электроэнергия: {result["kw"]}г, {round(result["kw_per"])}% от всего
Итого: {result["all"]}г

Среднее загрязнение на человека - /normal
Пройти тест заново - /calculate
""")
            return
        
        case "country":
            inp = msg.text
            try:
                real_country = find_match(inp)
            except NoCloseMatchException:
                bot.send_message(msg.chat.id, "Не найдено информации про такую страну. Введите правильное название")
                return
            res = db.get_CO2_per_month(real_country)
            bot.send_message(msg.chat.id, f"Среднее загрязнение одним человеком за месяц в стране {real_country} - {res}г")
            status = ""


bot.infinity_polling()
