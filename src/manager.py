import multiprocessing
from multiprocessing import Manager as man
from random import randint
import time


class Manager(object):
    """
    The Manager does exactly what would be expected. Only one exists per
    system, and it maintains an array of cubbyholes, an array of agents, and
    other information about system state.
    """
    def __init__(self, num_cubbies, initial_cubby_value, locking_enabled=True, terminate_on="transactions", termination_point=10):
        # terminate_on specifies 'transactions' or 'time', and
        # termination_point specifies (depending on the value of
        # terminate_on) the number of transactions or seconds after which to
        # terminate. 

        self.locking_enabled = locking_enabled
        self.terminate_on = terminate_on
        self.num_procs = multiprocessing.cpu_count()
        self.num_cubbies = num_cubbies
        self.manager = man()
        self.termination_point = int(termination_point)
        self.lock = multiprocessing.Lock()

        self.cubbyholes = self.manager.list()
        for cubby in range(num_cubbies):
            self.cubbyholes.append(int(initial_cubby_value))

    print("before run manager")
    def run(self):
        agent_processes = []

        if self.terminate_on == "time":
            print("manager if")
            start_time = time.clock() # Get current time
            end_time = int(start_time) + int(self.termination_point)
            while time.clock() < end_time:
                for proc in range(self.num_procs):
                    this_agent_process = multiprocessing.Process(target=self.modify_cubbyhole)
                    agent_processes.append(this_agent_process)
                    this_agent_process.start()

                # Make sure we wait for processes to finish before running again
                for elem in agent_processes:
                    proc = agent_processes.pop()
                    proc.join()

        else:
            print("manager else")
            run_counter = 0
            while run_counter < self.termination_point:
                for proc in range(self.num_procs):
                    this_agent_process = multiprocessing.Process(target=self.modify_cubbyhole)
                    agent_processes.append(this_agent_process)
                    this_agent_process.start()
                    run_counter += 1

                # Make sure we wait for processes to finish before running again
                for elem in agent_processes:
                    proc = agent_processes.pop()
                    proc.join()

    def modify_cubbyhole(self, delta_upper_bound=50):
        # The calling process should indicate which cubbyholes to modify,
        # but the Agent will automatically select a value by which to change
        # the cubbyholes' values.
        cubby_a = randint(0, len(self.cubbyholes)-1) #cubby_array[randint(0, self.num_self.cubbyholes-1)]
        cubby_b = randint(0, len(self.cubbyholes)-1) #cubby_array[randint(0, self.num_self.cubbyholes-1)]
        delta_value_a = randint(0, delta_upper_bound)
        delta_value_b = delta_value_a * (-1)
        print(multiprocessing.current_process())

        if self.locking_enabled:

            # Critical section
            print("Cubby Pre: " + str(self.cubbyholes[cubby_b]))
            self.lock.acquire()
            self.cubbyholes[cubby_a] += delta_value_a
            self.cubbyholes[cubby_b] += delta_value_b
            self.lock.release()

            print("Delta: " + str(delta_value_a))
            print("Cubby Post: " + str(self.cubbyholes[cubby_b]))

        else:
            # Change values without locking
            self.cubbyholes[cubby_a] += delta_value_a
            self.cubbyholes[cubby_b] += delta_value_b