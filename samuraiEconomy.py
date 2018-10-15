import discord
from discord.ext import commands

def setup(bot):
	bot.add_cog(BankCog(bot))


class BankCog:
	def __init__(self, bot):
		self.bot = bot
		self.centralBank=Bank()

	@commands.command()
	async def accounts(self):
		await self.bot.say(self.centralBank.getAccountList())

	@commands.command()
	async def createAccount(self, name):
		self.centralBank.createAccount(name)
		await self.bot.say("Created account named "+name)

	@commands.command()
	async def deposit(self, name, num):
		self.centralBank.deposit(name, num)
		await self.bot.say(self.centralBank.getAccount(name).getAmount())

	@commands.command()
	async def withdraw(self, name, num):
		money=self.centralBank.withdraw(name, num)
		await self.bot.say("Here is "+money+" don't lose it.")

	@commands.command()
	async def show(self, name):
		amt=self.centralBank.getAccount(name).getAmount()
		await self.bot.say(amt)


class Bank:
	def __init__(self):
		self.AccountList=[]

	def createAccount(self, name):
		self.AccountList.append(Account(name))

	def getAccount(self, name):
		for act in self.AccountList:
			if name==act.name:
				return act
	def getAccountList(self):
		return self.AccountList

	def deposit(self, name, num):
		self.getAccount(name).add(num)
	
	def withdraw(self, name, num):
		return self.getAccount(name).take(num)


class Account:
	def __init__(self, name):
		self.amount=0
		self.name=name

	def take(self, num):
		self.amount-=int(num)
		return num

	def add(self, num):
		self.amount+=int(num)

	def getAmount(self):
		return self.amount








'''
class ScrapeForum:

	directUrl="http://forum.openwar.org/t/the-warriors-bank/10786"

	def scrape(self):
		page =requests.get(directUrl)
		soup = BeautifulSoup(page.content, 'html.parser')
		postInfo=str(soup.find_all('div', {"class" : "reply"}))

class Account:
	def __init__(self, name):
		self.gold=0
		self.silver=0
		self.copper=0
		self.name=name

	def take(self, num):
		
		
	def add(self, num):
		addGold(num//100)
		addSilver(num//10%10)
		addCopper(num%10)

	def addGold(self,num):
		self.gold+=num

	def addSilver(self,num):
		self.silver+=num

	def addCopper(self,num):
		self.copper+=num

	def getAccount(self):
		return [self.gold, self.silver, self.copper]
'''