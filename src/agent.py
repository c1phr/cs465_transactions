from time import sleep

class Agent(object):
    """ 
    The Agent is the active part of the transactional system. It decides
    which cubbyholes' values to change, and by how much, and manages locking
    those cubbyholes and changing the values.
    """
    def __init__(self, locking_enabled):
        self.locking_enabled=locking_enabled

    def modify_cubbyhole(a, b, delta_upper_bound=50):
        # The calling process should indicate which cubbyholes to modify,
        # but the Agent will automatically select a value by which to change
        # the cubbyholes' values.
        delta_value_a = bounded_random(0, delta_upper_bound)
        delta_value_b = delta_value_a * -1

        if locking_enabled:
            while a.lock_status() or b.lock_status() == True:
                sleep(0.001)
            a.lock()
            b.lock()
            a.change_value(delta_value_a)
            b.change_value(delta_value_b)
            a.release_lock()
            b.release_lock()

        else:
            a.change_value(delta_value_a)
            b.change_value(delta_value_b)
