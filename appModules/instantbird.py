#instantbird App Module for NVDA

import appModuleHandler
from logHandler import log
import ui
import controlTypes
import unicodedata as ud
import api


class AppModule(appModuleHandler.AppModule):
	MessageHistoryLength = 9
	def __init__(self, *args, **kwargs):
		super(AppModule, self).__init__(*args, **kwargs)
		for n in xrange(1, self.MessageHistoryLength + 1):
			self.bindGesture("kb:NVDA+control+%s" % n, "readMessage")
	
	def script_readMessage(self, gesture):
		focus=api.getFocusObject()
		messageContainer = self.getMessageContainer(focus)
		if messageContainer is None:
			self.speak("Message container not found!")
		else:
			self.speak(self.getMessage(messageContainer,gesture))
	
	def getMessageContainer(self, focus):
		obj = focus
		mainWindow = None
		while(True):
			if obj.parent.name=='Desktop':
				mainWindow=obj
				break
			obj = obj.parent
		#for child in mainWindow.children:
			#if child.name==mainWindow.windowText and child.role==controlTypes.ROLE_FRAME:
		return self.getWYCIWYG(mainWindow)
	
	def getWYCIWYG(self, window):
		for child in window.children:
			if str(child.name)[:7]=="wyciwyg":
				return child
			elif len(child.children)>0:
				obj = self.getWYCIWYG(child)
				if not obj is None:
					return obj
	
	def getMessage(self, messageContainer, gesture):
		num=int(gesture.mainKeyName[-1])
		index = len(messageContainer.children) - num
		message = ""
		for child in messageContainer.children[index].children:
			if len(child.children)==0 and child.role!=controlTypes.ROLE_SEPARATOR:
				message = message + " " + child.name
			for grandChild in child.children:
				if len(grandChild.children)==0 and grandChild.role!=controlTypes.ROLE_SEPARATOR:
					message = message + " " + grandChild.name
				for grandGrandChild in grandChild.children:
					message = message + " " + str(grandGrandChild.name)
		return message
	
	def speak(self, message):
		ui.message(message)
	def logInfo(self, obj, eventName):
		log.debugWarning("Name of control on which %s fired: %s" % (eventName, obj.name))
		log.debugWarning("Value of control is: %s" % (obj.value))
		
	def event_NVDAObject_init(self,obj):
		if obj.role== controlTypes.ROLE_DOCUMENT and str(obj.parent.name)[:7]=="wyciwyg":
			log.debugWarning("Parent's name of new nvda object is: %s" % (str(obj.parent.name)))
			