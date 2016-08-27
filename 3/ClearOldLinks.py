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

def main():
	
	print ('')
	print (' Podcast Easy 0.4 clear old links')
	print ('')

	rss=open(os.getcwd()+'\\rss.txt', 'r') #if Linux os replace in path "\\" to "/"
	downloaded=open(os.getcwd()+'\\downloaded.txt', 'r').readlines() #if Linux os replace in path "\\" to "/"
	DownloadedUpdate=open(os.getcwd()+'\\downloaded.txt','w')

	source=''
	LinkCount=0
	
	#Создание общего списка / Creating a common list
	print(' Этап 1 - Подготовка общего списка')
	for i, address in enumerate(rss):
	
		#Лента / Rss
		GetRss=GetUrl(address)
		if GetRss=='-1':
			break
			print('Ошибка, лента "'+address+'" недоступна. Если она перестала существовать, то просто удалите ее из файла "rss.txt" и повторите попытку.')

		source+=GetRss
	print(' Этап 2 - Проверка ссылок в списке')
	
	for line in downloaded:
		if source.find(line.replace("\n",''))==-1:
			LinkCount+=1
		else:
			DownloadedUpdate.write(line.replace("\n",'')+"\n")
	
	print(' Удалено ссылок : '+str(LinkCount))
 
	DownloadedUpdate.close()
	rss.close()
	#EN=Press ENTER to execute the command
	wait=input('\n Нажмите Enter, чтобы выйти....')

if __name__=='__main__':
	main()
