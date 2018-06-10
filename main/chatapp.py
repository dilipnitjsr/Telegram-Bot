
#615128532:AAGYHWB16Q-6XuItcpVureamKHzwGJMBQxE
#
import telegram
import numpy
import pandas as pd

class Bot:
	__removeList = []
	def __init__(self):
		#token form bot father
		self.__bot = telegram.Bot(token='615128532:AAGYHWB16Q-6XuItcpVureamKHzwGJMBQxE')
	def getAllUpdate(self):
		ids =[]
		updates = self.__bot.get_updates()
		for details in updates:
			if not details.message.chat.username:
				details.message.chat.username = details.message.chat.title
			ids.append([details.message.chat_id, details.message.chat.first_name, details.message.chat.username ])
		return pd.DataFrame(ids, columns=['id', 'first_name', 'username'])

	def loadtoCSV(self):
		frm_csv = pd.read_csv('chatlist.csv')
		frm_net = self.getAllUpdate()
		frames = [frm_csv,frm_net]
		all =  pd.concat(frames, axis=0, join='inner')
		all = all.drop_duplicates(subset=None, keep='first', inplace=False)
		all.index = [x for x in range(len(all))] # index recalculate
		return all
	def readCSV(self):
		frm_csv = pd.read_csv('chatlist.csv')
		return frm_csv

	def save(self, dataFrame):
		dataFrame.to_csv('chatlist.csv', sep=',', index=False)

	def send(self, contactList, message):
		self.__removeList = []
		for contact in contactList.iterrows():
			try:
				self.__bot.send_message(chat_id=contact[1]['id'], text=message)
			except Exception as e:
				self.__removeList.append(contact[1]['id'])
		return True

	def getRemoveList(self):
		return self.__removeList

	def remove(self, removeList):
		allList = self.readCSV()
		self.save(allList[~allList.username.isin(removeList)])
		return True

#Database maintain
b = Bot()
df = b.loadtoCSV()
b.save(df)
# print(df)
# b.send(df, "Test")
# print(b.remove(['PrashantKumar94']))