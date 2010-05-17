import logging
import gobject

import pymsn
import pymsn.event
import pymsn.conversation
import pymsn.profile

class Bot(pymsn.Client):

	_name = None
	_client_event_handler = None
	_address_book_event_handler = None
	_subscribers = {}

	def __init__(self,server):

		pymsn.Client.__init__(self,server)
		self._client_event_handler = ClientEventHandler(self)
		self._address_book_event_handler = AddressBookEventHandler(self)


	def login(self,details,name=None):

		if name == None:
			name = username

		self._name = name
		pymsn.Client.login(self,*details)


	def run( self ):
		
		mainloop = gobject.MainLoop()
	        mainloop.run()


	def send_text_message(self,contact,message):

		pymsn.Conversation( self , [contact] ).send_text_message(pymsn.ConversationMessage(message))


	def broadcast(self,message):
		
		for i in self._subscribers:
			pymsn.Conversation( self , [self._subscribers[i]] ).send_text_message(pymsn.ConversationMessage(message))	

	

	def process(self , contact , message ):
		pass


class AddressBookEventHandler(pymsn.event.AddressBookEventInterface):

	_conversations = []

	def on_addressbook_messenger_contact_added(self,contact):
		logging.info( "Adding " + str(contact) )
		self._client.address_book.accept_contact_invitation( contact , True)
		self._client.profile.display_name = self._client._name
		self._client.profile.presence = pymsn.Presence.ONLINE
		self._conversations.append(Conversation(pymsn.Conversation(self._client , [contact])))


class Conversation(pymsn.event.ConversationEventInterface):

	def on_conversation_message_received(self, sender, message):
       		logging.info( "Received " + str(message.content) + " from " + str(sender.account) )

		if message.content == "subscribe":
			self._client._client._subscribers[sender.account] = sender
			self._client.send_text_message(pymsn.ConversationMessage( "Subscribing" ))
		elif message.content == "unsubscribe":
			try:
				del(self._client._client._subscribers[sender.account])
			except KeyError,e:
				pass
			self._client.send_text_message(pymsn.ConversationMessage( "Unsubscribing") )
		else:
			self._client._client.process( sender , message )

	

    	def on_conversation_error(self, error_type, error):
		logging.error( "Error " + str(error_type) + " - " + str(error) )


class ClientEventHandler(pymsn.event.ClientEventInterface):

	_conversations = []
	
	def on_client_error( self , error_type , error ):
		if error_type == pymsn.event.ClientErrorType.AUTHENTICATION:
			logging.critical( "Unable to login" )
		else:
			logging.error( "Error " + error_type + " - " + error )


	def on_client_state_changed( self , state ):
		if state == pymsn.event.ClientState.OPEN:
			logging.info( "Logging on" )
            		self._client.profile.display_name = self._client._name
            		self._client.profile.presence = pymsn.Presence.ONLINE
			
			for contact in self._client.address_book.contacts:
				self._conversations.append(Conversation(pymsn.Conversation(self._client , [contact] ) ) )
				if contact.memberships == pymsn.profile.Membership.PENDING:
					logging.info("Found contact " + str(contact) + " with membership " + repr(contact.memberships) + ",adding" )
					self._client.address_book.accept_contact_invitation( contact , True)
					self._client.profile.display_name = self._client._name
					self._client.profile.presence = pymsn.Presence.ONLINE
					self._conversations.append(Conversation(pymsn.Conversation(self._client , [contact] )))

	
if __name__ == "__main__":
	
	logging.basicConfig( level = logging.INFO )

	bot = Bot(( "messenger.hotmail.com" , 1863 ))
	bot.login( (username,password) , name )
	bot.run()
