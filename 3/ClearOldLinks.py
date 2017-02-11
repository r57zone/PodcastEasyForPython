# Podcast Easy 0.4 (27.08.2016) by r57zone
# http://r57zone.github.io
# Python 3.4

from pathlib import Path
from PodcastEasy import get_url


def main():
    print(' Podcast Easy 0.4 cleaner')
    cwd = Path.cwd()

    rss = open(cwd / 'rss.txt', 'r')
    downloaded_data = open(cwd / 'downloaded.txt', 'r').readlines()
    downloaded_file = open(cwd / 'downloaded.txt', 'w')

    source = ''
    link_count = 0

    # Создание общего списка / Creating a common list
    print(' Этап 1 - Подготовка общего списка')
    for address in rss:

        # Лента / Rss
        rss_data = get_url(address)
        if not rss_data:
            print('Ошибка, лента "' + address + '" недоступна. ')
            print('Если она перестала существовать, то просто удалите ее из файла "rss.txt"')
            continue

        source += rss_data
    print('Этап 2 - Проверка ссылок в списке')

    for line in downloaded_data:
        if source.find(line.replace('\n', '')) == -1:
            link_count += 1
        else:
            downloaded_file.write(line.replace('\n', '') + '\n')

    print('Удалено ссылок : {}'.format(link_count))

    downloaded_file.close()
    rss.close()
    # EN=Press ENTER to execute the command
    input('Нажмите Enter, чтобы выйти....')


if __name__ == '__main__':
    main()
