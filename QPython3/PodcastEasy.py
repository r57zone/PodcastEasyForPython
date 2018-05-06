#qpy:qpyapp
#Podcast Easy 0.7 (06.05.2018) by r57zone
#http://r57zone.github.io
#QPython3

import urllib.request, re, os, androidhelper

droid = androidhelper.Android()

def HTTPGet(Url):
	try:
		Responce = urllib.request.urlopen(Url)
		Source = str(Responce.read())
	except:
		Source = ''
	return Source

def DownloadFile(Url, Path):
	FileName = os.path.splitext(Url.split('/')[-1])[0]
	FileExt = os.path.splitext(Url)[1]
	if os.path.exists(Path + FileName + FileExt):
		FileExistsCounter = 0
		while True:
			FileExistsCounter += 1
			try:
				if not os.path.exists(Path + FileName + '(' + str(FileExistsCounter) + ')' + FileExt):
					DownloadFileName = Path + FileName + '(' + str(FileExistsCounter) + ')' + FileExt
					break
			except:
				pass
	else:
		DownloadFileName = Path + FileName + FileExt

	try:
		urllib.request.urlretrieve(Url, DownloadFileName)
		return True
	except:
		return False

		
def main():
	
	#====================
	#Настройки / Settings
	#--------------------
		
	DownloadPath = '/sdcard/Podcasts/'
	
	#--------------------
	#Загружать подкасты / Download podcasts
	#After adding a new feed is recommended to skip downloading all new podcasts.
	
	DownloadPodcasts = False
	#DownloadPodcasts = True
	
	#--------------------
	#Расширения подкастов / Podcasts extensions
	
	PodcastExt = 'mp3|aac|ogg|mp4';
	
	#=====================

	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	RSSList = open('RSS.txt', 'r').readlines()
	RSSCount = len(RSSList)
	Downloaded = open('Downloaded.txt', 'r').read()
	
	#Список для загрузки файлов / List to download files
	Download = []
	
	droid.dialogCreateHorizontalProgress('Podcast Easy', 'Checking news feeds', RSSCount)
	droid.dialogShow()
	
	for i, Address in enumerate(RSSList):
	
		droid.dialogSetCurrentProgress(i + 1)
	
		#Лента / Rss
		Source = HTTPGet(Address)
		if Source == '':
			continue
		
		#Atom
		Links = re.findall('<content.*?src="(.*?' + PodcastExt + ')"', Source)
		#RSS 2.0
		Links += re.findall('<enclosure.*?url="(.*?' + PodcastExt +')"', Source)

		for Link in Links:
		
			#Проверяем добавлялась ли ссылка в список загрузки / Checking if the link was added to the download list
			if not Link in Download:
							
				#Проверяем была ли загружена ссылка ранее / Checking if the link was previously downloaded
				if not Link in Downloaded:
					droid.makeToast('Found new podcast on ' + Address.replace("\n",''))
				
					#Добавление ссылки в список для загрузки / Add link to download list
					Download.append(Link)
	
	droid.dialogDismiss()
	
	DownloadedFile=open('Downloaded.txt', 'a')
	
	#Счетчик загруженных файлов / Counter donwloaded files
	DownloadedCount=0
	#Счетчик ошибок загрузки / Counter error downloaded
	ErrorCount=0
	
	droid.dialogCreateHorizontalProgress('Podcast Easy', 'Podcast downloaded', len(Download))
	droid.dialogShow()

	if Download:
	
		#Загрузка файлов / Download files
		for Link in Download:
			if DownloadPodcasts:
				if DownloadFile(Link, DownloadPath):
					
					#Сохранение ссылок на загруженные подкасты, чтобы не загружать их снова / Save links to downloaded podcasts to not download them again
					DownloadedFile.write(Link + "\n")
					
					DownloadedCount += 1
					
					droid.dialogSetCurrentProgress(DownloadedCount)
				else:
					ErrorCount += 1
			else:
				DownloadedFile.write(Link + "\n")
				DownloadedCount = 1
	
	droid.dialogDismiss()
	
	if not ErrorCount and DownloadedCount:
		if DownloadPodcasts:
			droid.makeToast('All podcasts downloaded')
		else:
			droid.makeToast('All podcasts skipped')
	else:
		if not (ErrorCount and DownloadedCount):
			droid.makeToast('New podcasts not found')
		else:
			droid.makeToast('Download error, downloaded podcasts: {}'.format(DownloadedCount))
	
	DownloadedFile.close()

    #Предупреждение / Warning
	if not DownloadPodcasts:
		droid.makeToast('Downloading new podcasts is disabled. To enabled download, change parameter "DownloadPodcasts" to "True" in the code.')


if __name__=='__main__':
	main()
