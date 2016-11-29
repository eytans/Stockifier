class Enumifier(object):
    def __init__(self):
        self.enums = {}
        self.names = []
        self.cur = 0

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.names[key]
        elif key not in self.enums:
            self.enums[key] = self.cur
            self.names.append(key)
            self.cur += 1
        return self.enums[key]


class EnumeratedTable(object):
    def __init__(self, data, enumerate_indexes=None):
        if enumerate_indexes is None:
            enumerate_indexes = []
            for i, val in enumerate(data[0]):
                try:
                    float(val)
                except:
                    enumerate_indexes += [i]

        self.enumifiers = {i: Enumifier() for i in enumerate_indexes}

        def enumify(i, val):
            if i not in enumerate_indexes:
                return float(val)
            return self.enumifiers[i][val]

        self.data = [[enumify(i, val) for i, val in enumerate(row)] for row in data]

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        return iter(self.data)
