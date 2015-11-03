from abc import ABCMeta, abstractmethod
import Credentials

class AbstractDatabase(object):

	@abstractmethod
	def connect(self, Credentials):
		raise NotImplementedError()
	
	@abstractmethod
	def query(self, dbconn, query):
		raise NotImplementedError()