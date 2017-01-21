class QuerySet(list):
    def __init__(self, *args, **kwargs):
        super(QuerySet, self).__init__(*args, **kwargs)

    def delete(self):
        for item in self:
            item.delete()
