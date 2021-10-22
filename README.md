# ShadowServantsGroupCheck

# Настройка:
### Конфиг в начале скрипта:
```py
session_cookie = '<здесь кук "session" из залогиненой сессии на shadowservants.ru (для доступа к стоимости тасков)>'
```

# Использование:
### Справка:
```shell
$ python main.py --help
usage: main.py [-h] [-g ID] [-n NICK [NICK ...]]

optional arguments:
  -h, --help            show this help message and exit
  -g ID, --group-id ID  Вывести всех участников группы (по умолчанию: 5)
  -n NICK [NICK ...], --nicks NICK [NICK ...]
                        Вывести score игроков
```

### Вывести score игрока(-ов):
```shell
$ python main.py -n TomasGl enty8080
```

### Вывести score всех участников группы:
```shell
$ python main.py -g 5
```

# Скриншоты:
![img.png](screenshot1.png)
![img.png](screenshot2.png)
