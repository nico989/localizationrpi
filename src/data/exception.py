class Error(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message

class HTTPError(Error):
    def __init__(self, message):
        super().__init__(message)    
