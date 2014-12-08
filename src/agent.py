from time import sleep
from random import randint

class Agent(object):
    """ 
    The Agent is the active part of the transactional system. It decides
    which cubbyholes' values to change, and by how much, and manages locking
    those cubbyholes and changing the values.
    """
    def __init__(self, num_cubbies, locking_enabled):
        self.locking_enabled=locking_enabled

    def modify_cubbyhole(cubby_a, cubby_b, delta_upper_bound=50
            agents_array):
        # The calling process should indicate which cubbyholes to modify,
        # but the Agent will automatically select a value by which to change
        # the cubbyholes' values.
        delta_value_a = random.randint(0, delta_upper_bound)
        delta_value_b = delta_value_a * (-1)

        if locking_enabled:
            while cubby_a.lock_status() or cubby_b.lock_status() == True:
                sleep(0.001)
            cubby_a.lock()
            cubby_b.lock()
            cubby_a.change_value(delta_value_a)
            cubby_b.change_value(delta_value_b)
            cubby_a.release_lock()
            cubby_b.release_lock()

        else:
            cubby_a.change_value(delta_value_a)
            cubby_b.change_value(delta_value_b)

    def run(cubby_array):
        while True:
            random_cubby_a = cubby_array[random.randint(0,
                self.num_cubbies)]
            random_cubby_b = cubby_array[random.randint(0,
                self.num_cubbies)]
            modify_cubbyhole(random_cubby_a, random_cubby_b)
