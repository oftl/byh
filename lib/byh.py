class Byh (object):

    @property
    def name (self):
        return '{classname}'.format (classname = self.__class__.__name__)

    @property
    def id (self):
        return self._id

    @id.setter
    def id (self, v):
        self._id = v
