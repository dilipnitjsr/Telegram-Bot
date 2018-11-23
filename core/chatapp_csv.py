
#615128532:AAGYHWB16Q-6XuItcpVureamKHzwGJMBQxE
#pip install python-telegram-bot --upgrade
#pip install numpy
#pip install pandas
# pip install psycopg2


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import numpy
import pandas as pd

Token = "<?Token?>"
class Bot:

	__removeList = []
	
	def __init__(self):
		#token form bot father
		self.__bot = telegram.Bot(token=Token)
		self.__chatlist = 'chatlist.csv'
		self.__mailler = 'automailler.csv'
		self.__search = 'search.csv'

	def getBot(self):
		return self.__bot

	def getChatList(self):
		return self.__chatlist

	def getMailler(self):
		return self.__mailler

	def getSearch(self):
		return self.__search

	def allUser(self):
		"""
		Read the CSV File and returns as pandas dataframe
		"""
		try:
			frm_csv = pd.read_csv(self.__chatlist)
			return frm_csv
		except Exception as e:
			f = open(self.__chatlist,"w+")
			f.write("id,first_name,username,active,start,end,type")
			f.close()
			return []

	def save(self, dataFrame):
		try:
			dataFrame = dataFrame.drop_duplicates(subset='id', keep='first', inplace=False)
			dataFrame.to_csv(self.__chatlist, sep=',', index=False)
		except Exception as e:
			f = open(self.__chatlist,"w+")
			f.write("id,first_name,username,active,start,end,type")
			f.close()

	def send(self, contactList, message):
		self.__removeList = []
		for contact in contactList:
			while True:
				try:
					self.__bot.send_message(chat_id=contact, text=message)
					print ("Send : "+ str(contact))
					break
				except Exception as e:
					print(e)
					print ("Error : "+ str(contact))
					self.__removeList.append(contact)
		return True

	def getRemoveList(self):
		return self.__removeList

	def remove(self, removeList):
		allList = self.readCSV()
		self.save(allList[~allList.username.isin(removeList)])
		return True

class Chat(Bot):
	"""User Class"""
	def __init__(self, bot):
		self.__bot = Bot.__init__(self)

	def allUser(self):
		"""
		Read the CSV File and returns as pandas dataframe
		"""
		try:
			frm_csv = pd.read_csv(self.getChatList())
			return frm_csv
		except Exception as e:
			f = open(self.getChatList(),"w+")
			f.write("id,first_name,username,active,start,end,type")
			f.close()
			return []

	def getAllGroup(self):
		df = self.allUser()
		return df.loc[df['type'] == 'group']

	def getAllPrivate(self):
		df = self.allUser()
		return df.loc[df['type'] == 'private']
	def getAllPrivateID(self):
		r = self.getAllPrivate()
		return r['id']

	def refresh(self):
		"""
		Get details form internet
		"""
		ids =[]
		updates = self.get_updates()
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
			
class AutoMailler(Bot):
	"""Automailler Class
		12/06/2018, 16:18:30
		DD/MM/YYYY, HH:MM:SS
	"""
	def __init__(self, bot):
		super(AutoMailler, self).__init__()
		self.__bot = Bot.__init__(self)

	def getAll(self):
		try:
			return pd.read_csv(self.getMailler())
		except Exception as e:
			f = open(self.getMailler(),"w+")
			f.close()
			return []

	def addNew(self, msgTime, message):
		allmail = self.getAll()
		df = pd.DataFrame([[msgTime, message]], columns=['time', 'message'])
		allmail = allmail.append(df, ignore_index=True, sort = False)
		allmail.to_csv(self.getMailler(), sep=',', index=False)
		return allmail
	def run(self):
		thread = threading.Thread(target = self.sheduler, args=[])
		thread.start()
		print("To take effect of edit in database, Automailer have to restart.")

	def sheduler(self):
		mails = self.getAll()
		timeList = list(mails['time'])
		message = list(mails['message'])
		print(timeList)
		user_list = self.allUser()
		user_list = user_list.loc[user_list['active'].isin(["Y"])]
		user_list = list(user_list["id"])
		while True:
			cu_time =  t.strftime("%d/%m/%Y, %H:%M:%S")
			print(cu_time)
			if cu_time in timeList:
				idx = timeList.index(cu_time) 


				self.send(user_list, message[idx])
				print("Send to : " + str(user_list))
			t.sleep(1)

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




