class ModelException(Exception):
    pass


class DoesNotExist(ModelException):
    pass


class MultipleObjectsReturned(ModelException):
    pass
