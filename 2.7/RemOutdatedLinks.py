#Podcast Easy 0.7 Removing outdated links (19.02.2018) by r57zone
#Pttp://r57zone.github.io
#Python 2.7.14

import urllib2, os, platform

def HTTPGet(Url):
	try:
		Responce = urllib2.urlopen(Url)
		Source = Responce.read()
	except:
		Source = ''
	return Source

def main():
	
	print ('Podcast Easy - Removing outdated links')
	
	#Системный слэш / System slash 
	if platform.system() == 'Windows':
		SysSlash = '\\'
	else:
		SysSlash = '/'

	RSSList = open(os.getcwd() + SysSlash + 'RSS.txt', 'r').readlines()
	Downloaded = open(os.getcwd() + SysSlash + 'Downloaded.txt', 'r').readlines()
	DownloadedFile = open(os.getcwd() + SysSlash + 'Downloaded.txt', 'w')

	#Все ленты / Source of all feeds
	Source = ''
	#Количество удаленных ссылок / Removed link count
	LinksCount = 0
	#Ошибка
	GetFeedError = False
	
	#Создание общего списка / Creating a common list
	print('Preparing the common list')
	for i, Address in enumerate(RSSList):
	
		FeedSource = HTTPGet(Address)
		if FeedSource == '':
			print('Error, feed "{}" not available.\nIf it ceased to exist, then simply remove it and try again.'.format(Address))
			GetFeedError = True
			break
			
		Source += FeedSource
		
	if not GetFeedError:	
		print('Checking links in list')
	
	#Проверка ссылок / Checking links
	for Line in Downloaded:
		if Source.find(Line.replace('\n', '')) == -1:
			LinksCount += 1
		else:
			DownloadedFile.write(Line.replace('\n', '') + '\n') # Перенос строки всегда
	
	if not GetFeedError:	
		print('Removed outdated links: {}'.format(LinksCount))
 
	DownloadedFile.close()

if __name__=='__main__':
	main()
