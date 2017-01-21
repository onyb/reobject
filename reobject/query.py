from reobject.utils import signed_attrgetter

class QuerySet(list):
    def __init__(self, *args, **kwargs):
        super(QuerySet, self).__init__(*args, **kwargs)

    def count(self):
        return len(self)

    def delete(self):
        for item in self:
            item.delete()

    def exists(self):
        return bool(self)

    def order_by(self, *args):
        return sorted(
            self, key=signed_attrgetter(*args)
        )
