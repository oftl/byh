import logging

logging.basicConfig (
    format = '%(asctime)s %(message)s',
    filename = './byh.log',
    level = logging.INFO,
)

class Byh (object):
    @property
    def id (self):
        return self._id

    @id.setter
    def id (self, v):
        self._id = v
