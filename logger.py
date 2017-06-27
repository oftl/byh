import logging

class Logger (object):
    """ logging mixin
    """

    _logger = None

    @property
    def logger (self):
        if not self._logger:
            # TODO move to logfile
            handler = logging.FileHandler ('./byh.log')

            handler.setFormatter (logging.Formatter (fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

            logger = logging.getLogger ('byh')
            logger.addHandler (handler)
            logger.setLevel (logging.INFO)

            self._logger = logger

        return self._logger
