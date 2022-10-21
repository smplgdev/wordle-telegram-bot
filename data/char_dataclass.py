statuses = ('match', 'mismatch', 'missing')


class Char:
    def __init__(self, char: str, status: str = None):
        self.char = char
        self.status = status

    def set_status(self, status):
        """
        Set the status of the char

        :param status:
        :return: True if the status is set
        """
        self.status = status if status in statuses else None
        return bool(self.status)
