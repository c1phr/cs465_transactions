from time import sleep
from random import randint


class Agent(object):
    """ 
    The Agent is the active part of the transactional system. It decides
    which cubbyholes' values to change, and by how much, and manages locking
    those cubbyholes and changing the values.
    """
    def __init__(self, num_cubbies, locking_enabled):
        self.locking_enabled = locking_enabled
        self.num_cubbies = num_cubbies

    def modify_cubbyhole(self, cubby_a, cubby_b, delta_upper_bound=50):
        # The calling process should indicate which cubbyholes to modify,
        # but the Agent will automatically select a value by which to change
        # the cubbyholes' values.
        delta_value_a = randint(0, delta_upper_bound)
        delta_value_b = delta_value_a * (-1)

        if self.locking_enabled:
            # Hold up here until both locks are free
            while cubby_a.get_lock() and cubby_b.get_lock() == True:
                print("Waiting")
                sleep(0.001)

            # Critical section
            cubby_a.set_lock()
            cubby_b.set_lock()
            print("Cubby Pre: " + str(cubby_a.get_value()))
            cubby_a.change_value(delta_value_a)
            cubby_b.change_value(delta_value_b)
            print("Delta: " + str(delta_value_a))
            print("Cubby Post: " + str(cubby_a.get_value()))
            cubby_a.release_lock()
            cubby_b.release_lock()

        else:
            # Change values without locking
            cubby_a.change_value(delta_value_a)
            cubby_b.change_value(delta_value_b)

    def run(self, cubby_array):
        random_cubby_a = cubby_array[randint(0, self.num_cubbies-1)]
        random_cubby_b = cubby_array[randint(0, self.num_cubbies-1)]
        self.modify_cubbyhole(random_cubby_a, random_cubby_b)
