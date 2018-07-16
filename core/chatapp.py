"""
4 June 2018

Telegram API Key

<??>

Dependencies

pip install python-telegram-bot --upgrade
pip install numpy
pip install pandas
pip install psycopg2

Cradensials 

Login Page : <??>
Email : prashant.rcciit@acm.org
Password : <??>
Database : <??>

"""


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import math
import pandas as pd
import os

import psycopg2
import urllib.parse
import threading
import time
from datetime import datetime
from datetime import time as time_format


import logging

# Enable logging
logging.basicConfig(format='[ %(asctime)s ]  %(name)s : %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

Token = "<??>"
db_username = '<??>'
db_password = '<??>'
db_host = '<??>'
db_port = 5432
db_database = '<??>'


class Bot:
	"""
	Bot() is a center class of API.
	__init__()
	__del__()
	getConn()
	getChatList()
	getMailler()
	getSearch()
	send(contactList, message)
	getRemoveList()
	"""
	__removeList = []
	def __init__(self):
		"""
			initilize the Bot Class
		"""
		print("Initilizing... Bot")

		#token form bot father
		self.__bot = telegram.Bot(token=Token)
		self.__db_chatlist = 'chatlist'
		self.__db_mailler = 'automailer'
		self.__db_search = 'search'
		self.__conn = False
		try:
			self.open()
		except Exception:
			print("Internet Error...")
			pass

	def open(self):
		"""
		Open new connection
		"""
		print("Database Connecting...")
		self.__conn = psycopg2.connect(database=db_database,
			user= db_username,
			password=db_password,
			host=db_host,
			port=db_port
		)
	def close(self):
		"""
		Close the connection
		"""
		print("Connection closed!")
		if self.__conn:
			self.__conn.close()

	def __del__(self):
		"""
			Close the connection
		"""
		try:
			print("Connection closed!")
			self.__conn.close()
		except Exception:
			pass
	def getConn(self):
		"""
		@return : __conn
		"""
		return self.__conn

	def getBot(self):
		"""
		@return : __bot  
		"""
		return self.__bot

	def getChatList(self):
		"""
		@return : __db_chatlist  
		"""
		return self.__db_chatlist

	def getMailler(self):
		"""
		@return : __db_mailler  
		"""
		return self.__db_mailler

	def getSearch(self):
		"""
		@return :  
		"""
		return self.__db_search

	def send(self, contactList, message):
		"""
		send the message to multiple  contact list
		@return : True
		"""
		self.__removeList = []
		for contact in contactList:
			while True:
				try:
					self.__bot.send_message(chat_id=contact, text=message)
					print ("Send : "+ str(contact))
					break
				except Exception as e:
					if (e == 'block__error'):
						#TODO:
						break
					print ("Error : "+ str(contact))
					self.__removeList.append(contact)
		return True

	def getRemoveList(self):
		"""
		@return : list of last failed SMS ID
		"""
		return self.__removeList

class User(Bot):
	"""
	--User Class
	"""
	def __init__(self):
		Bot.__init__(self)
		print("Initilizing... User")

	def remove(self, user_id):
		"""
		id (string)
		Remove user form SQL database
		@return : True|False
		"""
		try:
			conn = self.getConn()
			cur = conn.cursor()
			cur.execute("DELETE FROM chatlist WHERE id = %s;", (user_id,))
			self.getConn().commit()
			cur.close()
			return True
		except psycopg2.DatabaseError as e:
			if conn:
				conn.rollback()
			print ('Error : %s' % e)
			return False

	def getAllUser(self):
		"""
		All user from SQL Database
		"""
		try:
			conn = self.getConn()
			cur = conn.cursor()
			cur.execute("SELECT * FROM chatlist")

			tmp_list = [] 
			while True:
				row = cur.fetchone()
				if row == None:
					break
				tmp_list.append(row)
		except psycopg2.DatabaseError as e:
			if conn:
				conn.rollback()
			print ('Error %s' % e)

		df = pd.DataFrame(tmp_list, columns=['id', 'first_name', 'username', 'active', 'start', 'end', 'type'])
		self.getConn().commit()
		cur.close()
		return df

	def save(self, dataframe, table):
		try:
			conn = self.getConn()
			cur = conn.cursor()
			dataframe.to_sql(table, index=False )
			self.getConn().commit()
			cur.close()
			return True
		except psycopg2.DatabaseError as e:
			if conn:
				conn.rollback()
			print ('Error : %s' % e)
			return False
	def save(self, id_row, first_name, username, active, start, end, type_row):
		"""
		Insert in database 
		@return : True|False
		"""
		try:
			conn = self.getConn()
			cur = conn.cursor()
			cur.execute("INSERT INTO chatlist (id, first_name, username, active, start_date, end_date, type, payment) VALUES (%s, %s, %s, %s, %s, %s, %s);", (id_row, first_name, username, active, start, end, type_row, 'NO'))
			self.getConn().commit()
			cur.close()
			return True
		except psycopg2.DatabaseError as e:
			if conn:
				conn.rollback()
			print ('Error : %s' % e)
			return False
	def update(self,user_id, field, value):
		try:
			conn = self.getConn()
			cur = conn.cursor()
			cur.execute("UPDATE chatlist SET %s = %s WHERE id = %s", (field, value, user_id))
			self.getConn().commit()
			cur.close()
			return True
		except psycopg2.DatabaseError as e:
			if conn:
				conn.rollback()
			print ('Error : %s' % e)
			return False

class Chat(User):
	"""
	--Chat Class
	"""
	def __init__(self):
		User.__init__(self)
		print("Initilizing... Chat")

	def getAllGroup(self):
		"""
		get all group list
		@return : pandas.DataFrame
		"""
		df = self.getAllUser()
		return df.loc[df['type'] == 'group']

	def getAllPrivate(self):
		"""
		get all private prople
		@return : pandas.DataFrame
		"""
		df = self.getAllUser()
		return df.loc[df['type'] == 'private']

	def getAllPrivateID(self):
		"""
		get all private pep ids
		@return : pandas.DataFrame
		"""
		r = self.getAllPrivate()
		return r['id']

	def refresh(self):
		"""
		refresh the database
		@return : True
		"""
		try:
			ids =[]
			updates = self.getBot().get_updates()
			for details in updates:
				if not details.message.chat.username:
					details.message.chat.username = details.message.chat.title
				self.save(details.message.chat_id, details.message.chat.first_name, details.message.chat.username, 'Y',  details.message.date, 'No', details.message.chat.type)
			return True
		except Exception as e:
			return False

class AutoMailer(User):
	"""
	--Automailer Class
	Time Formet : DD/MM/YYYY, HH:MM:SS 
	Example : 12/06/2018, 16:18:30
	"""
	def __init__(self):
		User.__init__(self)
		print("Initilizing... AutoMailer")

	def getAllMailler(self):
		"""
		return all mailling shedule in database
		@return pandas.DataFrame
		"""
		tmp_list = [] 
		try:
			conn = self.getConn()
			cur = conn.cursor()
			cur.execute("SELECT time, message FROM automailer ORDER BY time ASC")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				tmp_list.append(row)
		except psycopg2.DatabaseError as e:
			if conn:
				conn.rollback()
			print ('Error %s' % e)

		df = pd.DataFrame(tmp_list, columns=['time', 'message'])
		self.getConn().commit()
		cur.close()
		return df

	def newMailler(self, msgTime, message):
		"""
		Add new entry in mailling shedule
		@return : True| False
		"""
		try:
			conn = self.getConn()
			cur = conn.cursor()
			cur.execute("INSERT INTO automailer (time, message) VALUES (%s, %s);", (msgTime, message))
			self.getConn().commit()
			cur.close()
			return True
		except psycopg2.DatabaseError as e:
			if conn:
				conn.rollback()
			print ('Error : %s' % e)
			return False

	def deleteMailler(self, mail_time, message):
		"""
		Delete a entry in mailling shedule
		@return : True| False		
		"""
		try:
			conn = self.getConn()
			cur = conn.cursor()
			cur.execute("DELETE FROM automailer WHERE time = %s AND message = %s;", (mail_time, message))
			self.getConn().commit()
			cur.close()
			return True
		except psycopg2.DatabaseError as e:
			if conn:
				conn.rollback()
			print ('Error : %s' % e)
			return False

	def run(self):
		"""
		Run a thread for sending automatic mail 
		start a thread __sheduler() 
		"""
		self.sheduler_thread = threading.Thread(target = self.__sheduler, args=[])
		self.sheduler_thread.start()
		self.sheduler_thread.join()
		# sheduler_thread._Thread_stop()
		print("To take effect of edit in database, AutoMailer have to restart.")

	def __sheduler(self, sleepTime=1):
		"""
		takes data form getAllMailler()
		Run in a loop and match time and send mail accordingly
		"""
		while True:
			mails = self.getAllMailler()
			mail_time = list(mails['time'][0])
			cu_time =  time.strftime("%d/%m/%Y, %H:%M:%S")
			message = list(mails['message'][0])

			user_list = self.getAllUser()
			user_list = user_list.loc[user_list['active'].isin(["Y"])]
			user_list = list(user_list["id"])
			if cu_time == mail_time:
				self.send(user_list, message)
				print("Send to : " + str(user_list))
				self.deleteMailler(mail_time, message)
			time.sleep(sleepTime)

	def __getLastInsID(self):
		last_id = 0
		try:
			conn = self.getConn()
			cur = conn.cursor()
			cur.execute("SELECT max(id) FROM automailer")
			while True:
				row = cur.fetchone()
				if row == None:
					break
				last_id = row
				break
		except psycopg2.DatabaseError as e:
			print ('Error %s' % e)
		self.getConn().commit()
		cur.close()
		return last_id

	def __scanDatabase(self):
		last_ins_id = self.__getLastInsID()
		while True:
			new_ins_id = self.__getLastInsID()
			print(last_ins_id, new_ins_id)
			if last_ins_id != new_ins_id:
				self.sheduler_thread = threading.Thread(target = self.__sheduler, args=[])
				self.sheduler_thread.start()
				return True
			time.sleep(1)

class Regestration(Chat):
	"""
	--Regestration Class

	"""
	def __init__(self):
		Chat.__init__(self)
		print("Initilizing... Regestration")

	def run(self):
		"""
		Run a thread getReg() to refresh the user database 
		@obsulute
		"""
		thread = threading.Thread(target = self.getReg, args=[])
		thread.start()
		print("Regestration Thread is running")

	def __getSerchbyKey(self, key):
		"""
		Search on SQL database and return the match
		@return : pandas.DataFrame
		"""
		try:
			conn = self.getConn()
			cur = conn.cursor()
			cur.execute("SELECT * FROM search WHERE key = '"+key+"'")

			tmp_list = [] 
			while True:
				row = cur.fetchone()
				if row == None:
					break
				tmp_list.append(row)
		except psycopg2.DatabaseError as e:
			if conn:
				conn.rollback()
			print ('Error %s' % e)

		df = pd.DataFrame(tmp_list, columns=['key','message','timeForm','timeTo'])
		self.getConn().commit()
		cur.close()
		return df
	def deleteSearch(self, key, message):
		"""
		Delete search keyword 
		@return : True|False
		"""
		try:
			conn = self.getConn()
			cur = conn.cursor()
			cur.execute("DELETE FROM search WHERE key= %s AND message= %s;", (key, message))
			self.getConn().commit()
			cur.close()
			return True
		except psycopg2.DatabaseError as e:
			if conn:
				conn.rollback()
			print ('Error : %s' % e)
			return False


	def insertSerch(self, key, message, timeForm, timrTo):
		"""
		Insert new entry in search
		@return : True|False
		"""
		try:
			conn = self.getConn()
			cur = conn.cursor()
			cur.execute("INSERT INTO search (key, message, timeform	, timeto) VALUES (%s, %s, %s, %s);", (key.lower(), message, timeForm, timrTo))
			self.getConn().commit()
			cur.close()
			return True
		except psycopg2.DatabaseError as e:
			if conn:
				conn.rollback()
			print ('Error : %s' % e)
			return False

	def getReg(self):
		"""
		Refresh in every seconds
		@obsulute
		"""
		while True:
			try:
				self.refresh()
			except Exception as e:
				pass
			time.sleep(1)


	def __in_between(self, now, start, end):
		"""
		check if time lies in between two time
		@return : True|False
		"""
		if start <= end:
			return start <= now < end
		else: # over midnight e.g., 23:30-04:15
			return start <= now or now < end

	def polling(self):
		"""
		Run a polling method that do all operaion like __search, __help, __start
		"""
		updater = Updater(token=Token)
		dp = updater.dispatcher

		dp.add_handler(CommandHandler("start", self.__start))
		dp.add_handler(CommandHandler("help", self.__help))
		dp.add_handler(CommandHandler("payment", self.__payment))
		dp.add_handler(CommandHandler("search", self.__search, pass_args=True))
		dp.add_handler(MessageHandler(Filters.text, self.__echo))

		updater.start_polling()
		updater.idle()

	def __echo(self, bot, update):
		"""
		Echo for non CommandHandler sms
		"""
		if update.message.chat_id in self.getAllPrivate:
			update.message.reply_text("Invalid")

	def __help(self, bot, update):
		"""
		reply List of available command to command issuer
		"""
		update.message.reply_text('/start : New Regestration\n /help : list of all command\n/search: Search \n/payment: Pay')
	
	def __payment(self, bot, update):
			"""
			reply List of available command to command issuer
			"""
			update.message.reply_text('Pay at https://imjo.in/kaJYkC or https://www.example.com/'+str(update.message.chat.username))


	def __search(self, bot, update, args):
		"""
		Send search result to command issuer
		"""
		try:
			# read the search file
			data = self.__getSerchbyKey(args[0].lower())
			# print(data)
			res = "Search Result : \n"
			for index, row in data.iterrows():
				form_h, form_m = row["timeForm"].split(":")
				to_h, to_m = row["timeTo"].split(":")
				if self.__in_between(datetime.now().time(), time_format(int(form_h),int(form_m)), time_format(int(to_h), int(to_m))):
					res = res + '\n' +row["message"]
				update.message.reply_text(res)
		except Exception as e:
			print(e)
			update.message.reply_text('Please enter the text.')

	def __start(self, bot, update):
		"""
		Send a message when the command /start is issued.
		regester the user 
		"""
		if not update.message.chat.username:
			update.message.chat.username = update.message.chat.title
		
		self.save(update.message.chat_id, update.message.chat.first_name, update.message.chat.username, 'Y',  update.message.date, 'No', update.message.chat.type)
		self.save(update.message.from_user.id, update.message.from_user.first_name, update.message.from_user.username, 'Y',  update.message.date, 'No', 'private')
		
		print(str(update.message.chat.username)+"( "+str(update.message.chat_id)+" ) Added..")
		print(str(update.message.chat.username)+"( "+str(update.message.from_user.id)+" ) Added..")
		update.message.reply_text('Regestration Success...\nType /help to get the list of all command')


ti =  time.strftime("%d/%m/%Y, %H:%M:%S")

"""
b = Bot()
b.open()
b.close()
del b
"""
"""
u = User()
print(u.getAllUser())
u.save(1, "first_name", "user", "Y", "25-12", "No", "group")
u.remove('1')
"""
"""
c = Chat()
print(c.getAllPrivate())
print(c.getAllGroup())
print(c.getAllPrivateID())
c.refresh()
"""

"""
a = AutoMailer()
print(a.getAllMailler())
print(a.newMailler(ti, 'This is sample Text genrated by AutoMailer'))
print(a.deleteMailler(ti, 'This is sample Text genrated by AutoMailer'))
a.run()
"""
a = AutoMailer()

# print(a.newMailler(ti, 'This is sample Text genrated by AutoMailer'))
a.run()
"""
r = Regestration()
r.run()
print(r.deleteSearch("key2", "This is key2."))
print(r.insertSerch("key2", "This is key2.", "12:30", "23:30"))
r.polling()
"""