import logging

import MsnBot

class Bot(MsnBot.Bot):

	def process(self , contact , message ):

		self.send_text_message( contact , "You just said " + message.content )
		self.broadcast( "Received " + message.content + " from " + str(contact.account) )

	
if __name__ == "__main__":
	
	logging.basicConfig( level = logging.INFO )

	bot = Bot(( "messenger.hotmail.com" , 1863 ))
	bot.login( (username,password) , name )
	bot.run()
