class BasicFile(object):

    def __init__(self, name, path, last_mod_date):
        self.__name = name
        self.__path = path
        self.__last_mod_date = last_mod_date

    def __eq__(self, other):
        return self.__name == other.__name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = path

    @property
    def last_mod_date(self):
        return self.__last_mod_date

    @last_mod_date.setter
    def last_mod_date(self, last_mod_date):
        self.__last_mod_date = last_mod_date