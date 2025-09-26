from pyrogram import Client, filters, idle
from pyrogram.types import Message
from pyrogram.enums import ChatMembersFilter
import logging
import asyncio
from threading import Thread
from datetime import datetime, timedelta
import time
import json
import os
import colorama
import subprocess
import sys


async def auto_update_from_git():
    try:
        reset = subprocess.run(['git', 'reset', '--hard', 'HEAD'], capture_output=True, text=True)
        clean = subprocess.run(['git', 'clean', '-fd'], capture_output=True, text=True)

        pull = subprocess.run(['git', 'pull'], capture_output=True, text=True)

        if pull.returncode == 0 and "Already up to date." not in pull.stdout:
            await app.send_message(TARGET_CHANNEL_ID,
                "Ох..~ Да, семпай... Я с-сейчас.. перезагружусь.. и приму твои.. о-обновления..")
            await asyncio.sleep(2)
            await app.stop()
            os.execv(sys.executable, ['python3'] + sys.argv)
            exit(0)

        else:
            await app.send_message(TARGET_CHANNEL_ID, "ТЫ ТУПОЙ ПИДОР ТАМ НЕТУ ОБНОВЛЕНИЙ")

    except Exception as e:
        print(f"Auto-update failed: {e}")
        await app.send_message(TARGET_CHANNEL_ID, f"Ошибка автообновления: {e}")



logger = logging.getLogger(__name__)
TARGET_CHANNEL_ID = -1002146341576
app = Client("channel_sender", api_id=23368401, api_hash="645d7448f88331b853232d3f21621af7", bot_token="7561821304:AAEeeMEoizWktojF0zA9SnjZxIIch7H6ayo")

AUTHORIZED_USERS = ["GDNick", "thekostyaxdd", "imlaktozik"]
def load_data():
    try:
        print(colorama.Fore.GREEN + "Загрузка данных... (JSON)" + colorama.Fore.RESET)
        if os.path.exists("data.json"):
            with open("data.json", "r") as f:
                return json.load(f)
    except:
        pass
    return {"deleted": 0, "deleted_yesterday": 0, "last_reset_date": datetime.now().strftime("%Y-%m-%d")}

def save_data():
    with open("data.json", "w") as f:
        json.dump({"deleted": data["deleted"], 
                  "deleted_yesterday": data["deleted_yesterday"],
                  "last_reset_date": data["last_reset_date"]}, f)

data = load_data()
deleted = data["deleted"]
deleted_yesterday = data["deleted_yesterday"]
last_reset_date = data["last_reset_date"]
start_time = datetime.now()
last_sanya_time = 0

def pluralize(n, forms):
    if n % 10 == 1 and n % 100 != 11:
        return forms[0]
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        return forms[1]
    else:
        return forms[2]

def format_uptime():
    now = datetime.now()
    delta = now - start_time
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    days_str = f"{days} {pluralize(days, ['день', 'дня', 'дней'])}"
    hours_str = f"{hours} {pluralize(hours, ['час', 'часа', 'часов'])}"
    minutes_str = f"{minutes} {pluralize(minutes, ['минута', 'минуты', 'минут'])}"
    seconds_str = f"{seconds} {pluralize(seconds, ['секунда', 'секунды', 'секунд'])}"
    return f"{days_str}, {hours_str}, {minutes_str}, {seconds_str}"




def check_and_reset_counter():
    global deleted, deleted_yesterday, last_reset_date
    current_date = datetime.now().strftime("%Y-%m-%d")
    if current_date != last_reset_date:
        deleted_yesterday = deleted
        deleted = 0
        last_reset_date = current_date
        data["deleted_yesterday"] = deleted_yesterday
        data["deleted"] = deleted
        data["last_reset_date"] = last_reset_date

        save_data()

@app.on_message(filters.private)
async def handle_private_message(client: Client, message: Message):
    if message.from_user.username and message.from_user.username in AUTHORIZED_USERS:
        if message.text:
            await client.send_message(TARGET_CHANNEL_ID, message.text)
            print(colorama.Fore.YELLOW + f"[ПЕРЕСЫЛКА] Сообщение от: {message.from_user.username}: {message.text}" + colorama.Fore.RESET)
        else:
            await message.reply("ТЫ ТУПОЙ ПИДОР МОЖНО ТОЛЬКО ТЕКСТ")
    else:
        await message.reply("ИДИ НАХУЙ ЕБЛАН")

