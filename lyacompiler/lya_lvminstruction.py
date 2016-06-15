
class LyaInstruction(object):
    _code = None

    def __init__(self, arg1=None, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2

    def __str__(self):
        if self.arg1 is None and self.arg2 is None:
            return str(tuple([self._code]))
        elif self.arg2 is None:
            return str(tuple([self._code, self.arg1]))
        elif self.arg1 is None:
            # TODO: Error
            raise TypeError()
        else:
            return str(tuple([self._code, self.arg1, self.arg2]))

    def __repr__(self):
        return str(self)


class STP(LyaInstruction):
    """
    (’stp’)         # Start Program
                        sp=-1; D[0]=0
    """
    _code = 'stp'


class LBL(LyaInstruction):
    """
    (’lbl’, i)      # No operation
                        (define the label index i)
    """
    _code = 'lbl'
