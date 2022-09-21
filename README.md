# GoIP-SMS

Отправка СМС со шлюза GoIP в Asterisk

Для настройки отредактировать сторки

```
goipAddr = '192.168.1.221'
goipUsr = 'admin'
goipPass = 'admin'
selCan = {1: 223, 2: 212, 3: 213, 4: 214, 5: 215}
```

В словаре ```selCan``` задаются соответствия номера ров каналов и абонементов

Отредактировать ```ari.conf```:

```
[general]
enabled = yes
pretty = yes
allowed_origins = localhost:8088,http://ari.asterisk.org,localhost:8088,localhost:8081

[asterisk]
type = user
read_only = no
password = asterisk
```

Отредактировать ```http.conf```
```
[general]
enabled=yes
enablestatic=yes
;bindaddr=0.0.0.0
bindaddr=127.0.0.1
bindport=8088
```