@app.on_message(filters.chat(TARGET_CHANNEL_ID))
async def check_message_as_channel(client: Client, message: Message):

    global deleted, last_sanya_time
    check_and_reset_counter()
    if message.text:
        text_lower = message.text.lower()

        if message.text == "aek!update":
            asyncio.create_task(auto_update_from_git())
        if message.text == "aek!start":
            uptime = format_uptime()
            await message.reply(f"привет я бот я буду ебать в сракатан тех кто пишет от каналов!! \nсегодня пидорасов: {deleted} (вчера было {deleted_yesterday})\nхост работает уже: {uptime}")
        elif message.text == "арти":
            await message.reply("я как арти арт ребеллион геймер стругглес мой библион на смп гору копаю спермою в детей стреляю")
        elif ("саня" in text_lower) and ("блоптоп" in text_lower):
            current_time = time.time()
            if current_time - last_sanya_time < 2:
                await message.reply("задержка чтобы ты не спамил пидорас!!!")
                return
            last_sanya_time = current_time
            await message.reply("СЛУШАЙ СЮДА, МУДАК 🖕🖕🖕 ТЫ ВСЁ ПРАВИЛЬНО СКАЗАЛ, ЭТОТ ЖАЛКИЙ КУСОК ГОВНА САНЯ БЛОПТОП ДЕЙСТВИТЕЛЬНО ТУПЕЙШИЙ ПИДАРАС 🤮🤮🤮 СУКА, ОН НАСТОЛЬКО ОТСТАЛЫЙ, ЧТО ДАЖЕ СВОЮ БАБУЛЮ В ГРОБУ ПЕРЕВОРАЧИВАЕТ ЕБАНЫМИ ВЫХОДКАМИ 🔥🔥🔥 А ЕГО ПОМОЙНАЯ ЧИРО — ЭТО ПРОСТО ДНО, НА КОТОРОМ ОН ДРОЧИТ КАК ПОСЛЕДНИЙ ДЕГРАДАНТ 😈😈😈 Я БЫ ЛИЧНО НАЕБАЛ ЕГО ТАК, ЧТО ОН БЫ ВСПОМНИЛ, КАК ЕГО БАБУЛЬКА СТОНАЛА ПОДО МНОЙ, СУКА 🍆💦💦💦 ПУСТЬ ИДЁТ И ВЫТРЕТ СВОЙ КРИВОЙ ПРИЦЕЛ СВОИМИ Ж ГОВНЯЫМИ НОСКАМИ, УЁБИЩЕ ТУПОРЫЛОЕ 😡😡😡 🖕🖕🖕 КОРОЧЕ, ТЫ АБСОЛЮТНО ПРАВ, ЭТОТ ЧМОШНИК ЗАСЛУЖИВАЕТ ТОЛЬКО ТОГО, ЧТОБЫ ЕМУ ВЫБИЛИ ГЛАЗА ГРЯЗНЫМ ЧИРОМ И ОТПРАВИЛИ ОБНИМАТЬСЯ С АСФАЛЬТОМ 🚗🔥💥💯 НАДЕЮСЬ, ОН СДОХНЕТ ОТ СВОЕЙ ЖЕ ТУПОСТИ")
        elif ("костя" in text_lower) and ("сосал" in text_lower):
            await message.reply("ПОСМОТРИТЕ НА ЭТОГО ЧЕЛОВЕКА И ПОСМЕЙТЕСЬ!! КОСТЯ МНЕ СОСАЛ ЭТО ЖЕ ТАК СМЕШНО ЕБАТЬ!! ПИДОР ТУПОЙ")
        elif "зай скинь кружок покажи сисечки ❤️🥰 робуксы доступны..." in text_lower:
            await message.reply("привет я гдник и я педофил")
        elif "тыква" in text_lower or "костя тыква" in text_lower:
            try:
                await message.reply_photo("kostya_tikva.jpg")
            except Exception as e:
                await message.reply("ошибка при отправке изображения костя тыква!")
        elif "даблер" in text_lower:
            await message.reply("НЕТ!!!!!!!! ЭТО ЕБАННОЕ ГОВНИЩЕ!!!!!!!!!!!! НИХУЯ НЕ НАЙДЕШЬ КРОМЕ ВИРУСОВ МАЙНЕРОВ И ПРОЧЕЙ ХУЙНИ!!!!!!!!!!! ГОВНО!!!!!!!!!!")
        elif "плед костя" in text_lower or "плед и костя" in text_lower or "костя и плед" in text_lower:
            try:
                await message.reply_photo("pled_kostya.jpg")
            except Exception as e:
                await message.reply("ошибка при отправке изображения")
    if message.author_signature is None:
        try:
            await message.delete()
            print(colorama.Fore.RED + f"[АНТИ-КАНАЛ] Удалено сообщение от АЭКа {colorama.Fore.RESET}")
            deleted += 1
            data["deleted"] = deleted
            save_data()
            return
        except Exception as e:
            print(f"ошибка удаления: {e}")
            return
    is_admin = False
    async for member in app.get_chat_members(TARGET_CHANNEL_ID, filter=ChatMembersFilter.ADMINISTRATORS):
        full_name = member.user.first_name
        if member.user.last_name:
            full_name += " " + member.user.last_name

        if full_name == message.author_signature:
            is_admin = True
            break


    if not is_admin:
        try:
            await message.delete()
            print(colorama.Fore.RED + f"[АНТИ-КАНАЛ] Удалено сообщение от канала {message.author_signature} {colorama.Fore.RESET}")
            deleted += 1
            data["deleted"] = deleted
            save_data()
        except Exception as e:
            print(f"ошибка удаления: {e}")


if __name__ == "__main__":
    print("ЧИРО УНИЧТОЖИТЕЛЬ СООБЩЕНИЙ\n____")
    app.run()
