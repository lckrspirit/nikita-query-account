#!/bin/python

import requests
import datetime
import telebot
import xml.etree.ElementTree as et

class Requests:
	def __init__(self):
		self.url = 'https://smspro.nikita.kg/api/info'
		self.req_xml = self.read_xml_file()
		self.answer = self.send_post()


	def read_xml_file(self):
		with open('req.xml', 'rb') as config:
			return config.read()

	def send_post(self):
		return requests.post(self.url, data=self.req_xml)


class Prepare:
	def __init__(self, answer):
		self.xml = et.fromstring(answer)
		self.answer_dict = {}

	def data_prepare(self):
		for item in self.xml:
			self.answer_dict[item.tag.replace('{http://Giper.mobi/schema/Info}', '')] = float(item.text)
		return self.answer_dict

class Push:
	TOKEN = 'Token'
	CHATID = 'idchat'
	
	def __init__(self):
		self.bot = telebot.TeleBot(self.TOKEN)

	def notify(self, message):
		self.bot.send_message(self.CHATID, f"Nikita account - {datetime.datetime.today().strftime('%d.%m (%H:%M)')}\n{message}")


class Application:
	def __init__(self):
		self.req = Requests()
		self.push = Push()
		self.prepare = Prepare(self.req.answer.text)
		self.status_dict = self.prepare.data_prepare()

	def run(self):
		message = ''
		if self.status_dict['status'] == 0:
			if self.status_dict['state'] == 1:
				message += f'Аккаунт заблокирован.\n'
			message += f"На балансе: {self.status_dict['account']} сом. \n"
			message += f"Стоимость одной SMS - {self.status_dict['smsprice']} coм. \n"
			self.push.notify(message)
		else:
			self.push.notify(f"Ошибка со статусом: {self.status_dict['status']}")

if __name__ == '__main__':
	app = Application()
	app.run()

	