class HPCError(Exception):
    """
    An error which occurs while processing a Data file.
    """
    def __init__(self, msg, debug_info=None):
        self.msg = msg
        self.debug = debug_info
    def __str__(self):
        return repr(self.msg)

