# Podcast Easy 0.4 (27.08.2016) by r57zone
# http://r57zone.github.io
# Python 3.4
import re
import urllib.request, os
from pprint import pprint
from urllib.error import URLError, HTTPError
from pathlib import Path


def get_url(url):
    try:
        resp = urllib.request.urlopen(url)
        html = str(resp.read())
    except (URLError, HTTPError):
        html = ''
    return html


def download_file(url, path):
    filename = url.split('/')[-1]
    if not os.path.exists(path + filename):
        try:
            urllib.request.urlretrieve(url, path + filename)
            return True
        except (URLError, HTTPError):
            return False

    files_counter = 0
    while True:
        files_counter += 1
        save_path = path + filename.split('.mp3')[0] + '({}).mp3'.format(files_counter)
        if not os.path.exists(save_path):
            try:
                urllib.request.urlretrieve(url, save_path)
                return True
            except (URLError, HTTPError):
                return False


# RegExp для поиска ссылок в строке / RegExp for searching a link in string
URL_REGEX = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
URL_REGEX = re.compile(URL_REGEX)

# Путь для загрузки подкастов / Path for downloading podcasts
DOWNLOAD_PATH = ''
# Загружать ли подкасты? / Download podcasts?
DOWNLOAD_PODCASTS = True
DOWNLOADED_PATH = Path.cwd() / 'downloaded.txt'

def main():
    print('Podcast Easy 0.4')

    rss_file = open(Path.cwd() / 'rss.txt', 'r').readlines()
    downloaded = open(DOWNLOADED_PATH, 'r').read()
    # Список для загрузок файлов / List for files to download
    download_list = []

    count = 0
    for match in URL_REGEX.findall(''.join(rss_file)):
        count += 1
        address = ''.join(match)
        # Лента / RSS
        rss_data = get_url(address)
        if not rss_data:
            continue
        rss_count = len(rss_file)
        print('Проверка новостных лент: {} из {}'.format(count, rss_count))
        for match in URL_REGEX.findall(rss_data):
            line = ''.join(match).strip()
            # Если в строке нет MP3 или GUID, то продолжаем
            if 'mp3' not in line and '<guid' not in line:
                continue
            link = line.split('<guid')[0]
            # Если ссылка не кончается на .mp3
            if not link.endswith('.mp3'):
                continue
            # Если в ссылке есть "HTTP" (включая HTTPS)
            # If there's "HTTP" in link (including HTTPS)
            if 'http' in link:
                # Проверяем ссылку на наличие в ее списке загруженных подкастов
                # Check presence of link on list of downloaded podcasts
                if link not in downloaded and link not in download_list:
                    # EN=Found a new podcast on
                    print('Найден новый подкаст на ' + address.replace('\n', ''))
                    # Добавление ссылки в список для загрузки
                    # Adding link to download list
                    download_list.append(link)

    downloaded_file = open(DOWNLOADED_PATH, 'a')

    # Счетчик загруженных файлов / Counter donwloaded files
    downloaded_count = 0
    # Счетчик ошибок загрузки / Counter error downloaded
    error_count = 0

    if download_list:
        if DOWNLOAD_PODCASTS:
            # EN=Downloading podcasts : 0 of
            print('Загружено подкастов: 0 из {}'.format(len(download_list)))
        else:
            # Все подкасты успешно загружены / All podcasts downloaded
            downloaded_count = 1

    # Загрузка файлов / Download files
    for link in download_list:
        if DOWNLOAD_PODCASTS:
            if download_file(link, DOWNLOAD_PATH):
                downloaded_count += 1
                # Сохранение ссылок на загруженные подкасты, чтобы не загружать их снова
                # Save links to downloaded podcasts to not download them again
                downloaded_file.write(link + '\n')
                # EN=Downloading podcasts : of
                print('Загружено подкастов: {} из {}'.format(downloaded_count, len(download_list)))
            else:
                error_count += 1
        else:
            downloaded_file.write(link + '\n')


    if error_count or downloaded_count:
        if not error_count:
            # EN=All podcasts have been downloaded
            print('Все подкасты загружены')
        else:
            # EN= Failed downloading {} podcasts :
            print('Не удалось загрузить {} подкастов'.format(error_count))
    if not (error_count and downloaded_count):
        # EN=No new podcasts are found
        print('Новых подкастов не найдено')

    downloaded_file.close()
    # EN=Press ENTER to execute the command
    input('Нажмите Enter, чтобы выйти....')


if __name__ == '__main__':
    main()