class Regestration(Bot):
	"""	Reg"""
	def __init__(self):
		super(Regestration, self).__init__()
		self.__bot = Bot.__init__(self)
	
	def refresh(self):
		"""
		Get details form internet
		"""
		ids =[]
		updates = self.getBot().get_updates()
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
	def run(self):
		thread = threading.Thread(target = self.getReg, args=[])
		thread.start()
		print("Thread is running")

	def getReg(self):
		while True:
			try:
				newList = self.newUserList()
				print(newList)
				self.save(newList)
			except Exception as e:
				pass
			time.sleep(1)


	def in_between(self, now, start, end):
		if start <= end:
			return start <= now < end
		else: # over midnight e.g., 23:30-04:15
			return start <= now or now < end

	def polling(self):
		updater = Updater(token=Token)
		dp = updater.dispatcher

		dp.add_handler(CommandHandler("start", self.start))
		dp.add_handler(CommandHandler("help", self.help))
		dp.add_handler(CommandHandler("search", self.search, pass_args=True))
		dp.add_handler(MessageHandler(Filters.text, self.echo))

		updater.start_polling()
		updater.idle()

	def echo(self, bot, update):
		update.message.reply_text("Invalid")

	def help(self, bot, update):
		"""List of command"""
		update.message.reply_text('/start : New Regestration\n /help : list of all command\n/search: Search ')

	def search(self, bot, update, args):
		"""List of command"""
		try:
			data = pd.read_csv(self.getSearch())
			print(update.message.text)
			data = data.loc[data['key'].isin(args)]
			# data = list(data)
			for index, row in data.iterrows():
				form_h, form_m = row["timeForm"].split(":")
				to_h, to_m = row["timrTo"].split(":")
				if self.in_between(datetime.now().time(), time(int(form_h),int(form_m)), time(int(to_h), int(to_m))):
					update.message.reply_text(row["message"])
		except Exception as e:
			print(e)
			update.message.reply_text('Please enter the text.')

	def start(self, bot, update):
		"""Send a message when the command /start is issued."""
		frm_csv = self.allUser()

		ids = []
		details = update

		if not details.message.chat.username:
			details.message.chat.username = details.message.chat.title
		ids.append([details.message.chat_id, details.message.chat.first_name, details.message.chat.username, 'Y',  details.message.date, 'No', details.message.chat.type ])
		
		frames = [frm_csv,pd.DataFrame(ids, columns=['id', 'first_name', 'username', 'active', 'start', 'end', 'type'])]
		all =  pd.concat(frames, axis=0, join='inner')
		all = all.drop_duplicates(subset='id', keep='first', inplace=False)
		all.index = [x for x in range(len(all))] # index recalculate
		self.save(all)

		print(str(details.message.chat.username)+"( "+str(details.message.chat_id)+" ) Added..")

		update.message.reply_text('Regestration Success...\nType /help to get the list of all command')

import threading
import time as t
from datetime import datetime, time
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
ti =  t.strftime("%d/%m/%Y, %H:%M:%S")

b = Bot()
# u = Chat(b)
# user = u.getAllPrivateID()
# b.send(user, "Test")
# c = Chat(b)
# c.refresh()
# # print(c.getAllGroup())
# # b.save(c.newUserList())

a = AutoMailler(b)
a.run()
# print(a.addNew(ti, 'mes thi,s sage'))

b = Regestration()
b.polling()
# k = b.run()

