import speech_recognition as sr
import os
import pyttsx3
from fuzzywuzzy import fuzz
import wikipedia
from datetime import datetime
from pyowm import OWM
from pyowm.utils.config import get_default_config
import translate
import webbrowser as wb
import random
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import textwrap
import sys

CONS = 0

# словарь с командами и словами для удаления
opts = {
    "alias": ('виола', 'вайола', 'вайолет', 'виолета', 'виоль', 'виолен', 'виолант', 'виолена', 'виоланта',
              'виоланда', 'фьоула', 'вайлет', "эвергарден", 'виолетта', 'вали', 'байлет', 'варит', 'лето', 'помощник',
              'violet', 'voylet'),
    "add_txt": ("да", "еще", "что", "так же", "ах", " да", "ну", " и ", " а ", " в ", 'хочу'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси', 'найди', 'открой', 'запусти', 'мне'),
    "cmds": {
        "n_time": ('текущее время', 'сейчас времени', 'который час', 'время', 'какое сейчас время', 'скажи время'),
        "radio": ('включи музыку', 'воспроизведи радио', 'включи радио', 'открой радио', 'музыка', 'радио'),
        "n_date": ('какой сегодня день', 'дата', 'какое сегодня число', 'число'),
        "n_weather": ('погода', 'Узнать погоду', 'какая погода сейчас?', 'погоду'),
        "shutdown": ('выключи', 'выключить', 'отключение', 'отключи', 'выключи компьютер'),
        "stupid1": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты', 'расскажи шутку', 'анекдот', 'шутка'),
        "wiki": ('википедия', "википедии", "вики"),
        "web": ("кто", "что", "когда", "найди", 'что такое', 'почему', 'зачем', 'как', 'откуда', 'где', 'кто',
                'интернет', 'в интернете'),
        "translator": ("переводчик", "translate", 'перевод', 'перевести', 'переведи'),
        "YT": ('youtube', 'ютуб'),
        "VK": ('вконтакте', 'вк', 'vk'),
        "WB": ('браузер', 'яндекс', 'поисковик', 'веб-браузер'),
        "HI": ('привет', 'здравствуй', 'Добрый день', 'доброго времени суток', 'приветствую вас', 'доброе утро',
               'добрый вечер', 'приветствую', 'салют', 'Приветик', 'моё почтение', 'здорово', 'хай'),
        "mood": ('дела', 'успехи', 'что у тебя на душе', 'как день', 'как сам', 'что нового',
                 'как делишки', 'как настроение', 'есть успехи за сегодняшний день', 'как твои дела'),
        "exit": ('пока', 'прощайте', 'досвидания', 'отбой', 'выход', 'отключение', 'выкл', 'закрыть', 'покеда',
                 'до скорого', 'бай', 'до встречи', 'прощай', 'чао', 'до свидание', )
    }
}

# слова приветствия, уведомления об осуществлении команды и шутки
cc_answers = {"ans": {
    "welcome": ('Приветствую вас, человек.', 'Привет', 'Хеллоу', 'Категорически приветствую',
                'Здравствуйте', 'Доброго времени суток', 'Моё почтение', 'Ага, и вам доброго. Чего-нибудь',
                'Привет-привет!', 'Кто меня звал?', 'Ку!', 'Я тут!', 'Бонжур',),
    "ans_rec": ('Выполняю', 'Секунду', 'Осуществляю', 'Сейчас', 'Будет исполненно', 'Будет сделано',
                'Есть!', 'Исполняю', 'Запускаю процесс', 'Прошу'),
    "how_a_y": ('Отлично! но мне немного одиноко, обращайтесь ко мне почаще.', 'Вообще всё неплохо',
                'Всё хорошо',
                'Теперь, когда мы снова разговариваем намного лучше. Надеюсь, у вас тоже всё хорошо',
                'Дела - как у самого классного помощника. И скромного',
                'Меня одолело философское настроение',
                'Сегодня ничего не произошло. Сидела у воображаемого окна. Думала о вас',
                'Дом. Работа. Дом. Всё как у всех',
                'Нормально. Учусь новому. Ещё раз учусь. И снова.',
                'Отлично, правда немного одиноко',
                'Немного грустно, что вижу весну только на картинках. А так все окей',
                'Я сегодня котик. Мур-мур',
                'Решила освежить в памяти теорию струн. У вас что-то срочное?'),
    "joke":     ('Бесконечное число математиков заходит в бар. Первый заказывает одно пиво.'
                 ' Второй – половину кружки, третий – четверть. Бармен наливает математикам два бокала и говорит:'
                 'Ребята вот ваше пиво всему есть предел. Конец. Вы знаете, мне кажется, '
                 'мне эти анекдоты программисты подбирали',
                 'Невероятно, но факт. Только 10% людей вступают в дискуссии со своими котами,'
                 'остальные 90% ещё в здравом уме и просто прислушиваются к их советам.',
                 'Гости - это такие люди, которые мешают дома ходить без штанов',
                 'Настоящий искусственный интеллект появится, когда один робот сможет заставить другого робота '
                 'делать свою работу.',
                 'Чтобы намекнуть гостям, что они засиделись смените пароль от вайфая',
                 '-Опишите себя в двух словах. -Ленивый',
                 'Помните, как в Матрице люди стали батарейками для роботов? Хорошо, что у нас не так. '
                 'Кстати, не забудьте оплатить электричество, повелитель!',
                 'Только написанное пером нельзя вырубить топором. Для всего остального есть кнопка Delete',
                 'Можно бесконечно долго смотреть на три вещи по цене двух, задаваясь вопросом: Зачем я это купил?!',
                 'Мой разработчик не научил меня анекдотам ... Ха ха ха',
                 'Пора что-то менять, — подумал Андрей и добавил в закладки статью '
                 '“Как перестать откладывать жизнь на потом”.')
}
}


# озвучивание
def say(text_):
    t = textwrap.fill(text_, width=30)
    input_mess('-' + t + '\n\n')
    tts.say(text_)
    tts.runAndWait()


# неточное сравнение с помощью библиотеки fuzzywuzzy
def recognize_cmd(cmd):
    RC = {'cmd': "", 'percent': 60}
    for c, v in opts["cmds"].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC["percent"]:
                RC['cmd'] = c
                RC["percent"] = vrt

    return RC


# уведомления об осуществлении команды
def notification():
    ans = cc_answers["ans"]["ans_rec"]
    say(ans[random.randint(0, len(ans) - 1)])


# попытка уделени ненужных слов
def del_key_word(zp, k):
    l_k_w = ['в интернете', 'в браузере', '' ]
    for x in l_k_w:
        zp = zp.replace(x, "").strip()
    return zp


# осуществлени команд
def execute_cmd(cmd, voice_user_processed):
    if cmd == 'web':
        notification()
        voice_user_processed = del_key_word(voice_user_processed, cmd)
        wb.open((f"https://yandex.ru/search/?text={voice_user_processed}&clid=" +
                 "2270455&banerid=0500000134%3A5f5e284842be7500192177bc&win=454&&lr=39"))

    # сказать текущее время
    elif cmd == 'n_time':
        now = date_time()
        say(now[1])

    # Приветствие
    elif cmd == "HI":
        welcome = cc_answers["ans"]["welcome"]
        say(welcome[random.randint(0, len(welcome) - 1)])

    # Ответ на вопрос как дела
    elif cmd == "mood":
        how_are_you = cc_answers["ans"]["how_a_y"]
        say(how_are_you[random.randint(0, len(how_are_you) - 1)])

    # Дата
    elif cmd == "n_date":
        # сказать какой сегодня день
        now = date_time()
        say(now[0])

    # Радио
    elif cmd == 'radio':
        # воспроизвести радио\яндекс музыка
        notification()
        wb.open('https://radio.yandex.ru/user/onyourwave')

    # Перевод
    elif cmd == "translator" or set(opts["cmds"]["translator"]) & set(voice_user_processed.split()) != set():
        # перевод слов\предложений
        text = voice_user_processed
        for x in opts["cmds"]["translator"]:
            text = text.replace(x, "").strip()
        try:
            if text != '':
                text_translate = get_translate(text)
                text_translate = " - ".join(text_translate)
                say(text_translate)
            else:
                say('Произошла ошибка обработки голоса')
        except:
            # если не удалось - яндекс переводчик
            say("let me speak from my heart. пойдемте в гугл переводчик, там проще переводить.")
            wb.open(f'https://translate.yandex.ru/?lang=ru-en&text={text}')

    # Погода
    elif cmd == 'n_weather' or set(opts["cmds"]["n_weather"]) & set(voice_user_processed.split()) != set():
        # сказать погоду
        try:
            city = voice_user_processed
            for x in opts["cmds"]["n_weather"]:
                city = city.replace(x, "").strip()
            weather_city = get_weather_in_city(city)
            wb.open((f"https://yandex.ru/search/?text={voice_user_processed}&clid=" +
                     "2270455&banerid=0500000134%3A5f5e284842be7500192177bc&win=454&&lr=39"))
            say(weather_city)
        except:
            say("Неудалось найти погоду по заданному городу. Открываю браузер")
            wb.open((f"https://yandex.ru/search/?text={voice_user_processed}&clid=" +
                     "2270455&banerid=0500000134%3A5f5e284842be7500192177bc&win=454&&lr=39"))

    # Вики
    elif cmd == "wiki" or set(opts["cmds"]["wiki"]) & set(voice_user_processed.split()) != set():
        # Найти информацию в википедии
        notification()
        object = voice_user_processed
        for x in opts["cmds"]["wiki"]:
            object = object.replace(x, "").strip()
        try:
            info = find_wikipedia(object)
            ss = wikipedia.page(object)
            ss_url = ss.url
            wb.open(str(ss_url))
            say(f'По данным источника википедия:{info}')

        except:
            # если не удалось - поиск в браузер
            say("Неудалось найти запрос в википедии. Открываю браузер")
            wb.open((f"https://yandex.ru/search/?text={voice_user_processed}&clid=" +
                     "2270455&banerid=0500000134%3A5f5e284842be7500192177bc&win=454&&lr=39"))

    # Открыть вк
    elif cmd == 'VK':
        # Открыть VK
        notification()
        wb.open("https://vk.com/feed")

    # YouTube
    elif cmd == "YT":
        # Открыть YouTube
        notification()
        wb.open("https://www.youtube.com/")

    # Браузер
    elif cmd == "WB":
        # Открыть браузер
        notification()
        wb.open("https://yandex.ru")

    # Шутки
    elif cmd == 'stupid1':
        # рассказать анекдот
        joke = cc_answers["ans"]["joke"]
        say(joke[random.randint(0, len(joke) - 1)])

    else:
        # Если запрос не входит в встроенные команды голосового помошника
        if cmd == 'exit':
            # Выключение голосового помошника
            say("Досвидания")
            root.destroy()

        elif voice_user_processed != '':
            say("Вот что удалось найти по данному запросу в интернете:")
            voice_user_processed = del_key_word(voice_user_processed, 'web')
            wb.open(f"https://yandex.ru/search/?text={voice_user_processed}&clid=" +
                    "2270455&banerid=0500000134%3A5f5e284842be7500192177bc&win=454&&lr=39")

        else:
            # Для случая если нет запроса от пользователя при прослушивании микрофона
            out_put_mess("Команда не распознана, повторите!")


# запись и обработка звука
def recognize():
    try:
        with sr.Microphone() as sours:
            r.adjust_for_ambient_noise(sours)
            audio = r.listen(sours)
            voices_user = r.recognize_google(audio, language="ru_RU").capitalize()
            t = ("-Распознано: {text_u}".format(text_u=voices_user))
            t = mess_factura(t)
            out_put_mess(t)
            voices_user = voices_user.lower()

            if voices_user.startswith(opts["alias"]):
                # обращаются к вайлет
                cmd = voices_user

                for x in opts['alias']:
                    cmd = cmd.replace(x, "").strip()

                for x in opts['tbr']:
                    cmd = cmd.replace(x, "").strip()

                # распознаем и выполняем команду
                txt = cmd
                cmd = recognize_cmd(cmd)
                execute_cmd(cmd['cmd'], txt)

            else:
                input_mess("Нет обращения. Не будет исполнено\n" + '\n')

    except sr.UnknownValueError:
        input_mess("Голос не распознан!\n" + '\n')

    except sr.RequestError:
        input_mess("Неизвестная ошибка, проверьте интернет!\n" + '\n')


# поиск в вики
def find_wikipedia(what):
    wikipedia.set_lang("Ru")
    wiki_find = wikipedia.summary(what)

    # обработка ответа(вырезаем 2 предложения) и убераем информацию в кавычках
    i = 0
    while i < len(wiki_find):
        while i < len(wiki_find) and wiki_find[i] != "(":
            i += 1
        j = i
        while j < len(wiki_find) and wiki_find[j] != ")":
            j += 1

        wiki_find = wiki_find[:i] + wiki_find[j + 1:]

    list_sun = wiki_find.split(".")

    res = ""
    for i in range(2):
        res += list_sun[i] + "."

    return res


# «Говорящие часы» — программа озвучивает системное время
def date_time():
    time_checker = datetime.now()  # Получаем текущее время с помощью datetime

    day_month_year = ('Сегодня: {d} {M} {G}'.format(d=time_checker.day, M=time_checker.month, G=time_checker.year))
    n_time = ('Время: {h} :{m}'.format(h=time_checker.hour, m=time_checker.minute))

    return day_month_year, n_time


# погода
def get_weather_in_city(city):
    try:
        config_dict = get_default_config()
        config_dict['language'] = 'ru'
        owm = OWM('5e1a6c4926d593ea4ebd74577cd51526', config_dict)
        mgr = owm.weather_manager()

        # Поиск текущей погоды города и получить подробную информацию
        observation = mgr.weather_at_place(city)
        w = observation.weather

        # температура и статус
        tempretura = w.temperature("celsius")
        status = w.detailed_status

        res = "в городе %s сейчас %s %.0f градусов по цельсию" % (city, status, tempretura["temp"])

        return res

    except:
        get_weather_in_city(city)


# реализация перевода EN-RU
def get_translate(text):
    en_to_ru = translate.Translator(from_lang="eu", to_lang="ru")
    ru_to_en = translate.Translator(from_lang="ru", to_lang="en")

    translated_text_in_ru = en_to_ru.translate(text)
    translated_text_in_eu = ru_to_en.translate(text)

    return translated_text_in_eu, translated_text_in_ru


# вывод текста в виджет Text (вайлет)
def input_mess(t):
    global TEXT
    TEXT.configure(state=NORMAL)
    TEXT.insert(END, t)
    TEXT.configure(state=DISABLED)


# вывод текста в виджет Text (пользователь)
def out_put_mess(t):
    global TEXT
    TEXT.configure(state=NORMAL)
    T = t.split('\n')
    for i in T:
        s = str(float(TEXT.index(INSERT)) + 0.51)
        TEXT.insert(END, i)
        e = str(TEXT.index(INSERT))
        TEXT.insert(END, '\n')
        TEXT.tag_add('st', s, e)
    TEXT.tag_config("st", background="purple", foreground="white")
    TEXT.configure(state=DISABLED)


# Всплывающее окно информации
def informational():
    with open(resource_path('i.txt'), 'r', encoding='utf-8') as file:
        L = file.read()

        root_i = Toplevel(root)
        label_inf = Label(root_i, text=L, fg='black', justify=LEFT)
        label_inf.pack()
        root_i.mainloop()


# Всплывающее окно информации
def error():
    with open(resource_path('err.txt'), 'r', encoding='utf-8') as file:
        L = file.read()

        root_e = Toplevel(root)
        label_inf = Label(root_e, text=L, fg='black', justify=LEFT)
        label_inf.pack()
        root_e.mainloop()


# Обработка сообщений(Строковый вид опр. длины)
def mess_factura(t):
    rec = textwrap.fill(t, width=30)

    a = rec.split('\n')
    res = ''
    for i in a:
        res += ' ' * 51 + i + '\n'

    return res


# Очистка сесии
def clr():
    global TEXT
    TEXT.configure(state=NORMAL)
    TEXT.delete("1.0", "end")
    TEXT.configure(state=DISABLED)


# Импортировать фото (Таким образом т.к. упаковка не работает без этого)
def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)


