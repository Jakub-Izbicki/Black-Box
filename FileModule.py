import BasicFileModule

class File(BasicFileModule.BasicFile):

    def __init__(self, name, path, last_mod_date):
        super(File, self).__init__(name, path, last_mod_date)