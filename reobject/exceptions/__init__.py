class ModelException(Exception):
    pass


class DoesNotExist(ModelException):
    pass


class MultipleObjectsReturned(ModelException):
    pass


class CorruptTransactionException(ModelException):
    pass
