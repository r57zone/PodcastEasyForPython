#qpy:qpyapp
#Podcast Easy 0.7 Removing outdated links (06.05.2018) by r57zone
#Pttp://r57zone.github.io
#QPython3

import urllib.request, os, androidhelper

droid = androidhelper.Android()

def HTTPGet(Url):
	try:
		Responce = urllib.request.urlopen(Url)
		Source = str(Responce.read())
	except:
		Source = ''
	return Source

def main():

	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	RSSList = open('RSS.txt', 'r').readlines()
	Downloaded = open('Downloaded.txt', 'r').readlines()
	DownloadedFile = open('Downloaded.txt', 'w')

	#Все ленты / Source of all feeds
	Source = ''
	#Количество удаленных ссылок / Removed link count
	LinksCount = 0
	#Ошибка
	GetFeedError = False
	
	droid.dialogCreateSpinnerProgress('Podcast Easy', 'Preparing the common list')
	droid.dialogShow()
	
	#Создание общего списка / Creating a common list
	for i, Address in enumerate(RSSList):
	
		FeedSource = HTTPGet(Address)
		if FeedSource == '':
			droid.dialogDismiss()
			
			droid.dialogCreateAlert('Podcast Easy', 'Error, feed "{}" not available. If it ceased to exist, then simply remove it and try again.'.format(Address))
			droid.dialogSetPositiveButtonText('Ok')
			droid.dialogShow()
			
			GetFeedError = True
			break
			
		Source += FeedSource

	if not GetFeedError:	
		droid.dialogDismiss()
		
		droid.dialogCreateSpinnerProgress('Podcast Easy', 'Checking links in list')
		droid.dialogShow()
	
	#Проверка ссылок / Checking links
	for Line in Downloaded:
		if Source.find(Line.replace('\n', '')) == -1:
			LinksCount += 1
		else:
			DownloadedFile.write(Line.replace('\n', '') + '\n') # Перенос строки всегда

	if not GetFeedError:
		droid.dialogDismiss()
		
		droid.dialogCreateAlert('Podcast Easy', 'Removed outdated links: {}'.format(LinksCount))
		droid.dialogSetPositiveButtonText('Ok')
		droid.dialogShow()
 
	DownloadedFile.close()

if __name__=='__main__':
	main()
