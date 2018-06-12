
#615128532:AAGYHWB16Q-6XuItcpVureamKHzwGJMBQxE
#pip install python-telegram-bot --upgrade
#pip install numpy
#pip install pandas
import telegram
import numpy
import pandas as pd
import datetime

class Bot:
	__removeList = []
	def __init__(self):
		super(Bot, self).__init__()
		#token form bot father
		self.__bot = telegram.Bot(token='615128532:AAGYHWB16Q-6XuItcpVureamKHzwGJMBQxE')
	
	def getBot(self):
		return self.__bot

	def save(self, dataFrame):
		dataFrame = dataFrame.drop_duplicates(subset='id', keep='first', inplace=False)
		dataFrame.to_csv('chatlist.csv', sep=',', index=False)

	def send(self, contactList, message):
		self.__removeList = []
		for contact in contactList:
			try:
				self.__bot.send_message(chat_id=contact, text=message)
				print ("Send : "+contact)
			except Exception as e:
				print(e)
				print ("Error : "+contact)
				self.__removeList.append(contact)
		return True

	def getRemoveList(self):
		return self.__removeList

	def remove(self, removeList):
		allList = self.readCSV()
		self.save(allList[~allList.username.isin(removeList)])
		return True

class Chat:
	"""User Class"""
	def __init__(self, bot):
		super(Chat, self).__init__()
		self.__bot = bot.getBot()

	def allUser(self):
		"""
		Read the CSV File and returns as pandas dataframe
		"""
		frm_csv = pd.read_csv('chatlist.csv')
		return frm_csv

	def getAllGroup(self):
		df = self.allUser()
		return df.loc[df['type'] == 'group']

	def getAllPrivate(self):
		df = self.allUser()
		return df.loc[df['type'] == 'private']

	def refresh(self):
		"""
		Get details form internet
		"""
		ids =[]
		updates = self.__bot.get_updates()
		for details in updates:
			if not details.message.chat.username:
				details.message.chat.username = details.message.chat.title
			ids.append([details.message.chat_id, details.message.chat.first_name, details.message.chat.username, 'Y',  details.message.date, 'No', details.message.chat.type ])
		return pd.DataFrame(ids, columns=['id', 'first_name', 'username', 'active', 'start', 'end', 'type'])

	def newUserList(self):
		"""
			Load the CSV file and Show details
		"""
		frm_csv = self.allUser()
		frm_net = self.refresh()
		frames = [frm_csv,frm_net]
		all =  pd.concat(frames, axis=0, join='inner')
		all = all.drop_duplicates(subset='id', keep='first', inplace=False)
		all.index = [x for x in range(len(all))] # index recalculate
		return all 
class AutoMailler:
	"""Automailler Class"""
	def __init__(self, bot):
		super(AutoMailler, self).__init__()
		self.__bot = bot

	def getAll(self):
		return pd.read_csv("automailler.csv")

	def addNew(self, msgTime, message, users):
		allmail = self.getAll()
		df = pd.DataFrame([[msgTime, message, users]], columns=['time', 'message', 'user_list'])
		allmail = allmail.append(df, ignore_index=True)
		allmail.to_csv('automailler.csv', sep=',', index=False)
		return allmail
	def run(self):
		thread = threading.Thread(target = self.sheduler, args=[])
		thread.start()
		print("To take effect of edit in database, Automailer have to restart.")

	def sheduler(self):
		mails = self.getAll()
		timeList = list(mails['time'])
		user_list = list(mails['user_list'])
		message = list(mails['message'])
		while True:
			cu_time =  time.strftime("%d/%m/%Y, %H:%M:%S")
			if cu_time in timeList:
				idx = timeList.index(cu_time) 
				self.__bot.send(user_list[idx].split(), message[idx])
				print("Send to : "+ str(user_list[idx]))
			time.sleep(1)

		
class User():
	"""Details of User"""
	def __init__(self, chatID, first_name, userID, active, startDate, endDate):
		super(User, self).__init__()
		self.chatID = chatID
		self.first_name = first_name
		self.userID = userID
		self.active = active
		self.startDate = startDate
		self.endDate = endDate


import threading
import time

ti =  time.strftime("%d/%m/%Y, %H:%M:%S")

b = Bot()
c = Chat(b)
# print(c.getAllGroup())
# b.save(c.newUserList())

a = AutoMailler(b)
a.run()
# print(a.addNew(ti, 'message', 'user'))

