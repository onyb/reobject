from reobject.model import Model


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
    def __init__(self):
        self.called = 0

    def __call__(self, *args, **kwargs):
        self.called += 1


if __name__ == '__main__':
    view = View()
    Dispatcher.register(Counter)

    increment()
    increment()

    assert view.called == 2, view.called
    assert Counter.get_state() == 2
