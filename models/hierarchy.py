from abc import ABC


class ROOT(ABC):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def getValue(self):
        return self.value


class VAR(ROOT):
    def __init__(self, var):
        super().__init__(var)


class PRED(ROOT):
    def __init__(self, pred):
        super().__init__(pred)


class OBJECT(ROOT):
    def __init__(self, object):
        super().__init__(object)