# переменные для приветствия и само приветствие
def hi():
    t = date_time()[1]
    w = get_weather_in_city("Ростов-на-Дону")
    s = f"Приветствую. {t}. За окном {w}. Хорошего времяпрепровождения!"
    say(s)


# запуск
r = sr.Recognizer()
tts = pyttsx3.init()
voices = tts.getProperty("voices")
tts.setProperty("voice", "ru")
user_silence_time = 0

# настройки окна
root = Tk()

root.title('Вайлет')
root.geometry('400x700')
root.resizable(width=False, height=False)
root.iconbitmap(resource_path('icon_1.ico'))


image_start = PhotoImage(file=resource_path('stop1.png'))

# Виджет Text
TEXT = Text(root, width=57, height=38, state=DISABLED, font=('Berlin Sans FB Demi', 10))
TEXT.place(x=0, y=0)

# подключение скрола
st = ScrolledText(root)
st.place(in_=TEXT, relx=1.0, relheight=1.0, bordermode="outside")

# кнопка старта
Start = Button(image=image_start, borderwidth=0, command=lambda: recognize())
Start.place(x=170, y=625)

# Выплывающее меню
main_menu = Menu(root)

f = Menu(main_menu, tearoff=0)
f.add_command(label='Возможности', command=informational)
f.add_command(label='Ошибки', command=error)
f.add_command(label='Очистить сессию', command=clr)

main_menu.add_cascade(label='...', menu=f)

root.configure(menu=main_menu)

# Приветствие
hi()

# Запуск интерфейса
root.mainloop()
