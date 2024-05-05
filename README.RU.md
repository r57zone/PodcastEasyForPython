[![EN](https://user-images.githubusercontent.com/9499881/33184537-7be87e86-d096-11e7-89bb-f3286f752bc6.png)](https://github.com/r57zone/PodcastEasyForPython/) 
[![RU](https://user-images.githubusercontent.com/9499881/27683795-5b0fbac6-5cd8-11e7-929c-057833e01fb1.png)](https://github.com/r57zone/PodcastEasyForPython/blob/master/README.RU.md)

# Podcast Easy
Приложение для загрузки подкастов. Доступны версии для Python 2.7, Python 3, QPython3 (Android) и [Windows](https://github.com/r57zone/PodcastEasy).


Введите RSS ленты в файл `RSS.txt` и запустите программу. После успешного выполнения программы поменяйте значение параметра `DownloadPodcasts`, в файле `PodcastEasy.py`, с `False` на `True` (60 строка для 2.7, 54 строка для 3 и 53 строка для QPython3). Изменение необходимо для того, чтобы в первый раз не загружались все подкасты из RSS лент.


Время от времени (раз в 2-4 месяца), желательно очищать базу устаревших ссылок, чтобы поиск новых подкастов не замедлялся. Для этого нужно запустить скрипт `RemOutdatedLinks.py`.

## Обратная связь
`r57zone[собака]gmail.com`