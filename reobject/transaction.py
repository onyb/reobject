# -*- coding: utf-8 -*-

from copy import deepcopy

from reobject.exceptions import CorruptTransactionException

__all__ = ['Transaction', 'transactional']


class Transaction(object):
    def __init__(self, obj):
        self.obj = obj
        self.__transaction_state = None

    def __enter__(self):
        self.__transaction_state = _memento(self.obj)

    def __exit__(self, *args):
        if any(args):
            if self.__transaction_state:
                self.__transaction_state()
            else:
                raise CorruptTransactionException


class transactional(object):
    def __init__(self, method):
        self.method = method

    def __get__(self, obj, T):
        def transaction(*args, **kwargs):
            state = _memento(obj)
            try:
                return self.method(obj, *args, **kwargs)
            except Exception as e:
                state()
                raise e

        return transaction


def _memento(obj):
    state = deepcopy(obj.__dict__)

    def f():
        obj.__dict__.clear()
        obj.__dict__.update(state)

    return f
