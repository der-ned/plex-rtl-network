
class ExceptionHandler(object):
	def __init__(self, exception):
		self.exception = exception

	def getBailOut(self):
		Log.Debug('Exception occured: ' + L(self.exception))
		return MessageContainer("Exceptionhandler: Error occured!", L(self.exception))