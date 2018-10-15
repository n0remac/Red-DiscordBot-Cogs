import requests
import re
import json
import sys
from bs4 import BeautifulSoup



import discord
from discord.ext import commands

def setup(bot):
	bot.add_cog(mangaCog(bot))

class mangaCog:

	def __init__(self, bot):
		self.bot = bot
		self.manga=getManga()



	@commands.command()
	async def find(self, *, message):
		text=self.manga.getLink(message.lower())
		await self.say(text)

	@commands.command()
	async def search(self, *,message):
		results=self.manga.searchLinks(message.lower())
		text=""
		for result in results:
			text+=result+ " "
		
		if len(text)>=2000:
			text=self.makeValid(text)
			tooLong="Not all results were returned due to size limit. Try something more specific."
			self.say(tooLong)
		await self.say(text)

	@commands.command()
	async def chapter(self, num, *,message):
		text=""
		if message.lower() in self.manga.links:
			text=self.manga.getAllPagesLink(num,self.manga.getLink(message.lower()))
		await self.say(text)

	def makeValid(self, message):
		fix=""
		i=0
		while i<2000:
			fix+=message[i]
			i+=1
		return fix

	async def say(self, message):
		print (message)
		if message==None:
			await self.bot.say("Nothing was found.")
		elif len(message)>0:
			await self.bot.say(message)
		else:
			await self.bot.say("Nothing was found.")



class getManga:
	links={}
	def __init__(self):
		self.getMangaLinks()

	def getMangaLinks(self):
		with open('/home/cameron/Projets/Red-DiscordBot/cogs/data.json', 'r') as fp:
			self.links = json.load(fp)

	def getAllPagesLink(self, chapter, link):
		return "http://www.mngdoom.com/"+link+"/"+str(chapter)+"/all-pages"

	def searchLinks(self, name):
		mangaLink=[]
		for n, link in self.links.items():
			if name.lower().strip() in n:
				mangaLink.append(n+" - "+self.links.get(n))

		return mangaLink

	def getLink(self, name):
		if name in self.links:
			return self.links.get(name)
'''
#optional code for scraping and command line

#this might not be working
class commandLineControl:

	def __init__(self):
		self.manga=getManga()
		self.getCommand()


	def getCommand(self):
		toRun=sys.argv[1]

		if toRun == "find":
			self.find(self.parseArguements(2))
		elif toRun=="search":
			self.search(self.parseArguements(2))
		elif toRun=="chapter":
			i=sys.argv[2]
			self.chapter(i, self.parseArguements(3))

	def parseArguements(self, num):
		i=num
		arguements=""
		while i< len(sys.argv):
			arguements+=sys.argv[i]
			i+=1
		return arguements


	def find(self, toFind):
		text=self.manga.getLink(toFind.lower())
		self.say(text)

	def search(self, toSearch):
		results=self.manga.searchLinks(toSearch)
		text=""
		for result in results:
			text+=result+ " "
		
		if len(text)>=2000:
			text=self.makeValid(text)
			tooLong="Not all results were returned due to size limit. Try something more specific."
			self.say(tooLong)
			self.say(text)

	def chapter(self, num, name):
		text=""
		if name.lower() in self.manga.links:
			text=self.manga.getAllPagesLink(num,self.manga.getLink(name.lower()))
		self.say(text)

	def makeValid(self, message):
		fix=""
		i=0
		while i<2000:
			fix+=message[i]
			i+=1
		return fix

	def say(self, message):
		if message==None:
			print ("Nothing was found.")
		elif len(message)>0:
			print(message)
		else:
			print("Nothing was found.")

#the url will have to be cahnged for various websites
class makeMangaFileList:

	directUrl="Manga Website"

	def __init__(self):
		#writeLinkFile()
		self.writeLinkFile()

	def buildDirectList(self):
		directList = [self.directUrl] 		
		i=ord('a')
		while i <=ord('z'):
			directList.append(self.directUrl+"/"+chr(i))
			i+=1
		return directList

		
	def getMangaInfo(self):
		directList=self.buildDirectList()
		mangaInfo=""

		for directPage in directList:
			page =requests.get(directPage)
			soup = BeautifulSoup(page.content, 'html.parser')
			mangaInfo+=str(soup.find_all('a', class_="manga-info-qtip"))
		return mangaInfo



	def createMangaDictionary(self):
		mangaInfo=self.getMangaInfo()
		mangaLinks=[]
#		print(mangaInfo)

		pattern = re.compile(r'href=[\'"]?([^\'" >]+)')
		matches=pattern.finditer(mangaInfo)
		
		linkEndPoints=[]

		mangaNames=[]

		for match in matches:
			linkEndPoints.append(match.end())
			mangaLinks.append(match.group().split("\"")[1])

		for end in linkEndPoints:
			i=end+2
			name=""
			while mangaInfo[i] is not '<':
				name+=mangaInfo[i]
				i+=1
			mangaNames.append(name.lower())
		mangaDict=dict(zip(mangaNames, mangaLinks))
		return mangaDict

	def writeLinkFile(self):
		links=self.createMangaDictionary()
		with open('data.json','w') as fp:
			json.dump(links,fp)

'''
#makeMangaFileList ended

#commandLineControl()