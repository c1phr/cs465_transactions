class Cubby:
    def __init__(self, value):
        self.__value = value
        self.__locked = False

    """
    Return the value of the cubby
    """
    def get_value(self):
        return self.__value

    """
    Takes in a delta value to apply to the cubby's value, rather than setting a direct value
    """
    def change_value(self, delta):
        self.__value += delta

    """
    Gets the lock status so the agent can manage it
    """
    def get_lock(self):
        return self.__locked

    """
    Lock the cubby's value
    """
    def set_lock(self):
        self.__locked = True

    """
    Release the cubby's lock
    """
    def release_lock(self):
        self.__locked = False