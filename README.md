<<<<<<< HEAD
# Телеграм-бот для поиска отелей по всему миру (кроме РФ)

## Настройка бота:
=======
# Телеграм-бот по поиску отелей по всему миру (без РФ, РБ)

### 1. Настройка бота:
>>>>>>> origin/master

- Создать файл .env в корневой папки с ботом.
- Добавить значения констант:

<<<<<<< HEAD
```
BOT_TOKEN - токен Телеграм бота 
            (Можно получить после создания в боте @BotFather)
RAPID_API_KEY - ключ для работы с АПИ, 
                получить можно после регистрации на сайте rapidapi.com
```


 - Из файла requirements.txt необходимо установить все пакеты.

```
pip install -r requirements.txt
```

## Запуск бота:

 - Запуск бота производится через скрипт в корне проекта
```
python main.py
```
 
## Инструкция по использованию бота:

При запуске бота в клиенте пользователю будут доступны следующие команды:

/start - запуск бота
=======
BOT_TOKEN - токен Телеграм бота (Можно получить после создания в боте @BotFather)
RAPID_API_KEY - ключ для работы с АПИ, получить можно после регистрации на сайте rapidapi.com
===================================================================================
### 2. Требования:

- Из файла requirements.txt необходимо установить все пакеты.

``` pip install -r requirements.txt ```
===================================================================================
3. Запуск бота:

Запуск бота производиться напрямую, запуском скрипта main.py

>> python main.py
===================================================================================
4. Инструкция по использованию бота:
>>>>>>> origin/master

/help — помощь по командам бота

/lowprice — вывод самых дешёвых отелей в городе

/highprice — вывод самых дорогих отелей в городе

/bestdeal — вывод отелей, наиболее подходящих по цене и расположению от центра

/history — вывод истории поиска отелей
<<<<<<< HEAD


## Дополнение:

Данные о пользователях и истории поиска в файле БД data_base.db
=======
===================================================================================
5. Дополнение

Данные о пользователях и истории поиска в файле БД data_base.db
===================================================================================
>>>>>>> origin/master
