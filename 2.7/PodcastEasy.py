#Podcast Easy 0.7 (19.02.2018) by r57zone
#http://r57zone.github.io
#Python 2.7.14

import urllib2, re, os, platform

def HTTPGet(Url):
	try:
		Responce = urllib2.urlopen(Url)
		Source = Responce.read()
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
		Response = urllib2.urlopen(Url)
	except:
		pass
		
	if Response:
		Output = open(DownloadFileName, 'wb')
		Output.write(Response.read())
		Output.close()
		return True
	else:
		return False

def main():
	
	#====================
	#Настройка / Settings
	#--------------------
	
	
	#Пример / Example
	#Windows - "C:\\Users\\User\\Desktop\\", Linux - "/home/"
	
	DownloadPath = ''
	
	#--------------------
	#Загружать подкасты / Download podcasts
	#After adding a new feed is recommended to skip downloading all new podcasts.
	
	DownloadPodcasts = False
	#DownloadPodcasts = True
	
	#--------------------
	#Расширения подкастов / Podcasts extensions
	
	PodcastExt = 'mp3|aac|ogg|mp4';
	
	#=====================

	
	#Системный слэш / System slash 
	if platform.system() == 'Windows':
		SysSlash = '\\'
	else:
		SysSlash = '/'

	RSSList = open(os.getcwd() + SysSlash + 'RSS.txt', 'r').readlines()
	RSSCount = len(RSSList)
	Downloaded = open(os.getcwd() + SysSlash + 'Downloaded.txt', 'r').read()
	
	if DownloadPath == '':
		DownloadPath = os.getcwd() + SysSlash

	#Список для загрузки файлов / List to download files
	Download = []
	
	print ('Podcast Easy')
	
	for i, Address in enumerate(RSSList):
	
		print ('Checking news feeds: {} of {}'.format(i + 1, RSSCount))
	
		#Лента / Rss
		Source = HTTPGet(Address)
		if Source == '':
			continue
		
		#Atom
		Links = re.findall('<content.*?src="(.*?' + PodcastExt + ')"', Source)
		#RSS 2.0
		Links += re.findall('<enclosure.*?url="(.*?' + PodcastExt + ')"', Source)

		for Link in Links:
		
			#Проверяем добавлялась ли ссылка в список загрузки / Checking if the link was added to the download list
			if not Link in Download:
							
				#Проверяем была ли загружена ссылка ранее / Checking if the link was previously downloaded
				if not Link in Downloaded:
      
					print ('Found new podcast on ' + Address.replace("\n",''))
				
					#Добавление ссылки в список для загрузки / Add link to download list
					Download.append(Link)
	
	DownloadedFile=open(os.getcwd() + SysSlash + 'Downloaded.txt', 'a')
	
	#Счетчик загруженных файлов / Counter donwloaded files
	DownloadedCount=0
	#Счетчик ошибок загрузки / Counter error downloaded
	ErrorCount=0

	if Download:
		#Загрузка файлов / Download files
		for Link in Download:
			if DownloadPodcasts:
				if DownloadFile(Link, DownloadPath):
					
					#Сохранение ссылок на загруженные подкасты, чтобы не загружать их снова / Save links to downloaded podcasts to not download them again
					DownloadedFile.write(Link + "\n")
					
					DownloadedCount += 1
					print('Podcasts downloaded: {} of {}'.format(DownloadedCount, len(Download)))
				else:
					ErrorCount += 1
			else:
				DownloadedFile.write(Link + "\n")
				DownloadedCount = 1
	
	
	if not ErrorCount and DownloadedCount:
		if DownloadPodcasts:
			print('All podcasts downloaded')
		else:
			print('All podcasts skipped')
	else:
		if not (ErrorCount and DownloadedCount):
			print('New podcasts not found')
		else:
			print('Download error, downloaded podcasts: {}'.format(DownloadedCount))
	
	DownloadedFile.close()

    #Предупреждение / Warning
	if not DownloadPodcasts:
		print('Downloading new podcasts is disabled. To enabled download, change parameter "DownloadPodcasts" to "True" in the code.')

if __name__=='__main__':
	main()
