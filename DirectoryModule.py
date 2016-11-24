import BasicFileModule

class Directory(BasicFileModule.BasicFile):

    def __init__(self, name, path, last_mod_date):
        super(Directory, self).__init__(name, path, last_mod_date)

