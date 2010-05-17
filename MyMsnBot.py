import logging
import gobject

import pymsn
import pymsn.event
import pymsn.conversation
import pymsn.profile

import MsnBot

class Bot(MsnBot.Bot):

	def process(self , contact , message ):
		self.broadcast( "Received " + message.content + " from " + str(contact.account) )

	
if __name__ == "__main__":
	
	logging.basicConfig( level = logging.INFO )

	bot = Bot(( "messenger.hotmail.com" , 1863 ))
	bot.login( ( username , password ) , name )
	bot.run()
