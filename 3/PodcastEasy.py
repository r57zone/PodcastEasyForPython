# Podcast Easy 0.4 (27.08.2016) by r57zone
# http://r57zone.github.io
# Python 3.4

import urllib.request, os

def GetUrl(url):
	try:
		responce=urllib.request.urlopen(url)
		html=str(responce.read())
	except:
		html=-1
	return html

def DownloadFile(url,path):
	filename=url.split('/')[-1]
	if os.path.exists(path+filename):
		FileExistsCounter=0
		while True:
			FileExistsCounter+=1
			if not os.path.exists(path+filename[0:filename.find('.mp3')]+'('+str(FileExistsCounter)+').mp3'):
				try:
					urllib.request.urlretrieve(url, path+filename[0:filename.find('.mp3')]+'('+str(FileExistsCounter)+').mp3')
					return True
				except:
					return False
					break
	else:
		try:
			urllib.request.urlretrieve(url, path+filename)
			return True
		except:
			return False

def main():

	# Настройка / Settings
	# Пример / Example "C:\\Users\\User\\Desktop\\" - Windows, "/home/" - Linux
	PathDownloads=''
	# Загружать подкасты / Download podcasts
	DownloadFiles=False
	# ------------------

	print ('')
	print (' Podcast Easy 0.4')
	print ('')
	
	rss=open(os.getcwd()+'\\rss.txt', 'r') # if Linux os replace in path "\\" to "/"
	downloaded=open(os.getcwd()+'\\downloaded.txt', 'r').read() # if Linux os replace in path "\\" to "/"

	# Список для загрузок файлов / List to download file
	download=[]

	for i, address in enumerate(rss):
	
		# Лента / Rss
		GetRss=GetUrl(address)
		if GetRss=='-1':
			continue

		# Перенос тега на новую строку / Move tag to new line
		GetRss=GetRss.replace('<enclosure','\n<enclosure')
		GetRss=GetRss.replace('<pubDate>','\n<pubDate>')
  
		# Костыль для старых лент, например, для "http://pirates.radio-t.com/atom.xml" / Сrutch for old feed, example - "http://pirates.radio-t.com/atom.xml"
		if GetRss.find('<audio src=')!=-1:
			GetRss=GetRss.replace('<audio src=','\n<audio url=')
		GetRss=GetRss.split('\n')
		
		print (' Проверка новостных лент: '+str(i+1)+' из '+str(len(open(os.getcwd()+'\\rss.txt', 'r').readlines()))) # if Linux os replace in path "\\" to "/", EN=Checking news feeds: ... of
		
		for line in GetRss:
   
			# Ищем строку с ".MP3" / Look for line with ".MP3"
			if line.upper().find('.MP3')!=-1:
   
				# Проверям строку на наличие тега "<GUID" / Check line for the presence of tag "<GUID" 
				if line.upper().find('<GUID')==-1:
    
					# Ссылка на mp3 файл / Link to mp3 file
					MyLink=line[line.upper().find('URL="')+5:line.upper().find('.MP3')+4]
	 
					if MyLink.upper()[0:7]=='HTTP://' or MyLink.upper()[0:8]=='HTTPS://':
	 
						# Проверяем ссылку на наличие в ее списке загруженных подкастов / Check presence of link on list of downloaded podcasts
						if downloaded.find(MyLink)==-1:
							
							# Проверяем не добавлена ли она уже в список загрузки / Check if it is added in the download list
							if not MyLink in download:
      
								print (' Найден новый подкаст на '+address.replace("\n",'')) # EN=Found a new podcast on
								# Добавление ссылки в список для загрузки / Add link to download list
								download.append(MyLink)
								
	
	if os.path.exists(os.getcwd()+'\\downloaded.txt'): # if Linux os replace in path "\\" to "/"
		DownloadedUpdate=open(os.getcwd()+'\\downloaded.txt', 'a') # if Linux os replace in path "\\" to "/"
	else:
		DownloadedUpdate=open(os.getcwd()+'\\downloaded.txt', 'w') # if Linux os replace in path "\\" to "/"
	
	# Счетчик загруженных файлов / Counter donwloaded files
	DownloadedCount=0
	# Счетчик ошибок загрузки / Counter error downloaded
	ErrorCount=0
	
	if len(download)>0:
		if DownloadFiles:
			# EN=Downloading podcasts : 0 of 
			print(' Загружено подкастов : 0 из '+str(len(download)))
		else:
			# Все подкасты успешно загружены / All podcasts downloaded
			DownloadedCount=1
	
	# Загрузка файлов / Download files
	for link in download:
		if DownloadFiles:
			if DownloadFile(link,PathDownloads)!='-1':
				# Сохранение ссылок на загруженные подкасты, чтобы не загрузить их снова / Save links to downloaded podcasts to not download them again
				DownloadedUpdate.write(link+"\n")
				DownloadedCount+=1
				# EN=Downloading podcasts : of
				print(' Загружено подкастов : '+str(DownloadedCount)+' из '+str(len(download))) 
			else:
				ErrorCount+=1
		else:
			DownloadedUpdate.write(link+"\n")

	if ErrorCount>0 or DownloadedCount>0:
		if ErrorCount==0:
			# EN=All podcasts downloaded
			print(' Все подкасты загружены') 
		else:
			# EN=Failed download podcasts : 
			print(' Не удалось загрузить подкастов : '+str(ErrorCount))
	if ErrorCount==0 and DownloadedCount==0:
		# EN=Not found new podcasts
		print(' Новых подкастов не найдено')
 
	rss.close()
	DownloadedUpdate.close()
	# EN=Press ENTER to execute the command
	wait=input('\n Нажмите Enter, чтобы выйти....')

if __name__=='__main__':
	main()
