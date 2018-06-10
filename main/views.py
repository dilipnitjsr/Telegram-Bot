"""
4 June 2018

615128532:AAGYHWB16Q-6XuItcpVureamKHzwGJMBQxE

"""
from django.http import HttpResponse
from django.template import loader
import sys

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

bot = Bot()

def index(request):
	if request.GET.get('refresh'):
		try:
			df = bot.loadtoCSV()
			bot.save(df)
		except Exception as e:
			pass
		return HttpResponse("Done Refresh")

	elif request.GET.get('remove'):
		try:
			bot.remove([request.GET.get('remove')])
		except Exception as e:
			raise
		return HttpResponse(str(request.GET.get('remove'))+" is removed.")

	elif request.GET.get('message'):
		l = []
		for id in request.GET:
			if id != "message":
				l.append(id)
		bot.send(l, request.GET.get('message'))
		return HttpResponse(str(len(l))+" message send.")
		
	elif request.GET.get('time'):
		template = loader.get_template('time.html')
		contacts = bot.readCSV()
		context = {
			'list': zip(contacts['id'], contacts['username']),
		}
		bot.save(contacts)
		return HttpResponse(template.render(context, request))

	else:
		template = loader.get_template('index.html')
		contacts = bot.readCSV()
		context = {
			'list': zip(contacts['id'], contacts['username']),
		}
		bot.save(contacts)
		return HttpResponse(template.render(context, request))