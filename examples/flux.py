import unittest

from reobject.models import Model, Field


class Dispatcher(object):
    stores = set()

    @classmethod
    def register(cls, store):
        cls.stores.add(store)

    @classmethod
    def unregister(cls, store):
        cls.stores.remove(store)

    @classmethod
    def dispatch(cls, action):
        for store in cls.stores:
            store.get_update_hook()(action)


dispatch = Dispatcher.dispatch


class Store(object):
    _state = None

    @classmethod
    def get_state(cls):
        return cls._state

    @classmethod
    def emit_change_event(cls):
        raise NotImplementedError

    @staticmethod
    def reduce(state, action):
        return state

    @classmethod
    def get_update_hook(cls):
        def f(action):
            new_state = cls.reduce(cls._state, action)

            if new_state != cls._state:
                cls._state = new_state
                cls.emit_change_event()

        return f


class Counter(Store):
    _state = 0

    @staticmethod
    def reduce(state, action):
        if action['type'] == 'INCREMENT':
            return state + 1
        else:
            return state

    @classmethod
    def emit_change_event(cls):
        for listener in View.objects.all():
            listener()


def increment():
    dispatch({
        'type': 'INCREMENT'
    })


class View(Model):
    called = Field(default=0)

    def __call__(self, *args, **kwargs):
        self.called += 1


class TestFlux(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        View()
        Dispatcher.register(Counter)

    def test_flux_increment(self):
        increment()
        increment()

        assert View.objects.get().called == 2
        assert Counter.get_state() == 2
