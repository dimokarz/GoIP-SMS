# Отправка СМС со шлюза GoIP в Asterisk

## Для настройки скрипта отредактировать сторки:

```
goipAddr = '192.168.1.221'
goipUsr = 'admin'
goipPass = 'admin'
selCan = {1: 223, 2: 212, 3: 213, 4: 214, 5: 215}
```

_В словаре ```selCan``` задаются соответствия номеров каналов GoIP и абонентов Asterisk_

Для работы скрипта необходима библиотека ``BeautifulSoup4``

```pip3 install BeautifulSoup4```

Добавить запуск скрипта в ```crontab```:

## Для настройки Asterisk REST Interface (ARI):

Отредактировать ```ari.conf```:

```
[general]
enabled = yes
pretty = yes
allowed_origins = localhost:8088

[asterisk]
type = user
read_only = no
password = asterisk
```

Отредактировать ```http.conf```:
```
[general]
enabled=yes
enablestatic=yes
;bindaddr=0.0.0.0
bindaddr=127.0.0.1
bindport=8088
```
